import json
from pathlib import Path
import numpy as np
import re

CAP_KEYS  = [
    "rpt_capacity_Ah","capacity_Ah","capacity","Q","Qd","Q_discharge","Capacity","cap",
    "capacity_discharge_C_5","capacity_discharge_C_2",
    "capacity_charge_C_5","capacity_charge_C_2"
]

def _extract_first_numeric(x):
    if isinstance(x,(int,float)) and np.isfinite(x):
        return float(x)
    if isinstance(x,str):
        m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", x)
        if m: 
            return float(m.group(0))
    return np.nan

def extract_capacity_from_list(data):
    values = []
    def flatten(x):
        if isinstance(x, list):
            for it in x:
                flatten(it)
        elif isinstance(x, (int, float)) and np.isfinite(x):
            values.append(float(x))
    flatten(data)
    if values:
        return float(np.nanmean(values))
    return np.nan

def scan_for_capacity(obj):
    values = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in CAP_KEYS:
                print(f"[MATCH] Key bulundu: {k}")
                if isinstance(v, (int, float)):
                    values.append(float(v))
                elif isinstance(v, list):
                    c = extract_capacity_from_list(v)
                    print(f"  Liste ortalama={c}")
                    if np.isfinite(c): 
                        values.append(c)
                else:
                    c = _extract_first_numeric(v)
                    print(f"  String sayı={c}")
                    if np.isfinite(c): 
                        values.append(c)
            # recursive tarama
            values.extend(scan_for_capacity(v))
    elif isinstance(obj, list):
        for it in obj:
            values.extend(scan_for_capacity(it))
    return values

if __name__ == "__main__":
    rpt_dir = Path(r"C:\Users\berha\battery_project\data\raw\isu-ilcc\RPT_json\RPT_json\Release 1.0")
    files = sorted(rpt_dir.glob("*.json"))
    capacity_rows = []

    for f in files:
        try:
            raw_text = f.read_text(encoding="utf-8")
            j = json.loads(raw_text)
            if isinstance(j, str):
                print(f"[DEBUG] {f.name} JSON içi string olarak geldi, ikinci kez parse ediliyor...")
                j = json.loads(j)
        except Exception as e:
            print(f"[ERROR] {f.name}: {e}")
            continue

        vals = scan_for_capacity(j)
        if not vals:
            print(f"[DEBUG] {f.name} -> Kapasite bulunamadı!")
            continue

        cap = float(np.nanmean(vals))

        # group_id ve cell_id çıkar
        mg = re.search(r"(G\d+)", f.name)
        mc = re.search(r"(C\d+)", f.name)
        g = mg.group(1) if mg else "GUNK"
        c = mc.group(1) if mc else "CUNK"

        capacity_rows.append({
            "group_id": g,
            "cell_id": c,
            "week_idx": 1,  # şimdilik 1
            "capacity": cap
        })

    print("capacity_rows örnek:", capacity_rows[:5], "...")

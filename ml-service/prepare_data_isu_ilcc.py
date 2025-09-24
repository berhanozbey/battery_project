"""
ISU-ILCC RPT_json'tan SOH zaman serisi ve genişletilmiş özellikler üretir.
- Tüm .json dosyalarını tarar (liste/dict farkına toleranslı).
- SOH = rpt_capacity / first_capacity
- Hedef: SOH_next
- Ek Özellikler: Ortalama voltajlar, DoD, C-rate, capacity fade
"""
import argparse, json, re
from pathlib import Path
import numpy as np
import pandas as pd
from utils import load_config, ensure_dir

# Kapasite için aday key’ler
CAP_KEYS  = [
    "rpt_capacity_Ah","capacity_Ah","capacity","Q","Qd","Q_discharge","Capacity","cap",
    "capacity_discharge_C_5","capacity_discharge_C_2",
    "capacity_charge_C_5","capacity_charge_C_2"
]
WEEK_KEYS = ["week_idx","week","weekIndex","Week","rpt_index"]

def _extract_first_numeric(x):
    if isinstance(x,(int,float)) and np.isfinite(x):
        return float(x)
    if isinstance(x,str):
        m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", x)
        if m: return float(m.group(0))
    return np.nan

def extract_capacity_from_list(data, max_depth=3, depth=0):
    """Liste içindeki (iç içe de olabilir) tüm sayıları çıkarır ve ortalamasını alır."""
    values = []

    def flatten(x, depth):
        if depth > max_depth:
            return
        if isinstance(x, list):
            for it in x:
                flatten(it, depth+1)
        elif isinstance(x, (int, float)) and np.isfinite(x):
            values.append(float(x))
        elif isinstance(x, str):
            # Tarih gibi stringleri sayıya çevirmeye çalışma
            m = re.search(r"^\d+(\.\d+)?$", x)
            if m:
                values.append(float(m.group(0)))

    flatten(data, depth)
    if values:
        return float(np.nanmean(values))
    return np.nan


def scan_for_capacity(obj, max_depth=10, depth=0):
    """Her türlü dict/list yapısını dolaşarak kapasite değerlerini bulur."""
    if depth > max_depth:
        return []

    values = []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if k in CAP_KEYS:
                if isinstance(v, (int, float)):
                    values.append(float(v))
                elif isinstance(v, list):
                    c = extract_capacity_from_list(v)
                    if np.isfinite(c):
                        values.append(c)
                else:
                    c = _extract_first_numeric(v)
                    if np.isfinite(c):
                        values.append(c)
            values.extend(scan_for_capacity(v, max_depth=max_depth, depth=depth+1))

    elif isinstance(obj, list):
        for it in obj:
            values.extend(scan_for_capacity(it, max_depth=max_depth, depth=depth+1))

    return values

def scan_for_voltage(obj):
    """QV_charge / QV_discharge içinden ortalama voltaj çıkarır."""
    avg_chg, avg_dchg = np.nan, np.nan
    if isinstance(obj, dict):
        for k, v in obj.items():
            if "QV_discharge" in k:
                if isinstance(v, list) and v:
                    avg_dchg = float(np.nanmean(v))
            if "QV_charge" in k:
                if isinstance(v, list) and v:
                    avg_chg = float(np.nanmean(v))
            if isinstance(v, (dict, list)):
                sub_chg, sub_dchg = scan_for_voltage(v)
                if np.isfinite(sub_chg): avg_chg = sub_chg
                if np.isfinite(sub_dchg): avg_dchg = sub_dchg
    elif isinstance(obj, list):
        for it in obj:
            sub_chg, sub_dchg = scan_for_voltage(it)
            if np.isfinite(sub_chg): avg_chg = sub_chg
            if np.isfinite(sub_dchg): avg_dchg = sub_dchg
    return avg_chg, avg_dchg

def pick_capacity(d: dict) -> float:
    vals = scan_for_capacity(d)
    if vals:
        return float(np.nanmean(vals))
    return np.nan

def pick_week(d: dict) -> float:
    for k in WEEK_KEYS:
        if k in d:
            v = _extract_first_numeric(d[k])
            if np.isfinite(v): return v
    return np.nan

def infer_ids_from_path(path: Path):
    s = str(path).replace("\\","/")
    mg = re.search(r"/(G\d+)\b", s, re.IGNORECASE)
    mc = re.search(r"/(C\d+)\b", s, re.IGNORECASE)
    group_id = (mg.group(1).upper() if mg else "GUNK")
    cell_id  = (mc.group(1).upper() if mc else "CUNK")
    return group_id, cell_id

def local_slope_last_k(weeks, soh, k=3):
    if len(weeks) < k: return np.nan
    w = np.asarray(weeks[-k:], float)
    y = np.asarray(soh[-k:], float)
    a, b = np.polyfit(w, y, 1)
    return float(a)

def main(args):
    cfg = load_config(args.config)
    data_root = Path(cfg["paths"]["data_root"])
    out_dir   = Path(cfg["paths"]["out_dir"])
    ensure_dir(out_dir)

    files = sorted(data_root.rglob("*.json"))
    if args.limit:
        files = files[:args.limit]

    rows = []
    cell_counters = {}

    for f in files:
        try:
            raw_text = f.read_text(encoding="utf-8")
            j = json.loads(raw_text)
            if isinstance(j, str):
                j = json.loads(j)
        except Exception:
            try:
                j = json.loads(f.read_text(encoding="latin-1"))
            except Exception:
                print(f"[WARN] Dosya okunamadı: {f}")
                continue

        cap = np.nan
        avg_chg, avg_dchg = np.nan, np.nan

        if isinstance(j, dict):
            cap = pick_capacity(j)
            avg_chg, avg_dchg = scan_for_voltage(j)
        elif isinstance(j, list):
            cap = extract_capacity_from_list(j)

        if not np.isfinite(cap):
            print(f"[DEBUG] İşlenen dosya: {f.name} -> Kapasite bulunamadı!")
            continue

        g, c = infer_ids_from_path(f)
        key = (g, c)
        if key not in cell_counters:
            cell_counters[key] = 1
        else:
            cell_counters[key] += 1
        wk = cell_counters[key]

        rows.append({
            "group_id": g, "cell_id": c,
            "week_idx": wk,
            "rpt_capacity_Ah": cap,
            "avgV_chg": avg_chg,
            "avgV_dchg": avg_dchg,
            "deltaV_hyst": avg_chg - avg_dchg if np.isfinite(avg_chg) and np.isfinite(avg_dchg) else np.nan
        })

    df = pd.DataFrame(rows)
    if df.empty:
        raise RuntimeError("RPT_json içinden kapasite/hafta çıkarılamadı.")

    # SOH ve SOH_next
    df = df.sort_values(["group_id","cell_id","week_idx"])
    df["first_cap"] = df.groupby(["group_id","cell_id"])["rpt_capacity_Ah"].transform("first")
    df["SOH"] = df["rpt_capacity_Ah"] / df["first_cap"]
    df["SOH_next"] = df.groupby(["group_id","cell_id"])["SOH"].shift(-1)

    # Capacity fade per cycle
    df["cap_fade"] = df.groupby(["group_id","cell_id"])["rpt_capacity_Ah"].diff()

    # Basit DoD (Discharge / Charge)
    df["DoD"] = np.nan  # Placeholder

    # Basit C-rate hesaplama (varsayımsal)
    nominal_cap = df["first_cap"].mean()
    df["C_rate"] = df["rpt_capacity_Ah"] / nominal_cap if np.isfinite(nominal_cap) else np.nan

    # Basit özellikler
    feats = []
    k = max(3, int(cfg["soh"]["min_points_for_trend"]))
    for (g,c), grp in df.groupby(["group_id","cell_id"]):
        weeks = grp["week_idx"].tolist()
        sohs  = grp["SOH"].tolist()
        slope = local_slope_last_k(weeks, sohs, k=k)
        for _, r in grp.iterrows():
            feats.append({
                "group_id": g,
                "cell_id": c,
                "week_idx": r["week_idx"],
                "SOH": r["SOH"],
                "current_SOH": r["SOH"],
                "weeks_since_start": r["week_idx"] - grp["week_idx"].iloc[0],
                "local_slope_k": slope,
                "n_points_cell": len(grp),
                "SOH_next": r["SOH_next"],
                "avgV_chg": r["avgV_chg"],
                "avgV_dchg": r["avgV_dchg"],
                "deltaV_hyst": r["deltaV_hyst"],
                "cap_fade": r["cap_fade"],
                "DoD": r["DoD"],
                "C_rate": r["C_rate"],
            })

    out = pd.DataFrame(feats)
    out.to_parquet(out_dir / "features.parquet", index=False)
    print(f"[OK] features.parquet -> {out_dir/'features.parquet'} | rows={len(out)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--limit", type=int, default=None, help="İşlenecek dosya sayısını sınırla")
    main(parser.parse_args())

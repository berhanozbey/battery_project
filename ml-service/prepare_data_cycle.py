"""
ISU-ILCC cycle JSON'lardan DoD, C-rate ve voltaj özelliklerini çıkarır.
"""
import argparse, json, re
from pathlib import Path
import numpy as np
import pandas as pd
from utils import load_config, ensure_dir

def _safe_mean(x):
    return float(np.nanmean(x)) if len(x) > 0 else np.nan

def _extract_first_numeric(x):
    if isinstance(x, (int, float)) and np.isfinite(x):
        return float(x)
    if isinstance(x, str):
        import re
        m = re.search(r"[-+]?\d*\.?\d+(?:[eE][-+]?\d+)?", x)
        if m: 
            return float(m.group(0))
    return np.nan

def scan_cycle(obj):
    """Cycle JSON içinden kapasite, voltaj ve akım çıkarır."""
    cap_chg, cap_dchg, avgV_chg, avgV_dchg, avgI_chg, avgI_dchg = [], [], [], [], [], []
    if isinstance(obj, dict):
        for k, v in obj.items():
            if "capacity_charge" in k and isinstance(v, list):
                cap_chg.extend(v)
            if "capacity_discharge" in k and isinstance(v, list):
                cap_dchg.extend(v)
            if "V_charge" in k and isinstance(v, list):
                avgV_chg.extend(v)
            if "V_discharge" in k and isinstance(v, list):
                avgV_dchg.extend(v)
            if "I_charge" in k and isinstance(v, list):
                avgI_chg.extend(v)
            if "I_discharge" in k and isinstance(v, list):
                avgI_dchg.extend(v)
            if isinstance(v, (dict, list)):
                c2 = scan_cycle(v)
                for i, arr in enumerate(c2):
                    if isinstance(arr, list):
                        [cap_chg, cap_dchg, avgV_chg, avgV_dchg, avgI_chg, avgI_dchg][i].extend(arr)
    elif isinstance(obj, list):
        for it in obj:
            c2 = scan_cycle(it)
            for i, arr in enumerate(c2):
                if isinstance(arr, list):
                    [cap_chg, cap_dchg, avgV_chg, avgV_dchg, avgI_chg, avgI_dchg][i].extend(arr)
    return cap_chg, cap_dchg, avgV_chg, avgV_dchg, avgI_chg, avgI_dchg

def main(args):
    cfg = load_config(args.config)
    data_root = Path(cfg["paths"]["data_root"])
    out_dir   = Path(cfg["paths"]["out_dir"])
    ensure_dir(out_dir)

    cycle_dir = data_root / "Cycle_json"
    files = sorted(cycle_dir.rglob("*.json"))
    if args.limit:
        files = files[:args.limit]

    rows = []
    for f in files:
        try:
            raw = f.read_text(encoding="utf-8")
            j = json.loads(raw)
            if isinstance(j, str):
                j = json.loads(j)
        except Exception as e:
            print(f"[WARN] {f.name} okunamadı: {e}")
            continue

        cap_chg, cap_dchg, Vc, Vd, Ic, Id = scan_cycle(j)
        cap_chg_val = _safe_mean(cap_chg)
        cap_dchg_val = _safe_mean(cap_dchg)

        dod = cap_dchg_val / cap_chg_val if cap_chg_val and np.isfinite(cap_chg_val) else np.nan
        cr_chg = abs(_safe_mean(Ic)) / cap_chg_val if cap_chg_val and np.isfinite(cap_chg_val) else np.nan
        cr_dchg = abs(_safe_mean(Id)) / cap_dchg_val if cap_dchg_val and np.isfinite(cap_dchg_val) else np.nan

        rows.append({
            "file": f.name,
            "capacity_charge_Ah": cap_chg_val,
            "capacity_discharge_Ah": cap_dchg_val,
            "DoD": dod,
            "avgV_chg": _safe_mean(Vc),
            "avgV_dchg": _safe_mean(Vd),
            "C_rate_chg": cr_chg,
            "C_rate_dchg": cr_dchg
        })

    df = pd.DataFrame(rows)
    out_path = out_dir / "features_cycle.parquet"
    df.to_parquet(out_path, index=False)
    print(f"[OK] features_cycle.parquet -> {out_path} | rows={len(df)}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--config", default="config.yaml")
    parser.add_argument("--limit", type=int, default=None, help="İşlenecek dosya sayısını sınırla")
    main(parser.parse_args())

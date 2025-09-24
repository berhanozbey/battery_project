"""
rul_linear.py
Basit doğrusal eğilimle (last K SOH points) RUL (hafta) tahmini.

- Her (group_id, cell_id) için SOH zaman serisi alınır.
- EOL eşiği: 0.80 (args.threshold)
- "Origin" noktası, EOL'e düşmeden hemen önceki SON SOH>=0.80 noktasıdır.
  (Cihaz hiç 0.80 altına düşmediyse -> sağdan sansürlü = censored=True)
- Son K nokta ile (SOH ~ a*week + b) doğrusu fit edilir.
- Eğim (a) >= 0 ise RUL = NaN (bozulma görünmüyor).
- Aksi halde x* = (threshold - b)/a, RUL_pred = x* - week_origin
- Gerçek RUL (uncensored için): first_week_at_or_below_0.80 - week_origin
- MAE sadece uncensored hücrelerde raporlanır.
"""

import argparse
import numpy as np
import pandas as pd
from pathlib import Path

def fit_rul_from_last_k(weeks, sohs, origin_idx, k, threshold=0.80):
    """
    weeks, sohs: sıralı listeler (aynı uzunlukta)
    origin_idx : origin = en son SOH >= threshold olan index
    k          : son k nokta ile fit
    """
    if origin_idx < 0:
        return np.nan, np.nan, np.nan, np.nan  # hiç >= threshold yok

    start = max(0, origin_idx - (k - 1))
    w = np.asarray(weeks[start:origin_idx + 1], dtype=float)
    y = np.asarray(sohs[start:origin_idx + 1], dtype=float)

    # En az 2 nokta lazım
    if len(w) < 2 or len(y) < 2:
        return np.nan, np.nan, np.nan, np.nan

    # Doğrusal fit: y = a*x + b
    a, b = np.polyfit(w, y, 1)

    if not np.isfinite(a) or not np.isfinite(b) or a >= 0:
        return a, b, np.nan, np.nan  # eğim pozitif/bozulma yok → NaN

    # EOL kesişimi
    x_star = (threshold - b) / a
    if not np.isfinite(x_star):
        return a, b, np.nan, np.nan

    origin_week = weeks[origin_idx]
    rul_pred = x_star - origin_week
    # negatif olursa 0'a sabitle (sayısal taşmalar için)
    if not np.isfinite(rul_pred) or rul_pred < 0:
        rul_pred = 0.0

    return a, b, x_star, float(rul_pred)

def compute_rul_per_cell(df, k=4, threshold=0.80):
    """
    df: features.parquet içeriği (group_id, cell_id, week_idx, SOH kolonları olmalı)
    """
    results = []
    for (g, c), grp in df.sort_values(["group_id","cell_id","week_idx"]).groupby(["group_id","cell_id"]):
        weeks = grp["week_idx"].astype(float).tolist()
        sohs  = grp["SOH"].astype(float).tolist()

        # İlk SOH<=threshold haftasını bul
        idx_cross = next((i for i, s in enumerate(sohs) if np.isfinite(s) and s <= threshold), None)

        if idx_cross is None:
            # Sansürlü: hiç 0.80 altına inmemiş
            origin_idx = len(sohs) - 1  # en son gözlem
            a, b, x_star, rul_pred = fit_rul_from_last_k(weeks, sohs, origin_idx, k, threshold)
            true_rul = np.nan
            censored = True
            origin_week = weeks[origin_idx] if len(weeks) else np.nan
        else:
            # EOL'den hemen önceki son >=threshold noktayı origin seç
            origin_idx = max(0, idx_cross - 1)
            a, b, x_star, rul_pred = fit_rul_from_last_k(weeks, sohs, origin_idx, k, threshold)
            # Gerçek RUL: EOL haftası - origin haftası
            if origin_idx < len(weeks):
                origin_week = weeks[origin_idx]
                true_rul = weeks[idx_cross] - origin_week
                if true_rul < 0:  # güvenlik
                    true_rul = 0.0
            else:
                origin_week = np.nan
                true_rul = np.nan
            censored = False

        results.append({
            "group_id": g,
            "cell_id": c,
            "k_used": k,
            "threshold": threshold,
            "origin_week_idx": origin_week,
            "slope_a": a,
            "intercept_b": b,
            "x_star_week": x_star,
            "RUL_pred_weeks": rul_pred,
            "RUL_true_weeks": true_rul,
            "censored": censored,
            "n_points": len(weeks),
        })
    return pd.DataFrame(results)

def main(args):
    path = Path(args.input)
    df = pd.read_parquet(path)
    # gerekli kolonların varlığını garanti et
    required = {"group_id","cell_id","week_idx","SOH"}
    missing = required - set(df.columns)
    if missing:
        raise ValueError(f"Missing columns in input: {missing}")

    res = compute_rul_per_cell(df, k=args.k, threshold=args.threshold)

    # MAE (sadece uncensored)
    eval_df = res[(~res["censored"]) & res["RUL_true_weeks"].notna() & res["RUL_pred_weeks"].notna()]
    if len(eval_df) > 0:
        mae = np.mean(np.abs(eval_df["RUL_true_weeks"] - eval_df["RUL_pred_weeks"]))
        print(f"[RUL] Uncensored cells = {len(eval_df)} | MAE (weeks) = {mae:.3f}")
    else:
        print("[RUL] No uncensored cells to evaluate (MAE not computed).")

    # Kaydet
    out_path = Path(args.out)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    res.to_parquet(out_path, index=False)
    print(f"[OK] Saved RUL table → {out_path} | rows={len(res)}")

if __name__ == "__main__":
    p = argparse.ArgumentParser()
    p.add_argument("--input", default="../artifacts/features.parquet", help="features.parquet path")
    p.add_argument("--out",   default="../artifacts/rul_linear.parquet", help="output parquet path")
    p.add_argument("--k", type=int, default=4, help="last K SOH points for linear fit")
    p.add_argument("--threshold", type=float, default=0.80, help="EOL SOH threshold")
    args = p.parse_args()
    main(args)

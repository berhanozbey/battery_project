"""
train_soh.py
SOH (State of Health) prediction using LinearRegression and RandomForest.
Group-level cross-validation (GroupKFold) ile MAE ve RMSE raporlar.
"""

import argparse
import pandas as pd
import numpy as np
from sklearn.model_selection import GroupKFold
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error


def evaluate_model(model, X, y, groups, model_name="Model"):
    """GroupKFold ile MAE ve RMSE hesapla"""
    unique_groups = np.unique(groups)
    n_splits = min(5, len(unique_groups))  # grup sayısından fazla split olmasın

    if n_splits < 2:
        print(f"[WARN] {model_name}: Yeterli grup yok (grup sayısı={len(unique_groups)}). CV yapılamadı.")
        return

    gkf = GroupKFold(n_splits=n_splits)
    maes, rmses = [], []

    for fold, (train_idx, test_idx) in enumerate(gkf.split(X, y, groups), 1):
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        mae = mean_absolute_error(y_test, y_pred)
        rmse = mean_squared_error(y_test, y_pred, squared=False)

        maes.append(mae)
        rmses.append(rmse)

        print(f"[Fold {fold}] {model_name} → MAE={mae:.4f}, RMSE={rmse:.4f}")

    print(f"\n📊 {model_name} ({n_splits}-fold GroupKFold)")
    print(f"  MAE  : {np.mean(maes):.4f} ± {np.std(maes):.4f}")
    print(f"  RMSE : {np.mean(rmses):.4f} ± {np.std(rmses):.4f}\n")


def main(args):
    # Veri yükle
    df = pd.read_parquet(args.input)
    print(f"[INFO] Loaded dataset with {len(df)} rows and {df.shape[1]} columns.")

    # Hedef → SOH_next (NaN'leri at)
    df = df.dropna(subset=["SOH_next"])
    print(f"[INFO] Rows after dropping NaN targets: {len(df)}")

    # Özellikler
    feature_cols = [
        "current_SOH", "weeks_since_start", "local_slope_k",
        "avgV_chg", "avgV_dchg", "deltaV_hyst"
    ]
    X = df[feature_cols].fillna(0.0).values
    y = df["SOH_next"].values
    groups = df["group_id"].values

    # Modeller
    linreg = LinearRegression()
    rf = RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1)

    # Değerlendirme
    evaluate_model(linreg, X, y, groups, model_name="Linear Regression")
    evaluate_model(rf, X, y, groups, model_name="Random Forest")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--input", default="artifacts/features.parquet", help="Path to features.parquet")
    args = parser.parse_args()
    main(args)

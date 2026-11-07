import json
import os
import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
)

def run_evaluation():
    print("[INFO] Starting Model Evaluation...")
    try:
        X_test = np.load("data/processed/X_test_final.npy")
        y_test = np.load("data/processed/y_test.npy")
        model = joblib.load("models/random_forest_baseline.pkl")
        y_pred = model.predict(X_test)
        y_proba = model.predict_proba(X_test)[:, 1]
    except Exception as exc:
        print(f"[ERROR] Evaluation inputs/model unavailable: {exc}")
        return False

    metrics = {
        "accuracy": float(accuracy_score(y_test, y_pred)),
        "precision": float(precision_score(y_test, y_pred, zero_division=0)),
        "recall": float(recall_score(y_test, y_pred, zero_division=0)),
        "f1_score": float(f1_score(y_test, y_pred, zero_division=0)),
        "roc_auc": float(roc_auc_score(y_test, y_proba)),
    }
    print("\n--- Model Evaluation Report ---")
    for name, value in metrics.items():
        print(f"{name.replace('_', ' ').title():10s}: {value:.4f}")
    print("-------------------------------\n")

    os.makedirs("artifacts", exist_ok=True)
    with open("artifacts/evaluation_report.json", "w", encoding="utf-8") as f:
        json.dump({"metrics": metrics}, f, indent=4)

    # Export false-positive/false-negative examples when raw rows are available.
    raw_path = "data/raw/churn.csv"
    if os.path.exists(raw_path):
        df = pd.read_csv(raw_path)
        from sklearn.model_selection import train_test_split
        X_raw = df.drop(columns=["Churn"])
        _, X_test_raw = train_test_split(
            X_raw, test_size=0.2, random_state=42, stratify=df["Churn"]
        )
        if len(X_test_raw) == len(y_test):
            errors = X_test_raw.reset_index(drop=True).copy()
            errors["Actual_Churn"] = y_test
            errors["Predicted_Churn"] = y_pred
            os.makedirs("outputs", exist_ok=True)
            errors[(errors.Actual_Churn == 1) & (errors.Predicted_Churn == 0)].to_csv(
                "outputs/false_negatives.csv", index=False
            )
            errors[(errors.Actual_Churn == 0) & (errors.Predicted_Churn == 1)].to_csv(
                "outputs/false_positives.csv", index=False
            )
    print("[SUCCESS] Evaluation report saved to artifacts/evaluation_report.json")
    return True

if __name__ == "__main__":
    import sys
    sys.exit(0 if run_evaluation() else 1)

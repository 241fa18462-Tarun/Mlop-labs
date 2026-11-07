import logging
from pathlib import Path

import joblib
import pandas as pd
from flask import Flask, jsonify, request

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)

BASE_DIR = Path(__file__).resolve().parent
MODEL_DIR = BASE_DIR / "models"

FEATURES = [
    "gender",
    "SeniorCitizen",
    "Partner",
    "Dependents",
    "tenure",
    "PhoneService",
    "MultipleLines",
    "InternetService",
    "OnlineSecurity",
    "OnlineBackup",
    "DeviceProtection",
    "TechSupport",
    "StreamingTV",
    "StreamingMovies",
    "Contract",
    "PaperlessBilling",
    "PaymentMethod",
    "MonthlyCharges",
    "TotalCharges",
]

NUMERIC_FEATURES = [
    "SeniorCitizen",
    "tenure",
    "MonthlyCharges",
    "TotalCharges",
]

preprocessor = joblib.load(MODEL_DIR / "preprocessor.pkl")
model = joblib.load(MODEL_DIR / "random_forest_mlflow.pkl")


@app.route("/", methods=["GET"])
def home():
    return jsonify({
        "project": "Customer Churn Prediction API",
        "status": "running",
        "model": "Random Forest",
        "version": "5.0",
        "endpoints": {
            "health": "/health",
            "predict": "/predict",
            "model_info": "/model-info"
        }
    })


@app.route("/health", methods=["GET"])
def health():
    return jsonify({
        "status": "healthy",
        "model_loaded": True
    })


@app.route("/model-info", methods=["GET"])
def model_info():
    return jsonify({
        "model": "Random Forest",
        "input_features": len(FEATURES),
        "processed_features": int(model.n_features_in_),
        "classes": [int(c) for c in model.classes_]
    })


@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json(silent=True)

    if not isinstance(data, dict):
        return jsonify({
            "error": "Please send a valid JSON object."
        }), 400

    # Also accept {"data": {...}}
    if "data" in data and isinstance(data["data"], dict):
        data = data["data"]

    missing = [feature for feature in FEATURES if feature not in data]

    if missing:
        return jsonify({
            "error": "Missing required customer features.",
            "missing_features": missing
        }), 400

    try:
        customer = {feature: data[feature] for feature in FEATURES}
        customer_df = pd.DataFrame([customer], columns=FEATURES)

        for feature in NUMERIC_FEATURES:
            customer_df[feature] = pd.to_numeric(
                customer_df[feature], errors="coerce"
            )

        required_numeric = [
            "SeniorCitizen", "tenure", "MonthlyCharges"
        ]

        invalid = [
            feature for feature in required_numeric
            if pd.isna(customer_df.loc[0, feature])
        ]

        if invalid:
            return jsonify({
                "error": "Invalid numeric values.",
                "features": invalid
            }), 400

        transformed = preprocessor.transform(customer_df)

        prediction = int(model.predict(transformed)[0])
        probabilities = model.predict_proba(transformed)[0]

        churn_index = list(model.classes_).index(1)
        no_churn_index = list(model.classes_).index(0)

        churn_probability = float(probabilities[churn_index])
        no_churn_probability = float(probabilities[no_churn_index])

        return jsonify({
            "status": "success",
            "prediction_class": prediction,
            "prediction": "Churn" if prediction == 1 else "No Churn",
            "churn_probability_percent": round(
                churn_probability * 100, 2
            ),
            "no_churn_probability_percent": round(
                no_churn_probability * 100, 2
            ),
            "model": "Random Forest"
        })

    except Exception:
        app.logger.exception("Prediction failed")
        return jsonify({
            "error": "Prediction failed. Check the API logs."
        }), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

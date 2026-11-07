from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load your trained model if available
# model = joblib.load('models/best_model.pkl')

@app.route('/')
def home():
    return jsonify({"status": "Churn Prediction API is running!"})

@app.route('/predict', methods=['POST'])
def predict():
    data = request.get_json()
    # Add inference logic here
    return jsonify({"prediction": "Sample Churn Prediction Result"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
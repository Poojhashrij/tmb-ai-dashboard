import joblib
import os

MODEL_PATH = "backend/models/tmb_predictor.joblib"

def predict_response(tmb, msi):
    model = joblib.load(MODEL_PATH)
    prediction = model.predict([[tmb, msi]])[0]
    prob = model.predict_proba([[tmb, msi]])[0][1]
    return f"{prediction} (Confidence: {round(prob*100, 2)}%)"

import os
import joblib
import numpy as np


# ============================================================
# LOAD XGBOOST MODEL
# ============================================================

MODEL_PATH = os.path.join(
    "saved_models",
    "xgboost_model.pkl"
)

SCALER_PATH = os.path.join(
    "saved_models",
    "scaler.pkl"
)


model = joblib.load(MODEL_PATH)
scaler = joblib.load(SCALER_PATH)


# ============================================================
# PREDICT WATER QUALITY
# ============================================================

def predict_water_quality(sample):

    # Convert input to numpy array
    sample = np.array(sample, dtype=float).reshape(1, -1)

    # Apply the same scaler used during training
    sample_scaled = scaler.transform(sample)

    # Prediction
    prediction = model.predict(sample_scaled)[0]

    # Probability of Potable class
    probability = model.predict_proba(sample_scaled)[0][1]

    return int(prediction), float(probability)
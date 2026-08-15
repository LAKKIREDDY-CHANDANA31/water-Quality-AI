import os
import numpy as np
import joblib
from tensorflow.keras.models import load_model


# ============================================================
# PROJECT PATH
# ============================================================

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

MODEL_PATH = os.path.join(
    BASE_DIR,
    "saved_models",
    "dnn_model.keras"
)

SCALER_PATH = os.path.join(
    BASE_DIR,
    "saved_models",
    "scaler.pkl"
)


# ============================================================
# LOAD DNN MODEL
# ============================================================

model = load_model(MODEL_PATH)

# Load the scaler used during training
scaler = joblib.load(SCALER_PATH)


# ============================================================
# PREDICT WATER QUALITY
# ============================================================

def predict_water_quality(sample):

    # Convert input to NumPy array
    sample = np.array(sample, dtype=np.float32).reshape(1, -1)

    # Scale input using the same scaler used during training
    sample_scaled = scaler.transform(sample)

    # DNN prediction
    probability = float(model.predict(sample_scaled, verbose=0)[0][0])

    # Convert probability into class
    if probability >= 0.5:
        prediction = 1
    else:
        prediction = 0

    return prediction, probability
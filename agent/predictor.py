import os
import numpy as np
import joblib
import tensorflow as tf
from tensorflow.keras.models import load_model


# ============================================================
# LIMIT TENSORFLOW RESOURCE USAGE FOR RENDER
# ============================================================

tf.config.threading.set_intra_op_parallelism_threads(1)
tf.config.threading.set_inter_op_parallelism_threads(1)


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
    sample = np.asarray(sample, dtype=np.float32).reshape(1, -1)

    # Scale input using the same scaler used during training
    sample_scaled = scaler.transform(sample)

    # Direct TensorFlow inference
    # This avoids the extra overhead of model.predict()
    probability = float(
        model(sample_scaled, training=False).numpy()[0][0]
    )

    # Convert probability into class
    prediction = 1 if probability >= 0.5 else 0

    return prediction, probability
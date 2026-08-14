from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data
from models.tabnet_model import build_tabnet_model

import numpy as np
import os
import joblib

# Load and clean dataset
data = load_and_clean_data()

# Split and scale dataset
X_train, X_test, y_train, y_test = split_and_scale_data(data)

# Convert data to NumPy arrays
X_train = np.array(X_train)
X_test = np.array(X_test)
y_train = np.array(y_train)
y_test = np.array(y_test)

# Build TabNet model
model = build_tabnet_model()

# Train the model
model.fit(
    X_train,
    y_train,
    eval_set=[(X_test, y_test)],
    max_epochs=20,
    patience=10,
    batch_size=256,
    virtual_batch_size=128
)

# Evaluate the model
predictions = model.predict(X_test)

accuracy = (predictions == y_test).mean()

print("\nTabNet Test Accuracy:", accuracy)

# Create folder if it doesn't exist
os.makedirs("saved_models", exist_ok=True)

# Save the trained model
joblib.dump(model, "saved_models/tabnet_model.pkl")

print("\nTabNet model saved successfully!")
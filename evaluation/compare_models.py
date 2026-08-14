from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data

import numpy as np
import joblib

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# Load dataset
data = load_and_clean_data()

# Split dataset
X_train, X_test, y_train, y_test = split_and_scale_data(data)

# Convert to NumPy arrays
X_test = np.array(X_test)
y_test = np.array(y_test)

# Load trained TabNet model
model = joblib.load("saved_models/tabnet_model.pkl")

# Predict
y_pred = model.predict(X_test)

print("\n====== TABNET RESULTS ======\n")

print("Accuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))
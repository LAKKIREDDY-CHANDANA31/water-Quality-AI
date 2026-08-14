from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data

from tensorflow.keras.models import load_model

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report
)

# Load data
data = load_and_clean_data()

# Split data
X_train, X_test, y_train, y_test = split_and_scale_data(data)

# Load trained model
model = load_model("saved_models/dnn_model.keras")

# Predict probabilities
y_pred = model.predict(X_test)

# Convert probabilities to 0 or 1
y_pred = (y_pred > 0.5).astype(int)

print("\nAccuracy :", accuracy_score(y_test, y_pred))
print("Precision:", precision_score(y_test, y_pred))
print("Recall   :", recall_score(y_test, y_pred))
print("F1 Score :", f1_score(y_test, y_pred))

print("\nConfusion Matrix")
print(confusion_matrix(y_test, y_pred))

print("\nClassification Report")
print(classification_report(y_test, y_pred))
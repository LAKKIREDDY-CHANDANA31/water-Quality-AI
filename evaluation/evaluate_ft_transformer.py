from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data

import pandas as pd
from pytorch_tabular import TabularModel

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    confusion_matrix,
    classification_report,
)

# ==========================
# Load and Clean Dataset
# ==========================
data = load_and_clean_data()

# ==========================
# Split Dataset
# ==========================
X_train, X_test, y_train, y_test = split_and_scale_data(data)

# ==========================
# Convert Test Data to DataFrame
# ==========================
test_df = pd.DataFrame(
    X_test,
    columns=[
        "ph",
        "Hardness",
        "Solids",
        "Chloramines",
        "Sulfate",
        "Conductivity",
        "Organic_carbon",
        "Trihalomethanes",
        "Turbidity",
    ],
)

test_df["Potability"] = y_test.values

# ==========================
# Load Trained FT-Transformer Model
# ==========================
model = TabularModel.load_model("saved_models/ft_transformer")

# ==========================
# Make Predictions
# ==========================
pred = model.predict(test_df)

# Get predicted class labels
y_pred = pred["Potability_prediction"]

# ==========================
# Evaluation Metrics
# ==========================
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
f1 = f1_score(y_test, y_pred)

print("\n========== FT-TRANSFORMER RESULTS ==========\n")

print(f"Accuracy : {accuracy:.4f}")
print(f"Precision: {precision:.4f}")
print(f"Recall   : {recall:.4f}")
print(f"F1 Score : {f1:.4f}")

print("\n========== Confusion Matrix ==========\n")
print(confusion_matrix(y_test, y_pred))

print("\n========== Classification Report ==========\n")
print(classification_report(y_test, y_pred))
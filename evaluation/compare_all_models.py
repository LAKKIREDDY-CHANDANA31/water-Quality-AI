import pandas as pd
import os

# ==============================
# Results from previous evaluations
# ==============================

results = [
    {
        "Model": "DNN",
        "Accuracy": 66.62,
        "Precision": 57.14,
        "Recall": 40.98,
        "F1 Score": 47.73
    },
    {
        "Model": "TabNet",
        "Accuracy": 61.13,
        "Precision": 46.86,
        "Recall": 33.61,
        "F1 Score": 39.14
    },
    {
        "Model": "FT-Transformer",
        "Accuracy": 66.62,
        "Precision": 58.62,
        "Recall": 34.84,
        "F1 Score": 43.70
    }
]

# ==============================
# Create DataFrame
# ==============================

df = pd.DataFrame(results)

# ==============================
# Find Best Model
# ==============================

best_model = df.loc[df["F1 Score"].idxmax(), "Model"]

# ==============================
# Print Comparison
# ==============================

print("\n" + "=" * 65)
print("         WATER QUALITY MODEL COMPARISON")
print("=" * 65)

print(df.to_string(index=False))

print("\n" + "=" * 65)
print("Best Model :", best_model)
print("=" * 65)

# ==============================
# Save Results
# ==============================

os.makedirs("results", exist_ok=True)

df.to_csv("results/model_comparison.csv", index=False)

print("\nComparison report saved successfully!")
print("Location: results/model_comparison.csv")
import pandas as pd

def load_and_clean_data():

    # Load dataset
    data = pd.read_csv("dataset/water_potability.csv")

    print("Missing Values Before Cleaning")
    print(data.isnull().sum())

    # Fill missing values with column mean
    data["ph"] = data["ph"].fillna(data["ph"].mean())
    data["Sulfate"] = data["Sulfate"].fillna(data["Sulfate"].mean())
    data["Trihalomethanes"] = data["Trihalomethanes"].fillna(data["Trihalomethanes"].mean())

    print("\nMissing Values After Cleaning")
    print(data.isnull().sum())

    return data
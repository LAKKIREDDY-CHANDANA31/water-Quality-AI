from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
import joblib
import os


def split_and_scale_data(data):
    """
    Splits the dataset into training and testing sets,
    scales the features, and saves the scaler.
    """

    # Features and Target
    X = data.drop("Potability", axis=1)
    y = data["Potability"]

    # Train-Test Split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    # Feature Scaling
    scaler = StandardScaler()

    X_train = scaler.fit_transform(X_train)
    X_test = scaler.transform(X_test)

    # Create saved_models folder if it doesn't exist
    os.makedirs("saved_models", exist_ok=True)

    # Save scaler
    joblib.dump(scaler, "saved_models/scaler.pkl")

    print("Scaler saved successfully!")

    print("Training Data Shape :", X_train.shape)
    print("Testing Data Shape  :", X_test.shape)

    return X_train, X_test, y_train, y_test
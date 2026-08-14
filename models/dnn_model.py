from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense


def build_dnn_model():

    model = Sequential()

    # Input Layer
    model.add(Dense(64, activation="relu", input_shape=(9,)))

    # Hidden Layer 1
    model.add(Dense(32, activation="relu"))

    # Hidden Layer 2
    model.add(Dense(16, activation="relu"))

    # Output Layer
    model.add(Dense(1, activation="sigmoid"))

    # Compile the model
    model.compile(
        optimizer="adam",
        loss="binary_crossentropy",
        metrics=["accuracy"]
    )

    return model
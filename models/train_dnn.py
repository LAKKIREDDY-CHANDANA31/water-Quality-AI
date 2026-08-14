import os

from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data
from models.dnn_model import build_dnn_model

from tensorflow.keras.callbacks import EarlyStopping, ReduceLROnPlateau


# ============================================================
# 1. LOAD AND CLEAN DATA
# ============================================================

print("=" * 60)
print("LOADING AND CLEANING DATA")
print("=" * 60)

data = load_and_clean_data()

print("Dataset loaded successfully.")


# ============================================================
# 2. SPLIT AND SCALE DATA
# ============================================================

print("\n" + "=" * 60)
print("SPLITTING AND SCALING DATA")
print("=" * 60)

X_train, X_test, y_train, y_test = split_and_scale_data(data)

print("Training samples :", len(X_train))
print("Testing samples  :", len(X_test))


# ============================================================
# 3. BUILD DNN MODEL
# ============================================================

print("\n" + "=" * 60)
print("BUILDING DNN MODEL")
print("=" * 60)

model = build_dnn_model()

model.summary()


# ============================================================
# 4. CALLBACKS
# ============================================================

early_stopping = EarlyStopping(
    monitor="val_loss",
    patience=10,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=4,
    min_lr=0.00001,
    verbose=1
)


# ============================================================
# 5. TRAIN MODEL
# ============================================================

print("\n" + "=" * 60)
print("STARTING DNN TRAINING")
print("=" * 60)

history = model.fit(
    X_train,
    y_train,
    epochs=100,
    batch_size=32,
    validation_split=0.2,
    callbacks=[
        early_stopping,
        reduce_lr
    ],
    verbose=1
)


# ============================================================
# 6. TRAINING RESULTS
# ============================================================

best_train_accuracy = max(history.history["accuracy"])
best_val_accuracy = max(history.history["val_accuracy"])

print("\n" + "=" * 60)
print("TRAINING RESULTS")
print("=" * 60)

print(
    f"Best Training Accuracy   : "
    f"{best_train_accuracy * 100:.2f}%"
)

print(
    f"Best Validation Accuracy : "
    f"{best_val_accuracy * 100:.2f}%"
)


# ============================================================
# 7. TEST MODEL
# ============================================================

print("\n" + "=" * 60)
print("TESTING MODEL")
print("=" * 60)

test_loss, test_accuracy = model.evaluate(
    X_test,
    y_test,
    verbose=1
)

print(
    f"\nTest Accuracy : "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Test Loss     : "
    f"{test_loss:.4f}"
)


# ============================================================
# 8. SAVE MODEL
# ============================================================

os.makedirs("saved_models", exist_ok=True)

model.save(
    "saved_models/dnn_model.keras"
)

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 60)

print(
    "Location: saved_models/dnn_model.keras"
)
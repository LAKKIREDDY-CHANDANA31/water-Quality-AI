import os
import joblib
import numpy as np
import tensorflow as tf

from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report
)

from preprocessing.clean_data import load_and_clean_data
from preprocessing.split_data import split_and_scale_data

from models.ft_transformer import FTTransformer


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
# 3. CONVERT DATA TO NUMPY
# ============================================================

X_train = np.asarray(
    X_train,
    dtype=np.float32
)

X_test = np.asarray(
    X_test,
    dtype=np.float32
)

y_train = np.asarray(
    y_train,
    dtype=np.float32
)

y_test = np.asarray(
    y_test,
    dtype=np.float32
)


# ============================================================
# 4. BUILD FT-TRANSFORMER MODEL
# ============================================================

print("\n" + "=" * 60)
print("BUILDING FT-TRANSFORMER MODEL")
print("=" * 60)

model = FTTransformer(
    num_features=X_train.shape[1],
    d_token=64,
    num_heads=8,
    num_layers=3,
    dropout=0.2
)

# Build model
model.build(
    (None, X_train.shape[1])
)

model.summary()


# ============================================================
# 5. COMPILE MODEL
# ============================================================

print("\n" + "=" * 60)
print("COMPILING FT-TRANSFORMER")
print("=" * 60)

model.compile(
    optimizer=tf.keras.optimizers.Adam(
        learning_rate=0.001
    ),
    loss="binary_crossentropy",
    metrics=[
        "accuracy"
    ]
)


# ============================================================
# 6. CALLBACKS
# ============================================================

early_stopping = tf.keras.callbacks.EarlyStopping(
    monitor="val_loss",
    patience=15,
    restore_best_weights=True,
    verbose=1
)

reduce_lr = tf.keras.callbacks.ReduceLROnPlateau(
    monitor="val_loss",
    factor=0.5,
    patience=5,
    min_lr=0.00001,
    verbose=1
)


# ============================================================
# 7. TRAIN MODEL
# ============================================================

print("\n" + "=" * 60)
print("STARTING FT-TRANSFORMER TRAINING")
print("=" * 60)

history = model.fit(
    X_train,
    y_train,

    validation_split=0.2,

    epochs=100,

    batch_size=32,

    callbacks=[
        early_stopping,
        reduce_lr
    ],

    verbose=1
)


# ============================================================
# 8. TRAINING PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("CALCULATING TRAINING RESULTS")
print("=" * 60)

train_probability = model.predict(
    X_train,
    verbose=0
).ravel()

train_predictions = (
    train_probability >= 0.5
).astype(int)

train_accuracy = accuracy_score(
    y_train,
    train_predictions
)


# ============================================================
# 9. TESTING PREDICTIONS
# ============================================================

print("\n" + "=" * 60)
print("TESTING FT-TRANSFORMER MODEL")
print("=" * 60)

test_probability = model.predict(
    X_test,
    verbose=0
).ravel()

test_predictions = (
    test_probability >= 0.5
).astype(int)


# ============================================================
# 10. CALCULATE TEST METRICS
# ============================================================

test_accuracy = accuracy_score(
    y_test,
    test_predictions
)

test_precision = precision_score(
    y_test,
    test_predictions,
    zero_division=0
)

test_recall = recall_score(
    y_test,
    test_predictions,
    zero_division=0
)

test_f1 = f1_score(
    y_test,
    test_predictions,
    zero_division=0
)


# ============================================================
# 11. PRINT RESULTS
# ============================================================

print("\n" + "=" * 60)
print("FT-TRANSFORMER RESULTS")
print("=" * 60)

print(
    f"Training Accuracy : "
    f"{train_accuracy * 100:.2f}%"
)

print(
    f"Test Accuracy     : "
    f"{test_accuracy * 100:.2f}%"
)

print(
    f"Precision         : "
    f"{test_precision * 100:.2f}%"
)

print(
    f"Recall            : "
    f"{test_recall * 100:.2f}%"
)

print(
    f"F1 Score          : "
    f"{test_f1 * 100:.2f}%"
)


# ============================================================
# 12. CLASSIFICATION REPORT
# ============================================================

print("\nClassification Report")
print("=" * 60)

print(
    classification_report(
        y_test,
        test_predictions,
        target_names=[
            "Not Potable",
            "Potable"
        ],
        zero_division=0
    )
)


# ============================================================
# 13. SAVE MODEL
# ============================================================

os.makedirs(
    "saved_models",
    exist_ok=True
)

model.save(
    "saved_models/ft_transformer_model.keras"
)

print("\n" + "=" * 60)
print("MODEL SAVED SUCCESSFULLY")
print("=" * 60)

print(
    "Location: "
    "saved_models/ft_transformer_model.keras"
)
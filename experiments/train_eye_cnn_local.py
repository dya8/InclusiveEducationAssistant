import os
import cv2
import numpy as np
from sklearn.model_selection import train_test_split
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

DATASET = "data/CEW"
IMG_SIZE = 24

def preprocess(path):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        return None
    img = cv2.resize(img, (IMG_SIZE, IMG_SIZE))
    clahe = cv2.createCLAHE(2.0, (8, 8))
    img = clahe.apply(img)
    return img.astype("float32") / 255.0

X, y = [], []

for label, cls in enumerate(["open", "closed"]):
    folder = os.path.join(DATASET, cls)
    for f in os.listdir(folder):
        img = preprocess(os.path.join(folder, f))
        if img is not None:
            X.append(img)
            y.append(label)

X = np.array(X).reshape(-1, 24, 24, 1)
y = np.array(y)

Xtr, Xte, ytr, yte = train_test_split(
    X, y, test_size=0.2, stratify=y, random_state=42
)

model = Sequential([
    Conv2D(32, (3,3), activation='relu', input_shape=(24,24,1)),
    MaxPooling2D(2,2),
    Conv2D(64, (3,3), activation='relu'),
    MaxPooling2D(2,2),
    Flatten(),
    Dense(64, activation='relu'),
    Dropout(0.5),
    Dense(1, activation='sigmoid')
])

model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

model.fit(
    Xtr, ytr,
    validation_data=(Xte, yte),
    epochs=8,
    batch_size=64
)

os.makedirs("assets/models", exist_ok=True)
model.save("assets/models/eye_closed_model.keras")
print("MODEL SAVED → assets/models/eye_closed_model.keras")

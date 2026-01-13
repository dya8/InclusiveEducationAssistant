from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Conv2D, MaxPooling2D, Flatten, Dense, Dropout

def build_eye_state_model():
    model = Sequential([
        Conv2D(
            32, (3, 3),
            activation="relu",
            input_shape=(24, 24, 1)
        ),
        MaxPooling2D(pool_size=(2, 2)),

        Conv2D(
            64, (3, 3),
            activation="relu"
        ),
        MaxPooling2D(pool_size=(2, 2)),

        Flatten(),                 # → 1024
        Dense(64, activation="relu"),
        Dropout(0.5),
        Dense(1, activation="sigmoid")
    ])

    return model

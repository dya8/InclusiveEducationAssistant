import cv2
import numpy as np
import tensorflow as tf

class EyeStateCNN:
    def __init__(self, model_path="assets/models/eye_closed_model.keras"):
        self.model = tf.keras.models.load_model(model_path)

        self.clahe = cv2.createCLAHE(
            clipLimit=2.0,
            tileGridSize=(8, 8)
        )

        self.CLOSED_THRESHOLD = 0.85

    def preprocess(self, eye_img):
        if len(eye_img.shape) == 3:
            eye_img = cv2.cvtColor(eye_img, cv2.COLOR_BGR2GRAY)

        eye_img = cv2.resize(eye_img, (24, 24))
        eye_img = self.clahe.apply(eye_img)
        eye_img = eye_img.astype(np.float32) / 255.0
        eye_img = eye_img.reshape(1, 24, 24, 1)

        return eye_img

    def is_closed(self, eye_img):
        x = self.preprocess(eye_img)
        p = float(self.model.predict(x, verbose=0)[0][0])
        return p > 0.5


    
    def predict_prob(self, eye_img):
        x = self.preprocess(eye_img)
        return float(self.model.predict(x, verbose=0)[0][0])


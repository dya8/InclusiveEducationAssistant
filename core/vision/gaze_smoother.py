import cv2
import numpy as np

class GazeKalman:
    def __init__(self):
        # State: [x, y, dx, dy]
        self.kf = cv2.KalmanFilter(4, 2)

        self.kf.transitionMatrix = np.array([
            [1, 0, 1, 0],
            [0, 1, 0, 1],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ], dtype=np.float32)

        self.kf.measurementMatrix = np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0]
        ], dtype=np.float32)

        # Tune these two for smoothness vs responsiveness
        self.kf.processNoiseCov = np.eye(4, dtype=np.float32) * 0.002
        self.kf.measurementNoiseCov = np.eye(2, dtype=np.float32) * 0.30

        self.kf.errorCovPost = np.eye(4, dtype=np.float32)
        self.initialized = False

    def smooth(self, x, y):
        measurement = np.array([[np.float32(x)], [np.float32(y)]])

        if not self.initialized:
            self.kf.statePost = np.array([[x], [y], [0], [0]], dtype=np.float32)
            self.initialized = True

        self.kf.predict()
        filtered = self.kf.correct(measurement)

        return float(filtered[0]), float(filtered[1])

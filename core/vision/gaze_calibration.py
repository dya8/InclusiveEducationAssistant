import numpy as np

class GazeCalibration:
    def __init__(self):
        self.data = {
            "CENTER": [],
            "LEFT": [],
            "RIGHT": [],
            "UP": [],
            "DOWN": []
        }
        self.calibrated = False

        self.center_x = None
        self.center_y = None
        self.left_x = None
        self.right_x = None
        self.up_y = None
        self.down_y = None

    def add_sample(self, label, gx, gy):
        if label in self.data:
            self.data[label].append((gx, gy))

    def finalize(self):
        self.center_x = np.mean([x for x, _ in self.data["CENTER"]])
        self.center_y = np.mean([y for _, y in self.data["CENTER"]])

        self.left_x = np.mean([x for x, _ in self.data["LEFT"]])
        self.right_x = np.mean([x for x, _ in self.data["RIGHT"]])
        self.up_y = np.mean([y for _, y in self.data["UP"]])
        self.down_y = np.mean([y for _, y in self.data["DOWN"]])

        self.calibrated = True

    def map(self, gx, gy):
        if not self.calibrated:
            return None

        x = (gx - self.left_x) / (self.right_x - self.left_x)
        y = (gy - self.up_y) / (self.down_y - self.up_y)

        x = min(max(x, 0.0), 1.0)
        y = min(max(y, 0.0), 1.0)

        return x, y

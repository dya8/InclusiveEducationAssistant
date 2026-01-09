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
        # Raw means
        self.center_x = np.mean([x for x, _ in self.data["CENTER"]])
        self.center_y = np.mean([y for _, y in self.data["CENTER"]])

        self.left_x = np.mean([x for x, _ in self.data["LEFT"]])
        self.right_x = np.mean([x for x, _ in self.data["RIGHT"]])
        self.up_y = np.mean([y for _, y in self.data["UP"]])
        self.down_y = np.mean([y for _, y in self.data["DOWN"]])

        # ---------- SAFETY: enforce ordering ----------
        if self.left_x > self.right_x:
            self.left_x, self.right_x = self.right_x, self.left_x

        if self.up_y > self.down_y:
            self.up_y, self.down_y = self.down_y, self.up_y

        # ---------- SAFETY: minimum range ----------
        if abs(self.right_x - self.left_x) < 0.02:
            raise ValueError("Calibration X range too small")

        if abs(self.down_y - self.up_y) < 0.02:
            # widen range slightly instead of failing hard
            mid = (self.up_y + self.down_y) / 2
            self.up_y = mid - 0.01
            self.down_y = mid + 0.01

        # ---------- SCREEN-SPACE CENTER ----------
        self.center_screen_x = (self.center_x - self.left_x) / (self.right_x - self.left_x)
        self.center_screen_y = 1.0 - ((self.center_y - self.up_y) / (self.down_y - self.up_y))

        self.calibrated = True


    def map(self, gx, gy):
        if not self.calibrated:
            return None

        # X (invert once)
        x = 1.0 - ((gx - self.left_x) / (self.right_x - self.left_x))

        # Y (already correct)
        y = (gy - self.up_y) / (self.down_y - self.up_y)
        y = 1.0 - y

        x = min(max(x, 0.0), 1.0)
        y = min(max(y, 0.0), 1.0)

        if not np.isfinite(x) or not np.isfinite(y):
            return None

        return x, y

import time
from core.input.input_events import BlinkType

class BlinkDetector:
    def __init__(self, eye_cnn):
        self.eye_cnn = eye_cnn

        self.closed_since = None
        self.last_blink_time = 0

        self.SINGLE_MAX = 0.35
        self.LONG_MIN = 0.6
        self.COOLDOWN = 0.5

    def update(self, left_eye_img, right_eye_img):
        now = time.time()

        left_p = self.eye_cnn.predict_prob(left_eye_img)
        right_p = self.eye_cnn.predict_prob(right_eye_img)

        p_avg = (left_p + right_p) / 2
        closed = p_avg > 0.65

        if closed:
            if self.closed_since is None:
                self.closed_since = now
            return BlinkType.NONE

        # eye opened
        if self.closed_since is not None:
            duration = now - self.closed_since
            self.closed_since = None

            if now - self.last_blink_time < self.COOLDOWN:
                return BlinkType.NONE

            self.last_blink_time = now

            if duration < self.SINGLE_MAX:
                return BlinkType.SINGLE
            if duration >= self.LONG_MIN:
                return BlinkType.LONG

        return BlinkType.NONE

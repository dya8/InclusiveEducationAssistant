import math
import time
from core.input.input_events import BlinkType

class BlinkDetector:
    def __init__(self):
        self.EAR_THRESHOLD = 0.22
        self.LONG_BLINK_TIME = 0.8  # seconds

        self.eye_closed = False
        self.blink_start_time = None

    def _euclidean(self, p1, p2):
        return math.dist(p1, p2)

    def compute_ear(self, eye_points):
        """
        eye_points: list of 6 (x, y) tuples
        """
        p1, p2, p3, p4, p5, p6 = eye_points

        vertical = (
            self._euclidean(p2, p6) +
            self._euclidean(p3, p5)
        )
        horizontal = 2.0 * self._euclidean(p1, p4)

        if horizontal == 0:
            return 0.0

        return vertical / horizontal

    def update(self, left_eye, right_eye):
        """
        Called every frame.
        Returns BlinkType or BlinkType.NONE
        """
        left_ear = self.compute_ear(left_eye)
        right_ear = self.compute_ear(right_eye)
        ear = (left_ear + right_ear) / 2.0

        current_time = time.time()

        # ---- EYE CLOSED ----
        if ear < self.EAR_THRESHOLD:
            if not self.eye_closed:
                self.eye_closed = True
                self.blink_start_time = current_time
            return BlinkType.NONE

        # ---- EYE OPEN ----
        if self.eye_closed:
            duration = current_time - self.blink_start_time
            self.eye_closed = False
            self.blink_start_time = None

            if duration >= self.LONG_BLINK_TIME:
                return BlinkType.LONG
            else:
                return BlinkType.SINGLE

        return BlinkType.NONE

import math
from core.input.input_events import BlinkType

class BlinkDetector:
    def __init__(self, eye_cnn):
        self.eye_cnn = eye_cnn

        self.closed_frames = 0
        self.cooldown = 0

        # Frame thresholds (~30 FPS)
        self.SINGLE_MIN = 2
        self.SINGLE_MAX = 5
        self.LONG_MIN = 10

        self.COOLDOWN_FRAMES = 6

        # EAR hysteresis thresholds (TUNED FOR YOUR LOGS)
        self.EAR_CLOSED_TH = 0.18   # must go BELOW this to count as closed
        self.EAR_OPEN_TH   = 0.23   # must go ABOVE this to reopen
        self.eyes_closed_state = False


    # -----------------------------------------

    def update(self, left_eye_img, right_eye_img, left_eye_pts, right_eye_pts):
        if self.cooldown > 0:
            self.cooldown -= 1
            return BlinkType.NONE

        # CNN decision
        left_closed = self.eye_cnn.is_closed(left_eye_img)
        right_closed = self.eye_cnn.is_closed(right_eye_img)

        # EAR decision
        ear = self._compute_ear(left_eye_pts, right_eye_pts)
        if ear < self.EAR_CLOSED_TH:
            self.eyes_closed_state = True
        elif ear > self.EAR_OPEN_TH:
            self.eyes_closed_state = False
    # else: keep previous state

        ear_closed = self.eyes_closed_state

    # Debug (THIS is the correct place)
        '''print(
            f"L={left_closed} R={right_closed} "
            f"EAR={ear:.3f} EAR_closed={ear_closed} "
            f"closed_frames={self.closed_frames}"
        )'''

        eyes_closed = left_closed and right_closed and ear_closed

        if eyes_closed:
            self.closed_frames += 1
            return BlinkType.NONE

        if self.closed_frames > 0:
            frames = self.closed_frames
            self.closed_frames = 0
            self.cooldown = self.COOLDOWN_FRAMES

            #print(f"closed_frames={frames}")

            if self.SINGLE_MIN <= frames <= self.SINGLE_MAX:
                return BlinkType.SINGLE
            if frames >= self.LONG_MIN:
                return BlinkType.LONG

        return BlinkType.NONE

    # -----------------------------------------
    # EAR helpers

    def _compute_ear(self, left_eye, right_eye):
        return (self._ear(left_eye) + self._ear(right_eye)) / 2.0

    def _ear(self, eye):
        A = self._dist(eye[1], eye[5])
        B = self._dist(eye[2], eye[4])
        C = self._dist(eye[0], eye[3])
        return (A + B) / (2.0 * C + 1e-6)

    def _dist(self, p1, p2):
        return math.hypot(p1[0] - p2[0], p1[1] - p2[1])

from pylsl import StreamInlet, resolve_stream


class EOGDetector:
    def __init__(self):
        print("EOG connecting...")

        try:
            streams = resolve_stream()

            if len(streams) == 0:
                print("⚠️ No EOG device found. Running without EOG.")
                self.inlet = None
                self.enabled = False
                return

            self.inlet = StreamInlet(streams[0])
            self.enabled = True

        except Exception as e:
            print("⚠️ EOG init failed:", e)
            self.inlet = None
            self.enabled = False

        self.baseline_h = None
        self.baseline_v = None

    def get_action(self):
        if not getattr(self, "enabled", False):
            return None
        if not self.enabled:
            return None
        sample, _ = self.inlet.pull_sample(timeout=0.0)

        if sample is None:
            return None

        h = sample[0]
        v = sample[1]

        # ---------- BETTER BASELINE (average first few samples) ----------
        if self.baseline_h is None:
            if not hasattr(self, "calib_samples"):
                self.calib_samples = []

            self.calib_samples.append((h, v))

            # collect ~20 samples (~0.04 sec)
            if len(self.calib_samples) < 20:
                return None

            # average baseline
            self.baseline_h = sum(s[0] for s in self.calib_samples) / len(self.calib_samples)
            self.baseline_v = sum(s[1] for s in self.calib_samples) / len(self.calib_samples)

            print("EOG calibrated")
            return None

        dx = -(h - self.baseline_h)
        dy = v - self.baseline_v

        # ---------- DEADZONE (kills jitter) ----------
        if abs(dx) < 15:
            dx = 0
        if abs(dy) < 15:
            dy = 0

        # ---------- HORIZONTAL ----------
        if dx > 30:
            return "RIGHT"
        elif dx < -30:
            return "LEFT"

        # ---------- BLINK ----------
        if dy > 50 and abs(dx) < 20:
            return "BLINK"

        return None
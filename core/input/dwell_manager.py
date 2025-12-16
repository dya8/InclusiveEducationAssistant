import time

class DwellManager:
    def __init__(self, dwell_time=1.2):
        self.dwell_time = dwell_time
        self.current = None
        self.start_time = None

    def update(self, widget):
        if widget != self.current:
            self.current = widget
            self.start_time = time.time()
            return 0.0, False

        elapsed = time.time() - self.start_time
        progress = min(elapsed / self.dwell_time, 1.0)
        selected = progress >= 1.0
        return progress, selected

    def reset(self):
        self.current = None
        self.start_time = None

from core.input.input_events import GazeDirection
class GazeEstimator:
    """
    Outputs raw normalized gaze (gx, gy) in approx [0, 1]
    No thresholds. No calibration. No enums.
    """

    def _eye_bounds(self, eye):
        xs = [p[0] for p in eye]
        ys = [p[1] for p in eye]
        return min(xs), max(xs), min(ys), max(ys)

    def estimate(self, left_eye, right_eye, left_iris, right_iris):
        # Average iris center
        iris_x = (left_iris[0] + right_iris[0]) / 2
        iris_y = (left_iris[1] + right_iris[1]) / 2

        # Eye bounds
        lx_min, lx_max, ly_min, ly_max = self._eye_bounds(left_eye)
        rx_min, rx_max, ry_min, ry_max = self._eye_bounds(right_eye)

        eye_min_x = (lx_min + rx_min) / 2
        eye_max_x = (lx_max + rx_max) / 2
        eye_min_y = (ly_min + ry_min) / 2
        eye_max_y = (ly_max + ry_max) / 2

        # Normalize iris position within eye region
        gx = (iris_x - eye_min_x) / max((eye_max_x - eye_min_x), 1)
        gy = (iris_y - eye_min_y) / max((eye_max_y - eye_min_y), 1)

        # Clamp for safety
        gx = min(max(gx, 0.0), 1.0)
        gy = min(max(gy, 0.0), 1.0)

        return gx, gy

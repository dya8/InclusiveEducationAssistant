import cv2
import mediapipe as mp
import numpy as np


class FaceMeshDetector:
    def __init__(self):
        self.mp_face_mesh = mp.solutions.face_mesh
        self.face_mesh = self.mp_face_mesh.FaceMesh(
            static_image_mode=False,
            max_num_faces=1,
            refine_landmarks=True,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )

        # Eye landmarks (MediaPipe standard)
        self.LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]

        # Iris landmarks
        self.LEFT_IRIS_IDX = [468, 469, 470, 471]
        self.RIGHT_IRIS_IDX = [472, 473, 474, 475]

        # FIXED crop size (critical for CNN stability)
        self.EYE_CROP_W = 48
        self.EYE_CROP_H = 32

    # -------------------------------------------------

    def _to_pixel(self, landmark, w, h):
        return int(landmark.x * w), int(landmark.y * h)

    def _eye_center(self, points):
        xs = [p[0] for p in points]
        ys = [p[1] for p in points]
        return int(np.mean(xs)), int(np.mean(ys))
    def _center(self, points):
        x = sum(p[0] for p in points) / len(points)
        y = sum(p[1] for p in points) / len(points)
        return (x, y)

    def _crop_eye(self, frame, center):
        cx, cy = center
        h, w, _ = frame.shape

        x_min = max(cx - self.EYE_CROP_W // 2, 0)
        x_max = min(cx + self.EYE_CROP_W // 2, w)

        y_min = max(cy - self.EYE_CROP_H // 2, 0)
        y_max = min(cy + self.EYE_CROP_H // 2, h)

        if x_max <= x_min or y_max <= y_min:
            return None

        return frame[y_min:y_max, x_min:x_max]

    # -------------------------------------------------

    def get_eye_landmarks(self, frame):
        if frame is None:
            return None

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark

        left_eye = [self._to_pixel(landmarks[i], w, h) for i in self.LEFT_EYE_IDX]
        right_eye = [self._to_pixel(landmarks[i], w, h) for i in self.RIGHT_EYE_IDX]

        left_iris_pts = [
            self._to_pixel(landmarks[i], w, h)
            for i in self.LEFT_IRIS_IDX
        ]
        right_iris_pts = [
            self._to_pixel(landmarks[i], w, h)
            for i in self.RIGHT_IRIS_IDX
        ]

        left_iris = self._center(left_iris_pts)
        right_iris = self._center(right_iris_pts)


        # 🔒 FIXED CENTER-BASED CROPPING
        left_center = self._eye_center(left_eye)
        right_center = self._eye_center(right_eye)

        left_eye_img = self._crop_eye(frame, left_center)
        right_eye_img = self._crop_eye(frame, right_center)

        if left_eye_img is None or right_eye_img is None:
            return None

        return {
            "left_eye": left_eye,
            "right_eye": right_eye,
            "left_eye_img": left_eye_img,
            "right_eye_img": right_eye_img,
            "left_iris": left_iris,
            "right_iris": right_iris
        }

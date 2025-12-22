import cv2
import mediapipe as mp

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

        # EAR-compatible eye landmark order
        self.LEFT_EYE_IDX = [33, 160, 158, 133, 153, 144]
        self.RIGHT_EYE_IDX = [362, 385, 387, 263, 373, 380]
        # Iris landmark indices
        self.LEFT_IRIS_IDX = [468, 469, 470, 471]
        self.RIGHT_IRIS_IDX = [472, 473, 474, 475]

    def get_eye_landmarks(self, frame):
        if frame is None:
            return None

        h, w, _ = frame.shape
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = self.face_mesh.process(rgb)

        if not results.multi_face_landmarks:
            return None

        landmarks = results.multi_face_landmarks[0].landmark

        def to_pixel(idx):
            lm = landmarks[idx]
            return (int(lm.x * w), int(lm.y * h))

        left_eye = [to_pixel(i) for i in self.LEFT_EYE_IDX]
        right_eye = [to_pixel(i) for i in self.RIGHT_EYE_IDX]
        left_iris = [to_pixel(i) for i in self.LEFT_IRIS_IDX]
        right_iris = [to_pixel(i) for i in self.RIGHT_IRIS_IDX]
        
        def center(points):
            x = sum(p[0] for p in points) / len(points)
            y = sum(p[1] for p in points) / len(points)
            return (x, y)

        return {
            "left_eye": left_eye,
            "right_eye": right_eye,
            "left_iris": center(left_iris),
            "right_iris": center(right_iris)
        }

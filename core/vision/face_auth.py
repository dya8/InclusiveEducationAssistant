# core/vision/face_auth.py

import os
import face_recognition
import cv2
import numpy as np


class FaceAuthenticator:
    def __init__(self, faces_dir: str = "assets/faces", tolerance: float = 0.45):
        self.faces_dir = faces_dir
        self.tolerance = tolerance
        self.known_encodings = []
        self.known_user_ids = []
        self._load_known_faces()

    def _load_known_faces(self):
        """
        Loads all face encodings from assets/faces/<user_id>/*.jpg
        """
        if not os.path.exists(self.faces_dir):
            print("[FaceAuth] Faces directory not found.")
            return

        for user_id in os.listdir(self.faces_dir):
            user_path = os.path.join(self.faces_dir, user_id)
            if not os.path.isdir(user_path):
                continue

            for img_name in os.listdir(user_path):
                img_path = os.path.join(user_path, img_name)

                try:
                    image = face_recognition.load_image_file(img_path)
                    encodings = face_recognition.face_encodings(image)

                    if encodings:
                        self.known_encodings.append(encodings[0])
                        self.known_user_ids.append(user_id)
                except Exception as e:
                    print(f"[FaceAuth] Failed loading {img_path}: {e}")

        print(f"[FaceAuth] Loaded {len(self.known_encodings)} face encodings.")

    def authenticate(self, frame) -> str | None:
        """
        Input: BGR frame from OpenCV
        Output:
            - user_id (str) if face recognized
            - None if unknown or no face detected
        """

        if frame is None:
            return None

        # Convert BGR → RGB
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        face_locations = face_recognition.face_locations(rgb_frame)
        if not face_locations:
            return None

        face_encodings = face_recognition.face_encodings(
            rgb_frame, face_locations
        )

        if not face_encodings:
            return None

        candidate_encoding = face_encodings[0]

        distances = face_recognition.face_distance(
            self.known_encodings, candidate_encoding
        )

        if len(distances) == 0:
            return None

        best_match_idx = np.argmin(distances)

        if distances[best_match_idx] <= self.tolerance:
            return self.known_user_ids[best_match_idx]

        return None
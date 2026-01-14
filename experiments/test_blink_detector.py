import cv2
from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.vision.blink_detector import BlinkDetector
from core.ml.eye_state_cnn import EyeStateCNN

print("BLINK DETECTOR TEST STARTED")
print("Blink normally. Press ESC to exit.")

camera = CameraManager()
camera.start()

face_mesh = FaceMeshDetector()
eye_cnn = EyeStateCNN("assets/models/eye_closed_model.h5")
blink = BlinkDetector(eye_cnn)

while True:
    frame = camera.get_frame()
    if frame is None:
        continue

    eyes = face_mesh.get_eye_landmarks(frame)
    if not eyes:
        continue

    result = blink.update(
        eyes["left_eye_img"],
        eyes["right_eye_img"],
        eyes["left_eye_pts"],
        eyes["right_eye_pts"]
        )
    print(result)

    if cv2.waitKey(1) & 0xFF == 27:
        break

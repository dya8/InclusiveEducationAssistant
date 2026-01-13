import cv2
from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.vision.blink_detector import BlinkDetector
from core.ml.eye_state_cnn import EyeStateCNN
print("BLINK DETECTOR TEST STARTED")
print("Blink normally. Press ESC to exit.")

cam = CameraManager()
cam.start()

mesh = FaceMeshDetector()
eye_cnn = EyeStateCNN("assets/models/eye_closed_model.keras")
blink = BlinkDetector(eye_cnn)

while True:
    frame = cam.get_frame()
    if frame is None:
        continue

    eyes = mesh.get_eye_landmarks(frame)
    if eyes:
        result = blink.update(
            eyes["left_eye_img"],
            eyes["right_eye_img"]
        )
        print(result)

    cv2.imshow("Blink Test", frame)
    if cv2.waitKey(1) == 27:
        break

cam.stop()
cv2.destroyAllWindows()

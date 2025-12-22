import cv2
import sys
import os

ROOT_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.insert(0, ROOT_DIR)

from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.vision.blink_detector import BlinkDetector

cam = CameraManager()
cam.start()

mesh = FaceMeshDetector()
blink = BlinkDetector()

while True:
    frame = cam.get_frame()
    if frame is None:
        continue

    eyes = mesh.get_eye_landmarks(frame)

    if eyes:
        blink_type = blink.update(
            eyes["left_eye"],
            eyes["right_eye"]
        )

        if blink_type.name != "NONE":
            print("BLINK:", blink_type.name)

    cv2.imshow("Blink Debug", frame)

    if cv2.waitKey(1) == 27:
        break

cam.stop()
cv2.destroyAllWindows()

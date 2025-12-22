import sys, os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import cv2
from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.vision.gaze_estimator import GazeEstimator

cam = CameraManager()
cam.start()

mesh = FaceMeshDetector()
gaze = GazeEstimator()

while True:
    frame = cam.get_frame()
    if frame is None:
        continue

    eyes = mesh.get_eye_landmarks(frame)

    if eyes:
        direction = gaze.estimate(
            eyes["left_eye"],
            eyes["right_eye"],
            eyes["left_iris"],
            eyes["right_iris"]
        )
        print(direction.name)

    cv2.imshow("Gaze Debug", frame)
    
    if cv2.waitKey(1) == 27:
        break

cam.stop()
cv2.destroyAllWindows()

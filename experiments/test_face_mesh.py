import cv2
from core.vision.face_mesh import FaceMeshDetector
from core.vision.camera import CameraManager

cam = CameraManager()
cam.start()

mesh = FaceMeshDetector()

while True:
    frame = cam.get_frame()
    if frame is None:
        continue

    eyes = mesh.get_eye_landmarks(frame)

    if eyes:
        cv2.imshow("Left Eye", eyes["left_eye_img"])
        cv2.imshow("Right Eye", eyes["right_eye_img"])

    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break

cam.stop()
cv2.destroyAllWindows()

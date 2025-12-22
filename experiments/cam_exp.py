import cv2
from core.vision.camera import CameraManager

cam = CameraManager()
cam.start()

while True:
    frame = cam.get_frame()
    if frame is not None:
        cv2.imshow("debug", frame)

    if cv2.waitKey(1) == 27:
        break

cam.stop()
cv2.destroyAllWindows()

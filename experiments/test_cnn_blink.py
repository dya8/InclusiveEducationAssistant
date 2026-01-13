import cv2
from core.vision.camera import CameraManager
from core.vision.face_mesh import FaceMeshDetector
from core.ml.eye_state_cnn import EyeStateCNN

# ---- INIT ----
cam = CameraManager()
cam.start()

mesh = FaceMeshDetector()
eye_cnn = EyeStateCNN("assets/models/eye_closed_inference_model.h5")

print("CNN BLINK TEST STARTED")
print("Press ESC to exit")

# ---- LOOP ----
while True:
    frame = cam.get_frame()
    if frame is None:
        continue

    eyes = mesh.get_eye_landmarks(frame)
    if not eyes:
        cv2.imshow("Frame", frame)
        if cv2.waitKey(1) == 27:
            break
        continue

    left_closed = eye_cnn.is_closed(eyes["left_eye_img"])
    right_closed = eye_cnn.is_closed(eyes["right_eye_img"])

    status = "CLOSED" if (left_closed and right_closed) else "OPEN"

    print(status)

    # Debug visuals
    cv2.imshow("Left Eye", eyes["left_eye_img"])
    cv2.imshow("Right Eye", eyes["right_eye_img"])
    cv2.imshow("Frame", frame)

    if cv2.waitKey(1) == 27:
        break

cam.stop()
cv2.destroyAllWindows()

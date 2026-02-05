import cv2
from core.vision.face_auth import FaceAuthenticator

auth = FaceAuthenticator()

cap = cv2.VideoCapture(0)
ret, frame = cap.read()

if not ret:
    print("Camera not working")
else:
    user = auth.authenticate(frame)
    print("Detected:", user)

cap.release()

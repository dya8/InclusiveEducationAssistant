import cv2
from core.ml.eye_state_cnn import EyeStateCNN

cnn = EyeStateCNN("assets/models/eye_closed.weights.h5")
print("CNN READY")

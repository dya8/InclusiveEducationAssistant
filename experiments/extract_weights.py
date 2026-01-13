import tensorflow as tf
from core.ml.eye_state_model import build_eye_state_model

# Build model locally
model = build_eye_state_model()

# Load weights ONLY
model.load_weights(
    "assets/models/eye_closed_probability_model.h5",
    by_name=True,
    skip_mismatch=True
)

# Save clean inference-only model
model.save("assets/models/eye_closed_inference_model.h5")

print("Weights extracted and model rebuilt successfully")

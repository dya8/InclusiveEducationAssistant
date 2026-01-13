import keras

model = keras.models.load_model(
    "assets/models/eye_closed_probability_model.keras",
    compile=False
)

print("MODEL LOADED")
print(model.input_shape)
print(model.output_shape)

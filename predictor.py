import tensorflow as tf
import cv2
import numpy as np
import streamlit as st

# --------------------------------------
# Load trained model (only once)
# --------------------------------------
@st.cache_resource
def load_digit_model():
    return tf.keras.models.load_model("models/digit_model.keras")
model = load_digit_model()


def predict_digit(image):

    # -----------------------------
    # RGBA → Grayscale
    # -----------------------------
    gray = cv2.cvtColor(image, cv2.COLOR_RGBA2GRAY)

    # Invert colors
    gray = 255 - gray

    # Threshold
    _, thresh = cv2.threshold(gray, 50, 255, cv2.THRESH_BINARY)

    # -----------------------------
    # Find contours
    # -----------------------------
    contours, _ = cv2.findContours(
        thresh,
        cv2.RETR_EXTERNAL,
        cv2.CHAIN_APPROX_SIMPLE
    )

    if len(contours) == 0:
        return None, 0

    contour = max(contours, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(contour)

    digit = thresh[y:y+h, x:x+w]

    # -----------------------------
    # Keep aspect ratio
    # -----------------------------
    if h > w:
        new_h = 20
        new_w = max(1, int(w * 20 / h))
    else:
        new_w = 20
        new_h = max(1, int(h * 20 / w))

    digit = cv2.resize(
        digit,
        (new_w, new_h),
        interpolation=cv2.INTER_AREA
    )

    # -----------------------------
    # Create 28x28 canvas
    # -----------------------------
    canvas = np.zeros((28, 28), dtype=np.uint8)

    x_offset = (28 - new_w) // 2
    y_offset = (28 - new_h) // 2

    canvas[
        y_offset:y_offset+new_h,
        x_offset:x_offset+new_w
    ] = digit

    # -----------------------------
    # Normalize
    # -----------------------------
    canvas = canvas.astype("float32") / 255.0

    canvas = canvas.reshape(1, 28, 28, 1)

    # -----------------------------
    # Predict
    # -----------------------------
    prediction = model.predict(canvas, verbose=0)

    predicted_digit = int(np.argmax(prediction))
    confidence = float(np.max(prediction))

    return predicted_digit, confidence
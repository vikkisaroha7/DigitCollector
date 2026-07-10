import streamlit as st
from streamlit_drawable_canvas import st_canvas

from predictor import predict_digit
from sheets import save_data, digit_already_exists

st.set_page_config(
    page_title="Predict Digit",
    page_icon="✍️",
    layout="centered"
)

# --------------------------------------------------
# Session State
# --------------------------------------------------

if "canvas_key" not in st.session_state:
    st.session_state.canvas_key = "canvas_0"

if "prediction_done" not in st.session_state:
    st.session_state.prediction_done = False

if "predicted_digit" not in st.session_state:
    st.session_state.predicted_digit = None

if "confidence" not in st.session_state:
    st.session_state.confidence = None

if "show_wrong_prediction" not in st.session_state:
    st.session_state.show_wrong_prediction = False


# --------------------------------------------------
# Header
# --------------------------------------------------

st.title("✍️ Predict Handwritten Digit")
st.caption("Draw one digit from 0 to 9, then confirm or correct the AI prediction.")


# --------------------------------------------------
# User Details
# --------------------------------------------------

with st.container(border=True):
    st.markdown("#### User Details")

    col1, col2 = st.columns(2)

    with col1:
        name = st.text_input("Name")

    with col2:
        email = st.text_input("Email")


# --------------------------------------------------
# Canvas
# --------------------------------------------------

with st.container(border=True):
    st.markdown("#### Draw Digit")

    canvas_result = st_canvas(
        fill_color="black",
        stroke_width=15,
        stroke_color="black",
        background_color="white",
        width=300,
        height=300,
        drawing_mode="freedraw",
        key=st.session_state.canvas_key
    )

    col1, col2 = st.columns(2)

    with col1:
        predict_clicked = st.button(
            "🔍 Predict Digit",
            use_container_width=True,
            type="primary"
        )

    with col2:
        clear_clicked = st.button(
            "🧹 Clear Canvas",
            use_container_width=True
        )


# --------------------------------------------------
# Clear Canvas
# --------------------------------------------------

if clear_clicked:
    number = int(st.session_state.canvas_key.split("_")[1]) + 1
    st.session_state.canvas_key = f"canvas_{number}"

    st.session_state.prediction_done = False
    st.session_state.predicted_digit = None
    st.session_state.confidence = None
    st.session_state.show_wrong_prediction = False

    st.rerun()


# --------------------------------------------------
# Predict
# --------------------------------------------------

if predict_clicked:

    if name.strip() == "":
        st.error("Please enter your name.")
        st.stop()

    if email.strip() == "":
        st.error("Please enter your email.")
        st.stop()

    if canvas_result.image_data is None:
        st.error("Please draw a digit.")
        st.stop()

    digit, confidence = predict_digit(canvas_result.image_data)

    if digit is None:
        st.error("No digit detected.")
        st.stop()

    if confidence < 0.90:
        st.warning("Prediction confidence is too low. Please draw again." "OR"
                    " confirm whether the prediction is correct."
                   )
        

    st.session_state.predicted_digit = int(digit)
    st.session_state.confidence = float(confidence)
    st.session_state.prediction_done = True
    st.session_state.show_wrong_prediction = False


# --------------------------------------------------
# Prediction Result
# --------------------------------------------------

if st.session_state.prediction_done:

    predicted_digit = st.session_state.predicted_digit
    confidence = st.session_state.confidence

    with st.container(border=True):
        st.markdown("#### Prediction Result")

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Predicted Digit", predicted_digit)

        with col2:
            st.metric("Confidence", f"{confidence * 100:.2f}%")

        st.progress(confidence)

        st.markdown("#### Confirm Prediction")

        col1, col2 = st.columns(2)

        with col1:
            save_clicked = st.button(
                "✅ Save Prediction",
                use_container_width=True,
                type="primary"
            )

        with col2:
            wrong_clicked = st.button(
                "❌ Wrong Prediction",
                use_container_width=True
            )

        if save_clicked:

        
            save_data(
                    name,
                    email,
                    predicted_digit,
                    predicted_digit,
                    confidence,
                    "Yes"
            )

            st.success("Prediction saved successfully.")

        if wrong_clicked:
            st.session_state.show_wrong_prediction = True


# --------------------------------------------------
# Wrong Prediction Correction
# --------------------------------------------------

if st.session_state.prediction_done and st.session_state.show_wrong_prediction:

    predicted_digit = st.session_state.predicted_digit
    confidence = st.session_state.confidence

    with st.container(border=True):
        st.markdown("#### Correction")

        st.warning(f"AI predicted {predicted_digit}. Select the correct digit.")

        actual_digit = st.selectbox(
            "Correct Digit",
            list(range(10))
        )

        save_correct_clicked = st.button(
            "💾 Save Correct Digit",
            use_container_width=True,
            type="primary"
        )

        if save_correct_clicked:

            if digit_already_exists(email, actual_digit):
                st.warning(f"You have already submitted digit {actual_digit}.")
            else:
                save_data(
                    name,
                    email,
                    predicted_digit,
                    actual_digit,
                    confidence,
                    "No"
                )

                st.success("Correct digit saved successfully.")
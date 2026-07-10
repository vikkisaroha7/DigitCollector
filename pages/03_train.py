import streamlit as st
import pandas as pd

from train_model import train_model

st.set_page_config(
    page_title="Train Model",
    layout="wide"
)

st.title("🧠 Train CNN Model")

st.write("Train the MNIST CNN model directly from the dashboard.")

st.divider()

# ----------------------------------------
# User Inputs
# ----------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    epochs = st.slider(
        "Epochs",
        min_value=1,
        max_value=20,
        value=5
    )

with col2:
    batch_size = st.selectbox(
        "Batch Size",
        [16, 32, 64, 128],
        index=2
    )

with col3:
    learning_rate = st.selectbox(
        "Learning Rate",
        [0.1, 0.01, 0.001, 0.0001],
        index=2
    )

st.divider()

# ----------------------------------------
# Train Button
# ----------------------------------------

if st.button("🚀 Train Model", use_container_width=True):

    with st.spinner("Training model... Please wait."):

        result = train_model(
            epochs=epochs,
            batch_size=batch_size,
            learning_rate=learning_rate
        )

    st.success("Model trained successfully!")

    st.metric(
        "Test Accuracy",
        f"{result['accuracy']*100:.2f}%"
    )

    history = result["history"]

    # ----------------------------------------
    # Accuracy Chart
    # ----------------------------------------

    st.subheader("Training Accuracy")

    accuracy_df = pd.DataFrame({
        "Training Accuracy": history["accuracy"],
        "Validation Accuracy": history["val_accuracy"]
    })

    st.line_chart(accuracy_df)

    # ----------------------------------------
    # Loss Chart
    # ----------------------------------------

    st.subheader("Training Loss")

    loss_df = pd.DataFrame({
        "Training Loss": history["loss"],
        "Validation Loss": history["val_loss"]
    })

    st.line_chart(loss_df)

    st.success("Model saved to models/digit_model.keras")
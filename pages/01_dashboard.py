import os

import cv2
import streamlit as st
import tensorflow as tf

from sheets import get_all_records


st.set_page_config(
    page_title="Dashboard",
    page_icon="🏠",
    layout="wide"
)

st.title("🏠 AI Deep Learning Dashboard")


# --------------------------------------------------
# Model status
# --------------------------------------------------

model_exists = os.path.exists("models/digit_model.keras")

model_status = "✅ Loaded" if model_exists else "❌ Not Found"


# --------------------------------------------------
# Google Sheet status and record count
# --------------------------------------------------

sheet_status = "❌ Not Connected"
total_records = 0

try:
    records = get_all_records()
    total_records = len(records)
    sheet_status = "✅ Connected"

except Exception as error:
    sheet_status = "❌ Not Connected"
    st.error(f"Google Sheets connection error: {error}")


# --------------------------------------------------
# Dashboard metrics
# --------------------------------------------------

col1, col2, col3 = st.columns(3)

with col1:
    st.metric(
        "Model Status",
        model_status
    )

with col2:
    st.metric(
        "Google Sheet",
        sheet_status
    )

with col3:
    st.metric(
        "Digits Collected",
        total_records
    )


col4, col5 = st.columns(2)

with col4:
    st.metric(
        "TensorFlow Version",
        tf.__version__
    )

with col5:
    st.metric(
        "OpenCV Version",
        cv2.__version__
    )


# --------------------------------------------------
# Model architecture summary
# --------------------------------------------------

st.subheader("Current CNN Model")

st.code(
    """
Input (28 x 28 x 1)

↓

Conv2D (32 Filters)

↓

MaxPooling2D

↓

Conv2D (64 Filters)

↓

MaxPooling2D

↓

Flatten

↓

Dense (128)

↓

Dropout (0.5)

↓

Dense (10)

↓

Softmax
"""
)
import streamlit as st
import tensorflow as tf
import cv2
import os
import gspread
from oauth2client.service_account import ServiceAccountCredentials

st.set_page_config(
    page_title="Dashboard",
    layout="wide"
)

st.title("MNIST Handwritten Digit APP")

# ------------------------------------------------
# Model Status
# ------------------------------------------------

model_status = "❌ Not Found"

if os.path.exists("models/digit_model.keras"):
    model_status = "✅ Loaded"

# ------------------------------------------------
# Google Sheet Status
# ------------------------------------------------

sheet_status = "❌ Not Connected"
total_records = 0

try:

    scope = [
        "https://spreadsheets.google.com/feeds",
        "https://www.googleapis.com/auth/drive"
    ]

    credentials = ServiceAccountCredentials.from_json_keyfile_name(
        "credentials.json",
        scope
    )

    client = gspread.authorize(credentials)

    sheet = client.open("Digit Collector").sheet1

    total_records = len(sheet.get_all_records())

    sheet_status = "✅ Connected"

except:
    pass

# ------------------------------------------------
# Dashboard Cards
# ------------------------------------------------

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

st.divider()

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

st.divider()

st.subheader("Current CNN Model")

st.code("""
Input (28 x 28 x 1)

↓

Conv2D (32 Filters)

↓

MaxPooling

↓

Conv2D (64 Filters)

↓

MaxPooling

↓

Flatten

↓

Dense (128)

↓

Dropout

↓

Dense (10)

↓

Softmax
""")
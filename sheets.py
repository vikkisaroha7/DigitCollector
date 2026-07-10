import os
from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


# --------------------------------------------------
# Google API configuration
# --------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "Digit Collector"


# --------------------------------------------------
# Create Google credentials
# --------------------------------------------------

def get_google_credentials():
    """
    Use credentials.json locally.

    Use Streamlit Secrets when deployed on
    Streamlit Community Cloud.
    """

    if os.path.exists("credentials.json"):

        return Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )

    try:
        service_account_info = dict(
            st.secrets["gcp_service_account"]
        )

        return Credentials.from_service_account_info(
            service_account_info,
            scopes=SCOPES
        )

    except Exception as error:
        raise RuntimeError(
            "Google credentials were not found. "
            "For local use, add credentials.json to the project root. "
            "For Streamlit Cloud, configure gcp_service_account "
            "in the app's Secrets settings."
        ) from error


# --------------------------------------------------
# Connect to Google Sheet
# --------------------------------------------------

@st.cache_resource
def get_worksheet():
    """
    Create and cache the Google Sheets connection.
    """

    credentials = get_google_credentials()
    client = gspread.authorize(credentials)

    return client.open(SHEET_NAME).sheet1


worksheet = get_worksheet()


# --------------------------------------------------
# Save prediction data
# --------------------------------------------------

def save_data(
    name,
    email,
    predicted_digit,
    actual_digit,
    confidence,
    correct
):
    """
    Save the verified prediction to Google Sheets.

    Expected Google Sheet headers:

    Name
    Email
    Predicted
    Actual
    Confidence (%)
    Correct
    Timestamp
    """

    row = [
        str(name).strip(),
        str(email).strip(),
        str(int(predicted_digit)),
        str(int(actual_digit)),
        f"{float(confidence) * 100:.2f}",
        str(correct),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    ]

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )


# --------------------------------------------------
# Read all prediction records
# --------------------------------------------------

def get_all_records():
    """
    Return all records from Google Sheets.

    This can be used by the Dashboard and Analytics pages.
    """

    return worksheet.get_all_records()
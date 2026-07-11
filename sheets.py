import json
import os
from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive",
]

SHEET_NAME = "Digit Collector"


def get_google_credentials():
    """
    Load Google credentials:

    - Locally from credentials.json
    - On Streamlit Cloud from gcp_service_account_json
    """

    # Local environment
    if os.path.exists("credentials.json"):
        return Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES,
        )

    # Streamlit Community Cloud
    if "gcp_service_account_json" not in st.secrets:
        raise RuntimeError(
            "Missing Streamlit secret: gcp_service_account_json. "
            f"Available secret keys: {list(st.secrets.keys())}"
        )

    try:
        service_account_info = json.loads(
            st.secrets["gcp_service_account_json"]
        )
    except json.JSONDecodeError as error:
        raise RuntimeError(
            "The gcp_service_account_json secret is not valid JSON. "
            "Copy the complete original credentials.json file without editing it."
        ) from error

    return Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES,
    )


@st.cache_resource
def get_worksheet():
    """Create and cache the Google Sheets connection."""

    credentials = get_google_credentials()
    client = gspread.authorize(credentials)

    return client.open(SHEET_NAME).sheet1


worksheet = get_worksheet()


def save_data(
    name,
    email,
    predicted_digit,
    actual_digit,
    confidence,
    correct,
):
    """Save one verified prediction to Google Sheets."""

    row = [
        str(name).strip(),
        str(email).strip(),
        str(int(predicted_digit)),
        str(int(actual_digit)),
        f"{float(confidence) * 100:.2f}",
        str(correct),
        datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    ]

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED",
    )


def get_all_records():
    """Read all prediction records for Dashboard and Analytics."""

    return worksheet.get_all_records()
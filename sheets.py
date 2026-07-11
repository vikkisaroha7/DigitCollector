import os
from datetime import datetime

import gspread
import streamlit as st
from google.oauth2.service_account import Credentials


SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

SHEET_NAME = "Digit Collector"


def get_google_credentials():
    """
    Use credentials.json locally.
    Use Streamlit Secrets on Streamlit Community Cloud.
    """

    if os.path.exists("credentials.json"):
        return Credentials.from_service_account_file(
            "credentials.json",
            scopes=SCOPES
        )

    if "gcp_service_account" not in st.secrets:
        raise RuntimeError(
            "Missing Streamlit secret section "
            "'gcp_service_account'. "
            f"Available secret sections: {list(st.secrets.keys())}"
        )

    service_account_info = dict(
        st.secrets["gcp_service_account"]
    )

    return Credentials.from_service_account_info(
        service_account_info,
        scopes=SCOPES
    )


@st.cache_resource
def get_worksheet():
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
    correct
):
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


def get_all_records():
    return worksheet.get_all_records()
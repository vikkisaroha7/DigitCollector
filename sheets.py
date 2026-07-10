import gspread
from google.oauth2.service_account import Credentials
from datetime import datetime

# --------------------------------------------------
# Google Authentication
# --------------------------------------------------

SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive"
]

creds = Credentials.from_service_account_file(
    "credentials.json",
    scopes=SCOPES
)

client = gspread.authorize(creds)

worksheet = client.open("Digit Collector").sheet1


# --------------------------------------------------
# Save Prediction
# --------------------------------------------------

def save_data(
    name,
    email,
    predicted_digit,
    actual_digit,
    confidence,
    correct
):

    row = [

        str(name),

        str(email),

        str(int(predicted_digit)),

        str(int(actual_digit)),

        f"{float(confidence)*100:.2f}",

        str(correct),

        datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    ]

    print("Saving :", row)

    worksheet.append_row(
        row,
        value_input_option="USER_ENTERED"
    )


# --------------------------------------------------
# Duplicate Check
# --------------------------------------------------

def digit_already_exists(
    email,
    actual_digit
):

    records = worksheet.get_all_records()

    email = email.strip().lower()

    actual_digit = str(actual_digit)

    for record in records:

        try:

            if (

                str(record["Email"]).strip().lower() == email

                and

                str(record["Actual"]) == actual_digit

            ):

                return True

        except Exception:
            pass

    return False
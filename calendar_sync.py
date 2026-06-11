# File: calendar_sync.py

import os
import sys
# CHANGE: Fixed Google token reuse
from ui.window_utils import get_data_dir


from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build


# ─────────────────────────────────────
# GOOGLE CALENDAR
# ─────────────────────────────────────


SCOPES = [
    "https://www.googleapis.com/auth/calendar"
]


# CHANGE: Fixed Google token reuse - store token in persistent data directory
def _token_path():
    return os.path.join(get_data_dir(), "token.json")


# CHANGE: Fixed file path handling - credentials.json is bundled with the app
def _credentials_path():
    base = getattr(sys, "_MEIPASS", os.path.abspath("."))
    return os.path.join(base, "credentials.json")


# ─────────────────────────────────────
# SERVICE
# ─────────────────────────────────────


def get_service():

    creds = None

    token_file = _token_path()

    if os.path.exists(token_file):

        creds = Credentials.from_authorized_user_file(
            token_file,
            SCOPES,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            try:
                creds.refresh(Request())
            except Exception:
                creds = None

        if not creds:

            flow = InstalledAppFlow.from_client_secrets_file(
                _credentials_path(),
                SCOPES,
            )

            # Automatically open browser for authorization
            creds = flow.run_local_server(port=0, open_browser=True)

        with open(token_file, "w") as token:
            token.write(creds.to_json())

    service = build(
        "calendar",
        "v3",
        credentials=creds,
    )

    return service


# ─────────────────────────────────────
# CREATE EVENT
# ─────────────────────────────────────


def create_event(
    title,
    due_date,
    notes="",
    reminder_minutes=1440,
):

    service = get_service()

    event = {
        "summary": title,

        "description": notes,

        "start": {
            "date": due_date,
        },

        "end": {
            "date": due_date,
        },

        "reminders": {
            "useDefault": False,

            "overrides": [
                {
                    "method": "popup",
                    "minutes": reminder_minutes,
                }
            ],
        },
    }

    event = service.events().insert(
        calendarId="primary",
        body=event,
    ).execute()

    return event["id"]


# ─────────────────────────────────────
# DELETE EVENT
# ─────────────────────────────────────


def delete_event(event_id):

    service = get_service()

    service.events().delete(
        calendarId="primary",
        eventId=event_id,
    ).execute()


# ─────────────────────────────────────
# UPDATE EVENT
# ─────────────────────────────────────


def update_event(
    event_id,
    title,
    due_date,
    notes="",
    reminder_minutes=1440,
):

    service = get_service()

    event = {
        "summary": title,

        "description": notes,

        "start": {
            "date": due_date,
        },

        "end": {
            "date": due_date,
        },

        "reminders": {
            "useDefault": False,

            "overrides": [
                {
                    "method": "popup",
                    "minutes": reminder_minutes,
                }
            ],
        },
    }

    service.events().update(
        calendarId="primary",
        eventId=event_id,
        body=event,
    ).execute()


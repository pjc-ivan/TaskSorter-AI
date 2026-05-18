# File: calendar_sync.py

import os

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


# ─────────────────────────────────────
# SERVICE
# ─────────────────────────────────────


def get_service():

    creds = None

    if os.path.exists("token.json"):

        creds = Credentials.from_authorized_user_file(
            "token.json",
            SCOPES,
        )

    if not creds or not creds.valid:

        if creds and creds.expired and creds.refresh_token:

            creds.refresh(Request())

        else:

            flow = InstalledAppFlow.from_client_secrets_file(
                "credentials.json",
                SCOPES,
            )

            creds = flow.run_local_server(port=0)

        with open("token.json", "w") as token:
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
    ).ex


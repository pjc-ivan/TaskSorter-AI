# File: task_parser.py


from datetime import datetime, timedelta

import dateparser

from task_ai import parse_task_ai


# ─────────────────────────────────────
# DATE PARSER
# ─────────────────────────────────────


def parse_due_date(value):

    if not value:
        return datetime.today()

    # Convert to string and lowercase for comparison
    value_str = str(value).lower().strip()
    
    today = datetime.today()
    
    # German relative date handling
    german_dates = {
        "heute": today,
        "morgen": today + timedelta(days=1),
        "übermorgen": today + timedelta(days=2),
        "uebermorgen": today + timedelta(days=2),
        "gestern": today - timedelta(days=1),
    }
    
    # Check for exact German matches
    if value_str in german_dates:
        return german_dates[value_str]
    
    # Check for "in X Tagen" pattern
    import re
    days_match = re.search(r"in\s+(\d+)\s*tagen?", value_str)
    if days_match:
        days = int(days_match.group(1))
        return today + timedelta(days=days)
    
    # German weekday mapping
    german_weekdays = {
        "montag": 0,
        "mo": 0,
        "dienstag": 1,
        "di": 1,
        "mittwoch": 2,
        "mi": 2,
        "donnerstag": 3,
        "do": 3,
        "freitag": 4,
        "fr": 4,
        "samstag": 5,
        "sa": 5,
        "sonntag": 6,
        "so": 6,
    }
    
    # Check for German weekdays
    for day_name, weekday_num in german_weekdays.items():
        if day_name in value_str:
            # Find next occurrence of this weekday
            days_ahead = weekday_num - today.weekday()
            if days_ahead <= 0:  # Already passed this week, go to next week
                days_ahead += 7
            return today + timedelta(days=days_ahead)
    
    # English weekday mapping
    english_weekdays = {
        "monday": 0,
        "mon": 0,
        "tuesday": 1,
        "tue": 1,
        "wednesday": 2,
        "wed": 2,
        "thursday": 3,
        "thu": 3,
        "friday": 4,
        "fri": 4,
        "saturday": 5,
        "sat": 5,
        "sunday": 6,
        "sun": 6,
    }
    
    # Check for English weekdays
    for day_name, weekday_num in english_weekdays.items():
        if day_name in value_str:
            days_ahead = weekday_num - today.weekday()
            if days_ahead <= 0:
                days_ahead += 7
            return today + timedelta(days=days_ahead)
    
    # Try dateparser as fallback (for dates like "next week", "in 3 days", etc.)
    parsed = dateparser.parse(
        str(value),
        languages=["de", "en"],  # Support both German and English
        settings={
            "PREFER_DATES_FROM": "future",
            "RELATIVE_BASE": today,
        }
    )

    if parsed:
        return parsed

    return today


# ─────────────────────────────────────
# PRIORITY NORMALIZATION
# ─────────────────────────────────────


def normalize_priority(value):

    try:

        value = int(value)

        if value in [1, 2, 3]:
            return value

    except Exception:
        pass

    return 3


# ─────────────────────────────────────
# CLEANUP
# ─────────────────────────────────────


def cleanup_text(text: str):

    if not text:
        return "Untitled Task"

    text = text.strip()

    if len(text) == 0:
        return "Untitled Task"

    return text[0].upper() + text[1:]


# ─────────────────────────────────────
# MAIN PARSER
# ─────────────────────────────────────


def parse_task(text: str, lang="en"):

    ai_result = parse_task_ai(text)

    due_date = parse_due_date(
        ai_result.get("due")
    )

    return {
        "text": cleanup_text(
            ai_result.get("text", text)
        ),

        "due": due_date.date().isoformat(),

        "priority": normalize_priority(
            ai_result.get("priority", 3)
        ),

        "notes": ai_result.get(
            "notes",
            "",
        ),
    }


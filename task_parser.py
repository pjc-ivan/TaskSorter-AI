# File: task_parser.py


from datetime import datetime

import dateparser

from task_ai import parse_task_ai


# ─────────────────────────────────────
# DATE PARSER
# ─────────────────────────────────────


def parse_due_date(value):

    if not value:
        return datetime.today()

    parsed = dateparser.parse(
        str(value),
        languages=["de", "en"],
        settings={
            "PREFER_DATES_FROM": "future"
        }
    )

    if parsed:
        return parsed

    return datetime.today()


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


def parse_task(text: str, lang="de"):

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


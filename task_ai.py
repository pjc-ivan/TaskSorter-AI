# File: task_ai.py


import json
import ollama

try:
    import spacy

    nlp = spacy.load("de_core_news_sm")
    SPACY_AVAILABLE = True

except Exception:

    nlp = None
    SPACY_AVAILABLE = False


# ─────────────────────────────────────
# OFFLINE NLP FALLBACK
# ─────────────────────────────────────


def offline_cleanup(text: str):

    if not SPACY_AVAILABLE:

        return {
            "text": text,
            "due": None,
            "priority": 3,
            "notes": "",
        }

    doc = nlp(text)

    keep = []

    for token in doc:

        if token.pos_ in [
            "NOUN",
            "PROPN",
        ]:

            keep.append(token.text)

    cleaned = " ".join(keep).strip()

    if not cleaned:
        cleaned = text

    lower = text.lower()

    priority = 3

    if any(
        word in lower
        for word in [
            "dringend",
            "wichtig",
            "sofort",
            "urgent",
            "important",
        ]
    ):
        priority = 1

    elif any(
        word in lower
        for word in [
            "bald",
            "soon",
        ]
    ):
        priority = 2

    due = None

    for word in [
        "heute",
        "morgen",
        "montag",
        "dienstag",
        "mittwoch",
        "donnerstag",
        "freitag",
        "samstag",
        "sonntag",
    ]:

        if word in lower:
            due = word
            break

    return {
        "text": cleaned,
        "due": due,
        "priority": priority,
        "notes": "",
    }


# ─────────────────────────────────────
# OLLAMA AI
# ─────────────────────────────────────


MODEL_NAME = "gemma3:1b"


SYSTEM_PROMPT = """
You are an AI task extraction engine.

Your job:
- extract ONLY the essential task title
- extract due date
- extract priority
- extract notes

Rules:
- remove filler words
- remove pronouns
- remove unnecessary verbs
- keep only the important task
- task title must be very short

Priority:
1 = High
2 = Medium
3 = Low

Return ONLY valid JSON.

Examples:

Input:
Ich muss bis morgen dringend die Mathe Hausübung machen

Output:
{
  "text": "Mathe Hausübung",
  "due": "morgen",
  "priority": 1,
  "notes": ""
}

Input:
Vergiss nicht bis Freitag die Englisch Präsentation fertigzustellen

Output:
{
  "text": "Englisch Präsentation",
  "due": "Freitag",
  "priority": 2,
  "notes": ""
}

Input:
Ich sollte bald Physik lernen

Output:
{
  "text": "Physik lernen",
  "due": null,
  "priority": 2,
  "notes": ""
}
"""


# ─────────────────────────────────────
# AI PARSER
# ─────────────────────────────────────


def ollama_parse(text: str):

    response = ollama.chat(
        model=MODEL_NAME,
        messages=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT,
            },
            {
                "role": "user",
                "content": text,
            },
        ],
    )

    raw = response["message"]["content"].strip()

    start = raw.find("{")
    end = raw.rfind("}") + 1

    if start == -1 or end == 0:
        raise Exception("No JSON returned")

    raw_json = raw[start:end]

    parsed = json.loads(raw_json)

    return {
        "text": parsed.get("text", text),
        "due": parsed.get("due", None),
        "priority": parsed.get("priority", 3),
        "notes": parsed.get("notes", ""),
    }


# ─────────────────────────────────────
# MAIN
# ─────────────────────────────────────


def parse_task_ai(text: str):

    try:

        return ollama_parse(text)

    except Exception as e:

        print("OLLAMA ERROR")
        print(e)

        return offline_cleanup(text)


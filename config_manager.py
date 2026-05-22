# File: config_manager.py


import json
from pathlib import Path


# ─────────────────────────────────────
# CONFIG
# ─────────────────────────────────────


CONFIG_FILE = Path("config.json")


config = {
    # Application language: "en" for English, "de" for German
    "language": "en",
    # Dark mode enabled/disabled
    "darkmode": True,
    # Show completed tasks in the list
    "show_done": True,
    # File path for storing tasks
    "task_file": "tasks.json",
    # Google Calendar synchronization (disabled by default)
    "google_sync": False,
    # First run flag for initial setup
    "first_run": False,
    # Minutes before deadline to send reminder
    "reminder_minutes": 1440,
    # Maximum character length for task input
    "max_task_length": 200,
}


# ─────────────────────────────────────
# LOAD CONFIG
# ─────────────────────────────────────


def load_config():

    global config

    if CONFIG_FILE.exists():

        try:

            loaded = json.loads(
                CONFIG_FILE.read_text(
                    encoding="utf-8"
                )
            )

            config.update(loaded)

        except Exception as e:

            print("Config load failed")
            print(e)


# ─────────────────────────────────────
# SAVE CONFIG
# ─────────────────────────────────────


def save_config():

    try:

        CONFIG_FILE.write_text(
            json.dumps(
                config,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    except Exception as e:

        print("Config save failed")
        print(e)


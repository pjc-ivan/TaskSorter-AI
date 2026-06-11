# File: config_manager.py


import json
import os
import sys
from pathlib import Path
# CHANGE: Fixed task persistence
from ui.window_utils import get_data_dir


# ─────────────────────────────────────
# CONFIG
# ─────────────────────────────────────


def _bundled_config_path():
    """
    Return the path to the bundled default config.json
    (inside PyInstaller archive or alongside the script).
    """

    base = getattr(
        sys,
        "_MEIPASS",
        os.path.abspath("."),
    )
    return os.path.join(base, "config.json")


def _user_config_path():
    """Return the writable user config.json inside the data directory."""

    return os.path.join(get_data_dir(), "config.json")


CONFIG_FILE = Path(_user_config_path())


config = {
    # Application language (English only)
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
    """
    Load config from the user data directory first.
    Fall back to the bundled default config.json if no user config exists.
    """

    global config

    user_file = Path(_user_config_path())

    if user_file.exists():

        try:

            loaded = json.loads(
                user_file.read_text(
                    encoding="utf-8"
                )
            )

            config.update(loaded)
            return

        except Exception as e:

            print("User config load failed, falling back to bundled")
            print(e)

    # Fall back to bundled config.json (PyInstaller or source directory)
    bundled = _bundled_config_path()

    if os.path.exists(bundled):

        try:

            loaded = json.loads(
                open(bundled, encoding="utf-8").read()
            )

            config.update(loaded)

        except Exception as e:

            print("Bundled config load failed")
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


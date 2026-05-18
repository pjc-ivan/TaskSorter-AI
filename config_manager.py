# File: config_manager.py


import json
from pathlib import Path


# ─────────────────────────────────────
# CONFIG
# ─────────────────────────────────────


CONFIG_FILE = Path("config.json")


config = {
    "language": "de",
    "darkmode": True,
    "show_done": True,
    "task_file": "tasks.json",
    "google_sync": True,
    "first_run": False,
    "reminder_minutes": 1440,
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


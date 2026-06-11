# File: task_storage.py


import json
import os
from pathlib import Path
# CHANGE: Fixed task persistence
from ui.window_utils import get_data_dir


# CHANGE: Fixed task persistence - resolve task file path inside the data directory
def _tasks_path():
    return os.path.join(get_data_dir(), "tasks.json")


# ─────────────────────────────────────
# LOAD TASKS
# ─────────────────────────────────────


def load_tasks(config):

    path = Path(_tasks_path())

    if not path.exists():
        return []

    try:

        data = json.loads(
            path.read_text(
                encoding="utf-8"
            )
        )

        if isinstance(data, list):
            return data

    except Exception as e:

        print("Task load failed")
        print(e)

    return []


# ─────────────────────────────────────
# SAVE TASKS
# ─────────────────────────────────────


def save_tasks(tasks, config):

    path = Path(_tasks_path())

    try:

        path.write_text(
            json.dumps(
                tasks,
                indent=2,
                ensure_ascii=False,
            ),
            encoding="utf-8",
        )

    except Exception as e:

        print("Task save failed")
        print(e)


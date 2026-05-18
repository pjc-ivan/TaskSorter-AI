# File: task_storage.py


import json
from pathlib import Path


# ─────────────────────────────────────
# LOAD TASKS
# ─────────────────────────────────────


def load_tasks(config):

    path = Path(
        config.get(
            "task_file",
            "tasks.json",
        )
    )

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

    path = Path(
        config.get(
            "task_file",
            "tasks.json",
        )
    )

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


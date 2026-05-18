# File: TaskSorter.py


import os

import customtkinter as ctk
import tkinter as tk

from task_parser import parse_task

from config_manager import (
    load_config,
    save_config,
    config,
)

from task_storage import (
    load_tasks,
    save_tasks,
)

from ui.settings_window import open_settings
from ui.manual_dialog import open_manual_dialog
from ui.task_renderer import render_tasks


try:
    from calendar_sync import (
        create_event,
        delete_event,
    )

    GCAL = True

except Exception:

    GCAL = False


# ─────────────────────────────────────
# CONFIG
# ─────────────────────────────────────


load_config()


ctk.set_appearance_mode(
    "dark"
    if config.get("darkmode", True)
    else "light"
)


# ─────────────────────────────────────
# ROOT
# ─────────────────────────────────────


root = ctk.CTk()

root.geometry("860x820")

root.title("TaskSorter AI")


# ─────────────────────────────────────
# ICON
# ─────────────────────────────────────


try:

    icon_path = os.path.abspath(
        "assets/icon.png"
    )

    icon = tk.PhotoImage(
        file=icon_path
    )

    root.iconphoto(True, icon)

    root._icon_image = icon

except Exception as e:

    print(e)


# ─────────────────────────────────────
# DATA
# ─────────────────────────────────────


tasks = load_tasks(config)


# ─────────────────────────────────────
# HEADER
# ─────────────────────────────────────


header = ctk.CTkFrame(
    root,
    corner_radius=0,
)

header.pack(
    fill="x"
)


ctk.CTkLabel(
    header,
    text="TaskSorter AI",
    font=("Arial", 30, "bold"),
).pack(
    side="left",
    padx=24,
    pady=20,
)


header_buttons = ctk.CTkFrame(
    header,
    fg_color="transparent",
)

header_buttons.pack(
    side="right",
    padx=20,
)


ctk.CTkButton(
    header_buttons,
    text="Add Task",
    width=140,
    height=42,
    command=lambda: open_manual_dialog(
        root,
        insert_task,
    ),
).pack(
    side="left",
    padx=8,
)


ctk.CTkButton(
    header_buttons,
    text="Settings",
    width=140,
    height=42,
    command=lambda: open_settings(
        root,
        config,
        save_config,
    ),
).pack(
    side="left",
    padx=8,
)


# ─────────────────────────────────────
# INPUT
# ─────────────────────────────────────


input_frame = ctk.CTkFrame(
    root,
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=20,
)


entry = ctk.CTkEntry(
    input_frame,
    placeholder_text=(
        "Describe your task..."
    ),
    height=52,
    font=("Arial", 16),
)

entry.pack(
    side="left",
    fill="x",
    expand=True,
    padx=(18, 12),
    pady=18,
)


# ─────────────────────────────────────
# TASKS
# ─────────────────────────────────────


scroll = ctk.CTkScrollableFrame(
    root,
)

scroll.pack(
    fill="both",
    expand=True,
    padx=20,
    pady=(0, 20),
)


# ─────────────────────────────────────
# HELPERS
# ─────────────────────────────────────


MAX_TASK_LENGTH = 300



def save_all():

    save_tasks(
        tasks,
        config,
    )

    save_config()



def refresh_ui():

    render_tasks(
        scroll,
        tasks,
        toggle_done,
        delete_task,
        edit_task,
        config,
    )



def insert_task(parsed: dict):

    event_id = None

    if (
        config.get("google_sync")
        and GCAL
    ):

        try:

            event_id = create_event(
                parsed["text"],
                parsed["due"],
                parsed.get("notes", ""),
                config.get(
                    "reminder_minutes",
                    1440,
                ),
            )

        except Exception as e:

            print(e)

    parsed["done"] = False

    parsed["event_id"] = event_id

    tasks.append(parsed)

    save_all()

    refresh_ui()



def add_task_from_input():

    text = entry.get().strip()

    if not text:
        return

    if len(text) > MAX_TASK_LENGTH:
        return

    parsed = parse_task(text)

    insert_task(parsed)

    entry.delete(0, "end")



def toggle_done(index):

    tasks[index]["done"] = not tasks[index]["done"]

    save_all()

    refresh_ui()



def delete_task(index):

    if tasks[index].get("event_id"):

        try:
            delete_event(
                tasks[index]["event_id"]
            )

        except Exception:
            pass

    tasks.pop(index)

    save_all()

    refresh_ui()


# ─────────────────────────────────────
# EDIT TASK
# ─────────────────────────────────────


def edit_task(index):

    task = tasks[index]

    win = ctk.CTkToplevel(root)

    win.title("Edit Task")

    win.geometry("520x680")


    ctk.CTkLabel(
        win,
        text="Edit Task",
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    frame = ctk.CTkFrame(
        win,
        fg_color="transparent",
    )

    frame.pack(
        fill="both",
        expand=True,
        padx=28,
        pady=10,
    )


    title_entry = ctk.CTkEntry(
        frame,
        height=48,
    )

    title_entry.insert(
        0,
        task.get("text", "")
    )

    title_entry.pack(
        fill="x",
        pady=(0, 18),
    )


    due_entry = ctk.CTkEntry(
        frame,
        height=48,
    )

    due_entry.insert(
        0,
        task.get("due", "")
    )

    due_entry.pack(
        fill="x",
        pady=(0, 18),
    )


    prio_map = {
        1: "High",
        2: "Medium",
        3: "Low",
    }


    reverse_map = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }


    prio_var = tk.StringVar(
        value=prio_map.get(
            task.get("priority", 3),
            "Low",
        )
    )


    ctk.CTkOptionMenu(
        frame,
        values=[
            "High",
            "Medium",
            "Low",
        ],
        variable=prio_var,
        height=46,
    ).pack(
        fill="x",
        pady=(0, 18),
    )


    notes_box = ctk.CTkTextbox(
        frame,
        height=180,
    )

    notes_box.insert(
        "1.0",
        task.get("notes", "")
    )

    notes_box.pack(
        fill="x",
        pady=(0, 24),
    )


    def save_edit():

        task["text"] = title_entry.get().strip()

        task["due"] = due_entry.get().strip()

        task["priority"] = reverse_map[
            prio_var.get()
        ]

        task["notes"] = notes_box.get(
            "1.0",
            "end",
        ).strip()

        save_all()

        refresh_ui()

        win.destroy()


    ctk.CTkButton(
        frame,
        text="Save",
        height=48,
        command=save_edit,
    ).pack(
        fill="x"
    )


# ─────────────────────────────────────
# BUTTONS
# ─────────────────────────────────────


ctk.CTkButton(
    input_frame,
    text="Create",
    width=140,
    height=52,
    command=add_task_from_input,
).pack(
    side="right",
    padx=(0, 18),
)


entry.bind(
    "<Return>",
    lambda e: add_task_from_input(),
)


# ─────────────────────────────────────
# START
# ─────────────────────────────────────


refresh_ui()

root.mainloop()


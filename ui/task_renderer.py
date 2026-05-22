# File: ui/task_renderer.py


import customtkinter as ctk

from datetime import datetime


# ─────────────────────────────────────
# PRIORITY
# ─────────────────────────────────────


PRIORITY_DATA = {
    1: {
        "label": "High",
        "color": "#ff4d4d",
    },

    2: {
        "label": "Medium",
        "color": "#ffb84d",
    },

    3: {
        "label": "Low",
        "color": "#66cc66",
    },
}


# ─────────────────────────────────────
# RENDER TASKS
# ─────────────────────────────────────


def render_tasks(
    frame,
    tasks,
    toggle_done,
    delete_task,
    edit_task,
    config,
):

    for widget in frame.winfo_children():
        widget.destroy()


    visible_tasks = [
        (i, task)
        for i, task in enumerate(tasks)
        if not (
            task.get("done")
            and not config.get("show_done", True)
        )
    ]


    visible_tasks.sort(
        key=lambda x: (
            x[1].get("due", "9999-99-99"),
            x[1].get("priority", 3),
        )
    )


    if not visible_tasks:

        empty = ctk.CTkLabel(
            frame,
            text="No tasks available",
            text_color="gray",
            font=("Arial", 18),
        )

        empty.pack(
            pady=40
        )

        return


    for index, task in visible_tasks:

        create_task_card(
            frame,
            index,
            task,
            toggle_done,
            delete_task,
            edit_task,
        )


# ─────────────────────────────────────
# TASK CARD
# ─────────────────────────────────────


def create_task_card(
    parent,
    index,
    task,
    toggle_done,
    delete_task,
    edit_task,
):

    priority = PRIORITY_DATA.get(
        task.get("priority", 3),
        PRIORITY_DATA[3],
    )


    card = ctk.CTkFrame(
        parent,
        corner_radius=20,
    )

    card.pack(
        fill="x",
        padx=6,
        pady=8,
    )


    # ─────────────────────────────────────
    # HEADER
    # ─────────────────────────────────────


    header = ctk.CTkFrame(
        card,
        fg_color="transparent",
    )

    header.pack(
        fill="x",
        padx=18,
        pady=(16, 8),
    )


    task_text = task.get(
        "text",
        "Untitled Task",
    )


    if task.get("done"):
        task_text = "✔ " + task_text


    title = ctk.CTkLabel(
        header,
        text=task_text,
        font=("Arial", 20, "bold"),
        anchor="w",
    )

    title.pack(
        side="left",
        fill="x",
        expand=True,
    )


    priority_label = ctk.CTkLabel(
        header,
        text=priority["label"],
        text_color=priority["color"],
        font=("Arial", 14, "bold"),
    )

    priority_label.pack(
        side="right"
    )


    # ─────────────────────────────────────
    # DATE
    # ─────────────────────────────────────


    due = task.get(
        "due",
        "",
    )


    try:

        formatted = datetime.strptime(
            due,
            "%Y-%m-%d",
        ).strftime(
            "%d.%m.%Y"
        )

    except Exception:

        formatted = due


    due_label = ctk.CTkLabel(
        card,
        text=f"Due: {formatted}",
        text_color="gray",
        font=("Arial", 14),
    )

    due_label.pack(
        anchor="w",
        padx=18,
        pady=(0, 8),
    )


    # ─────────────────────────────────────
    # NOTES
    # ─────────────────────────────────────


    notes = task.get(
        "notes",
        "",
    )

    if notes is None:
        notes = ""

    notes = notes.strip()


    if notes:

        notes_label = ctk.CTkLabel(
            card,
            text=notes,
            justify="left",
            wraplength=520,
            text_color="gray",
            font=("Arial", 14),
        )

        notes_label.pack(
            anchor="w",
            padx=18,
            pady=(0, 12),
        )


    # ─────────────────────────────────────
    # BUTTONS
    # ─────────────────────────────────────


    buttons = ctk.CTkFrame(
        card,
        fg_color="transparent",
    )

    buttons.pack(
        pady=(0, 16),
    )


    ctk.CTkButton(
        buttons,
        text="Done",
        width=110,
        height=42,
        command=lambda: toggle_done(index),
    ).pack(
        side="left",
        padx=6,
    )


    ctk.CTkButton(
        buttons,
        text="Edit",
        width=110,
        height=42,
        command=lambda: edit_task(index),
    ).pack(
        side="left",
        padx=6,
    )


    ctk.CTkButton(
        buttons,
        text="Delete",
        width=110,
        height=42,
        fg_color="#d9534f",
        hover_color="#c9302c",
        command=lambda: delete_task(index),
    ).pack(
        side="left",
        padx=6,
    )


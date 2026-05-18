# File: ui/manual_dialog.py


import customtkinter as ctk
import tkinter as tk

from datetime import datetime


# ─────────────────────────────────────
# MANUAL TASK DIALOG
# ─────────────────────────────────────


def open_manual_dialog(
    root,
    insert_task,
):

    win = ctk.CTkToplevel(root)

    win.title("Add Task")

    win.geometry("520x680")

    win.resizable(False, False)


    # ─────────────────────────────────────
    # TITLE
    # ─────────────────────────────────────


    ctk.CTkLabel(
        win,
        text="Add Task",
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    # ─────────────────────────────────────
    # MAIN FRAME
    # ─────────────────────────────────────


    form = ctk.CTkFrame(
        win,
        fg_color="transparent",
    )

    form.pack(
        fill="both",
        expand=True,
        padx=28,
        pady=(0, 20),
    )


    # ─────────────────────────────────────
    # TASK TITLE
    # ─────────────────────────────────────


    ctk.CTkLabel(
        form,
        text="Task",
        font=("Arial", 15),
    ).pack(
        anchor="w",
        pady=(0, 6),
    )


    name_entry = ctk.CTkEntry(
        form,
        placeholder_text="Enter task title...",
        height=48,
    )

    name_entry.pack(
        fill="x",
        pady=(0, 18),
    )


    # ─────────────────────────────────────
    # DUE DATE
    # ─────────────────────────────────────


    ctk.CTkLabel(
        form,
        text="Due Date",
        font=("Arial", 15),
    ).pack(
        anchor="w",
        pady=(0, 6),
    )


    date_entry = ctk.CTkEntry(
        form,
        placeholder_text=datetime.today().strftime(
            "%d.%m.%Y"
        ),
        height=48,
    )

    date_entry.pack(
        fill="x",
        pady=(0, 18),
    )


    # ─────────────────────────────────────
    # PRIORITY
    # ─────────────────────────────────────


    ctk.CTkLabel(
        form,
        text="Priority",
        font=("Arial", 15),
    ).pack(
        anchor="w",
        pady=(0, 6),
    )


    prio_var = tk.StringVar(
        value="Medium"
    )


    ctk.CTkOptionMenu(
        form,
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


    # ─────────────────────────────────────
    # NOTES
    # ─────────────────────────────────────


    ctk.CTkLabel(
        form,
        text="Notes",
        font=("Arial", 15),
    ).pack(
        anchor="w",
        pady=(0, 6),
    )


    notes_box = ctk.CTkTextbox(
        form,
        height=180,
    )

    notes_box.pack(
        fill="x",
        pady=(0, 26),
    )


    # ─────────────────────────────────────
    # BUTTONS
    # ─────────────────────────────────────


    buttons = ctk.CTkFrame(
        form,
        fg_color="transparent",
    )

    buttons.pack(
        pady=10,
    )


    def save_manual():

        prio_map = {
            "High": 1,
            "Medium": 2,
            "Low": 3,
        }

        try:

            due = datetime.strptime(
                date_entry.get(),
                "%d.%m.%Y",
            ).date().isoformat()

        except Exception:

            due = datetime.today().date().isoformat()

        parsed = {
            "text": name_entry.get().strip(),

            "due": due,

            "priority": prio_map[
                prio_var.get()
            ],

            "notes": notes_box.get(
                "1.0",
                "end",
            ).strip(),
        }

        insert_task(parsed)

        win.destroy()


    ctk.CTkButton(
        buttons,
        text="Save",
        width=170,
        height=48,
        command=save_manual,
    ).pack(
        side="left",
        padx=10,
    )


    ctk.CTkButton(
        buttons,
        text="Cancel",
        width=170,
        height=48,
        command=win.destroy,
    ).pack(
        side="left",
        padx=10,
    )


# File: ui/manual_dialog.py
# Manual task creation dialog for TaskSorter AI
# Allows users to manually create tasks with title, due date, priority, and notes


import customtkinter as ctk
import tkinter as tk

from datetime import datetime


# ─────────────────────────────────────
# OPEN MANUAL TASK DIALOG
# ─────────────────────────────────────
# Opens a dialog window for manually creating a new task


def open_manual_dialog(
    root,
    insert_task,
):
    """
    Open a dialog for manually creating a new task.
    
    Args:
        root: The main application window
        insert_task: Function to call when task is created
    
    The dialog allows entering:
    - Task title
    - Due date (DD.MM.YYYY format)
    - Priority (High, Medium, Low)
    - Notes
    """

    # Create dialog window
    win = ctk.CTkToplevel(root)

    win.title("Add Task")

    win.geometry("520x680")

    win.resizable(False, False)


    # ─────────────────────────────────────
    # DIALOG TITLE
    # ─────────────────────────────────────

    ctk.CTkLabel(
        win,
        text="Add Task",
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    # ─────────────────────────────────────
    # MAIN FORM FRAME
    # ─────────────────────────────────────
    # Container for all form fields

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
    # TASK TITLE INPUT
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
    # DUE DATE INPUT
    # ─────────────────────────────────────

    ctk.CTkLabel(
        form,
        text="Due Date",
        font=("Arial", 15),
    ).pack(
        anchor="w",
        pady=(0, 6),
    )


    # Default placeholder shows today's date in DD.MM.YYYY format
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
    # PRIORITY SELECTION
    # ─────────────────────────────────────

    ctk.CTkLabel(
        form,
        text="Priority",
        font=("Arial", 15),
    ).pack(
        anchor="w",
        pady=(0, 6),
    )


    # Variable for priority selection (default: Medium)
    prio_var = tk.StringVar(
        value="Medium"
    )


    # Priority dropdown menu
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
    # NOTES TEXT AREA
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
    # ACTION BUTTONS
    # ─────────────────────────────────────

    buttons = ctk.CTkFrame(
        form,
        fg_color="transparent",
    )

    buttons.pack(
        pady=10,
    )


    def save_manual():
        """
        Save the manually entered task and close dialog.
        
        Parses the due date from DD.MM.YYYY format to ISO format.
        If date parsing fails, uses today's date as default.
        """

        # Map priority labels to numeric values
        prio_map = {
            "High": 1,
            "Medium": 2,
            "Low": 3,
        }

        # Parse due date from user input
        try:

            due = datetime.strptime(
                date_entry.get(),
                "%d.%m.%Y",
            ).date().isoformat()

        except Exception:

            # Use today's date if parsing fails
            due = datetime.today().date().isoformat()

        # Build task data dictionary
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


    # Save button - creates the task
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


    # Cancel button - closes dialog without saving
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


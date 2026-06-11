# File: ui/manual_dialog.py
# Manual task creation dialog for TaskSorter AI
# Allows users to manually create tasks with title, due date, priority, and notes


import customtkinter as ctk
import tkinter as tk

from datetime import datetime
# CHANGE: Windows/Linux icon compatibility fix
from ui.window_utils import (
    apply_app_icon,
    fit_window_after_idle,
    fit_window_to_content,
)


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

    # CHANGE: Delayed window initialization
    win.withdraw()
    # CHANGE: Window hierarchy management
    win.transient(root)

    win.title("Add Task")

    # CHANGE: Removed fixed window dimensions
    # CHANGE: Windows/Linux icon compatibility fix
    apply_app_icon(win)


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

        # CHANGE: Parent-child focus handling
        win.grab_release()
        win.destroy()
        root.focus_set()


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


    # CHANGE: Parent-child focus handling
    def on_manual_closing():
        win.grab_release()
        win.destroy()
        root.focus_set()

    # Cancel button - closes dialog without saving
    ctk.CTkButton(
        buttons,
        text="Cancel",
        width=170,
        height=48,
        command=on_manual_closing,
    ).pack(
        side="left",
        padx=10,
    )

    win.protocol("WM_DELETE_WINDOW", on_manual_closing)

    # CHANGE: Delayed window initialization - show after all widgets created
    win.update_idletasks()
    fit_window_to_content(
        win,
        min_width=420,
        min_height=520,
        max_width_ratio=0.85,
        max_height_ratio=0.85,
    )
    win.deiconify()
    # CHANGE: Modal dialog behavior
    win.grab_set()
    win.focus_set()

    # CHANGE: Added automatic geometry calculation
    fit_window_after_idle(
        win,
        min_width=420,
        min_height=520,
        max_width_ratio=0.85,
        max_height_ratio=0.85,
    )


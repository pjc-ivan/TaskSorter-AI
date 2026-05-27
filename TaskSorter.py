# File: TaskSorter.py
# Main application file for TaskSorter AI
# This is the entry point that creates the GUI and handles task management


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


# Try to import Google Calendar synchronization
# If import fails, disable Google Calendar feature

try:
    from calendar_sync import (
        create_event,
        delete_event,
    )

    GCAL = True

except Exception:

    GCAL = False


# ─────────────────────────────────────
# CONFIGURATION
# ─────────────────────────────────────
# Load configuration from config.json file


load_config()


# Set appearance mode based on configuration (dark or light theme)

ctk.set_appearance_mode(
    "dark"
    if config.get("darkmode", True)
    else "light"
)


# ─────────────────────────────────────
# MAIN APPLICATION WINDOW
# ─────────────────────────────────────
# Create the root window for the application


root = ctk.CTk()

root.geometry("860x820")

root.title("TaskSorter AI")


# ─────────────────────────────────────
# APPLICATION ICON
# ─────────────────────────────────────
# Try to load and set the application icon


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
# LOAD TASK DATA
# ─────────────────────────────────────
# Load existing tasks from storage


tasks = load_tasks(config)


# ─────────────────────────────────────
# HEADER SECTION
# ─────────────────────────────────────
# Create the header with title and action buttons


header = ctk.CTkFrame(
    root,
    corner_radius=0,
)

header.pack(
    fill="x"
)


# Application title label

ctk.CTkLabel(
    header,
    text="TaskSorter AI",
    font=("Arial", 30, "bold"),
).pack(
    side="left",
    padx=24,
    pady=20,
)


# Container for header buttons

header_buttons = ctk.CTkFrame(
    header,
    fg_color="transparent",
)

header_buttons.pack(
    side="right",
    padx=20,
)


# Add Task button - opens manual task creation dialog

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


# Settings button - opens settings window

ctk.CTkButton(
    header_buttons,
    text="Settings",
    width=140,
    height=42,
    command=lambda: open_settings(
        root,
        config,
        save_config,
        refresh_ui,  # Pass refresh callback for language changes
    ),
).pack(
    side="left",
    padx=8,
)


# ─────────────────────────────────────
# INPUT SECTION
# ─────────────────────────────────────
# Text input field for quick task creation


input_frame = ctk.CTkFrame(
    root,
)

input_frame.pack(
    fill="x",
    padx=20,
    pady=20,
)


# Text entry field with placeholder text

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
# TASKS SCROLL AREA
# ─────────────────────────────────────
# Scrollable frame to display all task cards


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
# HELPER FUNCTIONS
# ─────────────────────────────────────
# Maximum allowed length for task input text

MAX_TASK_LENGTH = 300



def save_all():
    """
    Save all tasks and configuration to disk.
    Persists both task data and application settings.
    """

    save_tasks(
        tasks,
        config,
    )

    save_config()



def refresh_ui():
    """
    Refresh the user interface by re-rendering all tasks.
    Clears the scrollable frame and rebuilds task cards.
    """

    render_tasks(
        scroll,
        tasks,
        toggle_done,
        delete_task,
        edit_task,
        config,
    )



def insert_task(parsed: dict):
    """
    Insert a new task into the task list.
    
    Args:
        parsed: Dictionary containing task data (text, due date, priority, notes)
    
    Creates Google Calendar event if sync is enabled.
    """

    event_id = None

    # Create Google Calendar event if sync is enabled
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

    # Mark task as not done by default
    parsed["done"] = False

    parsed["event_id"] = event_id

    tasks.append(parsed)

    save_all()

    refresh_ui()



def add_task_from_input():
    """
    Parse and add a task from the text input field.
    Uses AI to extract task details from natural language.
    """

    # Get and clean input text
    text = entry.get().strip()

    # Don't process empty input
    if not text:
        return

    # Don't process if exceeds maximum length
    if len(text) > MAX_TASK_LENGTH:
        return

    # Show loading indicator
    loading_label = ctk.CTkLabel(
        input_frame,
        text="⏳ Parsing...",
        font=("Arial", 14),
        text_color=("gray50", "gray70"),
    )
    loading_label.pack(
        side="right",
        padx=(0, 12),
    )
    
    # Disable input during parsing
    entry.configure(state="disabled")
    create_button.configure(state="disabled")
    
    # Force UI update to show loading indicator
    root.update()

    try:
        # Parse task using AI/NLP
        parsed = parse_task(text)

        insert_task(parsed)

        # Clear input field after adding
        entry.delete(0, "end")
    
    finally:
        # Remove loading indicator
        loading_label.destroy()
        
        # Re-enable input
        entry.configure(state="normal")
        create_button.configure(state="normal")



def toggle_done(index):
    """
    Toggle the completion status of a task.
    
    Args:
        index: Index of the task in the tasks list
    """

    tasks[index]["done"] = not tasks[index]["done"]

    save_all()

    refresh_ui()



def delete_task(index):
    """
    Delete a task from the task list.
    
    Args:
        index: Index of the task to delete
    
    Also deletes associated Google Calendar event if it exists.
    """

    # Delete Google Calendar event if linked
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
# EDIT TASK FUNCTION
# ─────────────────────────────────────
# Opens dialog to edit an existing task


def edit_task(index):
    """
    Open dialog to edit an existing task.
    
    Args:
        index: Index of the task to edit
    
    Allows editing of title, due date, priority, and notes.
    """

    task = tasks[index]

    # Create edit dialog window
    win = ctk.CTkToplevel(root)

    win.title("Edit Task")

    win.geometry("520x680")


    # Dialog title

    ctk.CTkLabel(
        win,
        text="Edit Task",
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    # Form container frame

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


    # Task title input field

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


    # Due date input field

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


    # Priority mapping (number to label)

    prio_map = {
        1: "High",
        2: "Medium",
        3: "Low",
    }


    # Reverse priority mapping (label to number)

    reverse_map = {
        "High": 1,
        "Medium": 2,
        "Low": 3,
    }


    # Priority selection variable

    prio_var = tk.StringVar(
        value=prio_map.get(
            task.get("priority", 3),
            "Low",
        )
    )


    # Priority dropdown menu

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


    # Notes text area

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
        """Save edited task data and close dialog."""

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


    # Save button

    ctk.CTkButton(
        frame,
        text="Save",
        height=48,
        command=save_edit,
    ).pack(
        fill="x"
    )


# ─────────────────────────────────────
# CREATE BUTTON
# ─────────────────────────────────────
# Button to create task from input field


create_button = ctk.CTkButton(
    input_frame,
    text="Create",
    width=140,
    height=52,
    command=add_task_from_input,
).pack(
    side="right",
    padx=(0, 18),
)


# Bind Enter key to create task

entry.bind(
    "<Return>",
    lambda e: add_task_from_input(),
)


# ─────────────────────────────────────
# START APPLICATION
# ─────────────────────────────────────
# Initial UI render and start main event loop


refresh_ui()

root.mainloop()


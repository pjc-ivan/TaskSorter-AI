# File: ui/settings_window.py
# Settings window for TaskSorter AI application
# Allows users to configure appearance, tasks, Google Calendar, and AI settings


import customtkinter as ctk
import tkinter as tk


# ─────────────────────────────────────
# CREATE SECTION HELPER
# ─────────────────────────────────────
# Creates a styled frame section with a title for organizing settings


def create_section(parent, title):
    """
    Create a styled frame section with a title.
    
    Args:
        parent: The parent widget to attach the section to
        title: The title text to display for this section
    
    Returns:
        A CTkFrame widget containing the section
    """

    # Create frame with rounded corners
    frame = ctk.CTkFrame(
        parent,
        corner_radius=18,
    )

    # Pack frame to fill horizontal space with padding
    frame.pack(
        fill="x",
        padx=20,
        pady=10,
    )

    # Add section title label
    ctk.CTkLabel(
        frame,
        text=title,
        font=("Arial", 18, "bold"),
    ).pack(
        anchor="w",
        padx=18,
        pady=(16, 12),
    )

    return frame


# ─────────────────────────────────────
# OPEN SETTINGS WINDOW
# ─────────────────────────────────────
# Opens the main settings dialog with all configuration options


def open_settings(
    root,
    config,
    save_config,
):
    """
    Open the settings window for configuring application preferences.
    
    Args:
        root: The main application window
        config: The configuration dictionary
        save_config: Function to save configuration changes
    """

    # Create new top-level window for settings
    win = ctk.CTkToplevel(root)

    win.title("Settings")

    win.geometry("560x720")

    win.resizable(False, False)


    # ─────────────────────────────────────
    # TITLE
    # ─────────────────────────────────────

    ctk.CTkLabel(
        win,
        text="Settings",
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    # ─────────────────────────────────────
    # LANGUAGE SECTION
    # ─────────────────────────────────────

    language = create_section(
        win,
        "Language",
    )

    # Variable to store selected language
    lang_var = tk.StringVar(
        value=config.get(
            "language",
            "en",
        )
    )

    def change_language():
        """Update language setting and save configuration."""
        config["language"] = lang_var.get()
        save_config()

    ctk.CTkLabel(
        language,
        text="Select Language",
        font=("Arial", 14),
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 8),
    )

    ctk.CTkOptionMenu(
        language,
        values=["English", "Deutsch"],
        variable=lang_var,
        command=change_language,
        height=42,
    ).pack(
        fill="x",
        padx=22,
        pady=(0, 20),
    )


    # ─────────────────────────────────────
    # APPEARANCE SECTION
    # ─────────────────────────────────────

    appearance = create_section(
        win,
        "Appearance",
    )


    # Dark mode toggle variable
    dark_var = tk.BooleanVar(
        value=config.get(
            "darkmode",
            True,
        )
    )


    def toggle_dark():
        """Toggle dark mode and apply theme change."""
        config["darkmode"] = dark_var.get()

        ctk.set_appearance_mode(
            "dark"
            if config["darkmode"]
            else "light"
        )

        save_config()


    ctk.CTkCheckBox(
        appearance,
        text="Enable Dark Mode",
        variable=dark_var,
        command=toggle_dark,
        checkbox_width=24,
        checkbox_height=24,
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 16),
    )


    # ─────────────────────────────────────
    # TASKS SECTION
    # ─────────────────────────────────────

    tasks = create_section(
        win,
        "Tasks",
    )


    # Show completed tasks toggle variable
    done_var = tk.BooleanVar(
        value=config.get(
            "show_done",
            True,
        )
    )


    def toggle_done():
        """Toggle visibility of completed tasks."""
        config["show_done"] = done_var.get()

        save_config()


    ctk.CTkCheckBox(
        tasks,
        text="Show Completed Tasks",
        variable=done_var,
        command=toggle_done,
        checkbox_width=24,
        checkbox_height=24,
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 16),
    )


    # ─────────────────────────────────────
    # GOOGLE CALENDAR SECTION
    # ─────────────────────────────────────

    calendar = create_section(
        win,
        "Google Calendar",
    )


    # Google sync toggle variable
    google_var = tk.BooleanVar(
        value=config.get(
            "google_sync",
            False,
        )
    )


    def toggle_google():
        """Toggle Google Calendar synchronization."""
        config["google_sync"] = google_var.get()

        save_config()


    ctk.CTkCheckBox(
        calendar,
        text="Sync Tasks With Google Calendar",
        variable=google_var,
        command=toggle_google,
        checkbox_width=24,
        checkbox_height=24,
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 8),
    )

    # Note about contacting developer for Google Calendar feature
    ctk.CTkLabel(
        calendar,
        text="Contact the developer if you want to use this feature.",
        font=("Arial", 12),
        text_color="gray",
        justify="left",
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 18),
    )


    # Reminder time mapping (text to minutes)
    reminder_map = {
        "5 Minutes Before": 5,
        "15 Minutes Before": 15,
        "1 Hour Before": 60,
        "1 Day Before": 1440,
        "1 Week Before": 10080,
    }


    # Reverse mapping (minutes to text)
    reverse_map = {
        v: k
        for k, v in reminder_map.items()
    }


    # Variable for selected reminder time
    reminder_var = tk.StringVar(
        value=reverse_map.get(
            config.get(
                "reminder_minutes",
                1440,
            ),
            "1 Day Before",
        )
    )


    def change_reminder(choice):
        """Update reminder time setting."""
        config["reminder_minutes"] = reminder_map[choice]

        save_config()


    ctk.CTkLabel(
        calendar,
        text="Reminder Before Deadline",
        font=("Arial", 14),
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 8),
    )


    ctk.CTkOptionMenu(
        calendar,
        values=list(reminder_map.keys()),
        variable=reminder_var,
        command=change_reminder,
        height=42,
    ).pack(
        fill="x",
        padx=22,
        pady=(0, 20),
    )


    # ─────────────────────────────────────
    # ARTIFICIAL INTELLIGENCE SECTION
    # ─────────────────────────────────────

    ai = create_section(
        win,
        "Artificial Intelligence",
    )


    # Information label about AI usage
    ai_label = ctk.CTkLabel(
        ai,
        text=(
            "TaskSorter uses a local AI model\n"
            "for intelligent task extraction."
        ),
        justify="left",
        text_color="gray",
        font=("Arial", 14),
    )

    ai_label.pack(
        anchor="w",
        padx=22,
        pady=(0, 18),
    )


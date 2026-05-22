# File: ui/settings_window.py
# Settings window for TaskSorter AI application
# Allows users to configure appearance, tasks, Google Calendar, and AI settings
# Note: All UI text is in English for international compatibility


import customtkinter as ctk
import tkinter as tk
import webbrowser


# ─────────────────────────────────────
# SETTINGS CONSTANTS
# ─────────────────────────────────────
# Defines all text labels and options used in the settings window

# Reminder time options displayed to the user
REMINDER_OPTIONS = [
    "5 Minutes Before",
    "15 Minutes Before",
    "1 Hour Before",
    "1 Day Before",
    "1 Week Before",
]

# Maps reminder text to minutes before deadline
REMINDER_MINUTES = {
    "5 Minutes Before": 5,
    "15 Minutes Before": 15,
    "1 Hour Before": 60,
    "1 Day Before": 1440,
    "1 Week Before": 10080,
}


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
    refresh_ui_callback=None,
):
    """
    Open the settings window for configuring application preferences.
    
    Args:
        root: The main application window
        config: The configuration dictionary
        save_config: Function to save configuration changes
        refresh_ui_callback: Optional callback to refresh UI after settings change
    """

    # Create new top-level window for settings
    win = ctk.CTkToplevel(root)

    win.title("Settings")

    # Window size adjusted to fit all content comfortably
    win.geometry("600x720")

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

    # Highlighted note about contacting developer for Google Calendar feature
    contact_frame = ctk.CTkFrame(
        calendar,
        fg_color="#FF6B35",  # Red-orange background for high visibility
        corner_radius=10,
        border_width=2,
        border_color="#CC4400",
    )
    contact_frame.pack(
        fill="x",
        padx=22,
        pady=(0, 18),
    )
    
    ctk.CTkLabel(
        contact_frame,
        text="⚠️  IMPORTANT: Contact the developer to enable this feature!",
        font=("Arial", 14, "bold"),
        text_color="white",
        justify="center",
        wraplength=450,
    ).pack(
        padx=15,
        pady=(12, 6),
    )
    
    # Developer contact information
    ctk.CTkLabel(
        contact_frame,
        text="📧 Ivan Pejic\n✉️ ivan.pejic@htl-wels.at\n✉️ pivane8@gmail.com",
        font=("Arial", 13, "bold"),
        text_color="white",
        justify="center",
        wraplength=450,
    ).pack(
        padx=15,
        pady=(0, 12),
    )


    # Variable for selected reminder time
    # Maps minutes to display text
    reverse_map = {
        v: k
        for k, v in REMINDER_MINUTES.items()
    }

    reminder_var = tk.StringVar(
        value=reverse_map.get(
            config.get(
                "reminder_minutes",
                1440,
            ),
            "1 Day Before",  # Default reminder time
        )
    )


    def change_reminder(choice):
        """Update reminder time setting."""
        config["reminder_minutes"] = REMINDER_MINUTES[choice]

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
        values=REMINDER_OPTIONS,
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
        text="TaskSorter uses a local AI model\nfor intelligent task extraction.",
        justify="left",
        text_color="gray",
        font=("Arial", 14),
    )

    ai_label.pack(
        anchor="w",
        padx=22,
        pady=(0, 18),
    )


# File: ui/settings_window.py
# Settings window for TaskSorter AI application
# Allows users to configure appearance, tasks, Google Calendar, and AI settings


import customtkinter as ctk
import tkinter as tk
import webbrowser


# ─────────────────────────────────────
# TRANSLATIONS DICTIONARY
# ─────────────────────────────────────
# Contains all UI text translations for English and German

TRANSLATIONS = {
    "en": {
        "title": "Settings",
        "language_section": "Language",
        "select_language": "Select Language",
        "appearance_section": "Appearance",
        "dark_mode": "Enable Dark Mode",
        "tasks_section": "Tasks",
        "show_completed": "Show Completed Tasks",
        "calendar_section": "Google Calendar",
        "sync_tasks": "Sync Tasks With Google Calendar",
        "contact_dev_warning": "⚠️  IMPORTANT: Contact the developer to enable this feature!",
        "developer_contact": "📧 Ivan Pejic\n✉️ ivan.pejic@htl-wels.at\n✉️ pivane8@gmail.com",
        "reminder_label": "Reminder Before Deadline",
        "ai_section": "Artificial Intelligence",
        "ai_info": "TaskSorter uses a local AI model\nfor intelligent task extraction.",
        "languages": ["English", "Deutsch"],
        "reminders": [
            "5 Minutes Before",
            "15 Minutes Before",
            "1 Hour Before",
            "1 Day Before",
            "1 Week Before",
        ],
    },
    "de": {
        "title": "Einstellungen",
        "language_section": "Sprache",
        "select_language": "Sprache auswählen",
        "appearance_section": "Erscheinungsbild",
        "dark_mode": "Dunklen Modus aktivieren",
        "tasks_section": "Aufgaben",
        "show_completed": "Erledigte Aufgaben anzeigen",
        "calendar_section": "Google Kalender",
        "sync_tasks": "Aufgaben mit Google Kalender synchronisieren",
        "contact_dev_warning": "⚠️  WICHTIG: Kontaktieren Sie den Entwickler, um diese Funktion zu aktivieren!",
        "developer_contact": "📧 Ivan Pejic\n✉️ ivan.pejic@htl-wels.at\n✉️ pivane8@gmail.com",
        "reminder_label": "Erinnerung vor Frist",
        "ai_section": "Künstliche Intelligenz",
        "ai_info": "TaskSorter verwendet ein lokales KI-Modell\nfür intelligente Aufgabenerkennung.",
        "languages": ["English", "Deutsch"],
        "reminders": [
            "5 Minuten vorher",
            "15 Minuten vorher",
            "1 Stunde vorher",
            "1 Tag vorher",
            "1 Woche vorher",
        ],
    },
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
        refresh_ui_callback: Optional callback to refresh UI after language change
    """

    # Get current language for translations
    lang_code = config.get("language", "en")
    t = TRANSLATIONS.get(lang_code, TRANSLATIONS["en"])

    # Create new top-level window for settings
    win = ctk.CTkToplevel(root)

    win.title(t["title"])

    # Increased window size to fit all content
    win.geometry("600x780")

    win.resizable(False, False)


    # ─────────────────────────────────────
    # TITLE
    # ─────────────────────────────────────

    ctk.CTkLabel(
        win,
        text=t["title"],
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    # ─────────────────────────────────────
    # LANGUAGE SECTION
    # ─────────────────────────────────────

    language_frame = create_section(
        win,
        t["language_section"],
    )

    # Mapping between display names and config values
    lang_display_map = {
        "English": "en",
        "Deutsch": "de",
    }
    
    # Reverse mapping for displaying current selection
    lang_reverse_map = {v: k for k, v in lang_display_map.items()}

    # Variable to store selected language (display name)
    current_lang_code = config.get("language", "en")
    current_lang_display = lang_reverse_map.get(current_lang_code, "English")
    
    lang_var = tk.StringVar(value=current_lang_display)

    def change_language(selected_value):
        """Update language setting and save configuration."""
        # Convert display name to config value
        config["language"] = lang_display_map.get(selected_value, "en")
        save_config()
        # Refresh UI if callback provided
        if refresh_ui_callback:
            refresh_ui_callback()

    ctk.CTkLabel(
        language_frame,
        text=t["select_language"],
        font=("Arial", 14),
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 8),
    )

    ctk.CTkOptionMenu(
        language_frame,
        values=t["languages"],
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
        t["appearance_section"],
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
        text=t["dark_mode"],
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
        t["tasks_section"],
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
        text=t["show_completed"],
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
        t["calendar_section"],
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
        text=t["sync_tasks"],
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
        text=t["contact_dev_warning"],
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
        text=t["developer_contact"],
        font=("Arial", 13, "bold"),
        text_color="white",
        justify="center",
        wraplength=450,
    ).pack(
        padx=15,
        pady=(0, 12),
    )


    # Reminder time mapping (text to minutes)
    reminder_map = {
        "5 Minutes Before": 5,
        "15 Minutes Before": 15,
        "1 Hour Before": 60,
        "1 Day Before": 1440,
        "1 Week Before": 10080,
    }
    
    # German reminder mapping
    reminder_map_de = {
        "5 Minuten vorher": 5,
        "15 Minuten vorher": 15,
        "1 Stunde vorher": 60,
        "1 Tag vorher": 1440,
        "1 Woche vorher": 10080,
    }


    # Select appropriate reminder map based on language
    if lang_code == "de":
        current_reminder_map = reminder_map_de
    else:
        current_reminder_map = reminder_map


    # Reverse mapping (minutes to text)
    reverse_map = {
        v: k
        for k, v in current_reminder_map.items()
    }


    # Variable for selected reminder time
    reminder_var = tk.StringVar(
        value=reverse_map.get(
            config.get(
                "reminder_minutes",
                1440,
            ),
            list(current_reminder_map.keys())[3],  # Default to "1 Day Before" or equivalent
        )
    )


    def change_reminder(choice):
        """Update reminder time setting."""
        config["reminder_minutes"] = current_reminder_map[choice]

        save_config()


    ctk.CTkLabel(
        calendar,
        text=t["reminder_label"],
        font=("Arial", 14),
    ).pack(
        anchor="w",
        padx=22,
        pady=(0, 8),
    )


    ctk.CTkOptionMenu(
        calendar,
        values=list(current_reminder_map.keys()),
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
        t["ai_section"],
    )


    # Information label about AI usage
    ai_label = ctk.CTkLabel(
        ai,
        text=t["ai_info"],
        justify="left",
        text_color="gray",
        font=("Arial", 14),
    )

    ai_label.pack(
        anchor="w",
        padx=22,
        pady=(0, 18),
    )


# File: ui/settings_window.py
# Settings window for TaskSorter AI application
# Allows users to configure appearance, tasks, Google Calendar, and AI settings
# Note: All UI text is in English for international compatibility


import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
import webbrowser
# CHANGE: Windows/Linux icon compatibility fix
from ui.window_utils import (
    apply_app_icon,
    fit_scrollable_frame_to_content,
    fit_window_after_idle,
    fit_window_to_content,
)


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
    restart_callback=None,
):
    """
    Open the settings window for configuring application preferences.
    
    Args:
        root: The main application window
        config: The configuration dictionary
        save_config: Function to save configuration changes
        refresh_ui_callback: Optional callback to refresh UI after settings change
        restart_callback: Optional callback to restart the application
    """

    # Create new top-level window for settings
    win = ctk.CTkToplevel(root)

    # CHANGE: Delayed window initialization
    win.withdraw()
    # CHANGE: Window hierarchy management
    win.transient(root)

    win.title("Settings")

    # CHANGE: Removed fixed window dimensions
    # CHANGE: Windows/Linux icon compatibility fix
    apply_app_icon(win)


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

    # CHANGE: Dynamic window sizing fix
    content = ctk.CTkScrollableFrame(
        win,
        fg_color="transparent",
    )

    # CHANGE: Dynamic window sizing fix
    content.pack(
        fill="both",
        expand=True,
        padx=0,
        pady=(0, 16),
    )

    appearance = create_section(
        content,
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
        """
        Toggle dark mode preference.

        No live theme switch is performed. CustomTkinter's
        set_appearance_mode() triggers synchronous full-widget redraw
        on every window, which conflicts with the modal event loop of
        the settings dialog (grab_set), causing a freeze.

        Instead:
        1. Save the preference to config.
        2. Ask the user to restart.
        3. On confirmation, restart the application automatically.
        4. The new theme is applied at startup via ctk.set_appearance_mode().
        """

        config["darkmode"] = dark_var.get()

        save_config()

        # CHANGE: Theme change requires restart - inform user and restart on confirmation
        confirm = messagebox.askyesno(
            "Theme Change",
            "Theme changes require an application restart.\n\nTaskSorter will now restart.",
            parent=win,
        )

        if confirm:
            # Release modal grab before destroying the settings window
            win.grab_release()
            win.destroy()
            root.focus_set()

            # Restart the application (new process loads the new theme)
            if restart_callback:
                restart_callback()


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

    # CHANGE: Dynamic window sizing fix
    tasks = create_section(
        content,
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

        # CHANGE: Bug audit fix - trigger UI refresh so task list updates
        if refresh_ui_callback:
            refresh_ui_callback()


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

    # CHANGE: Dynamic window sizing fix
    calendar = create_section(
        content,
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
        # CHANGE: Dynamic window sizing fix
        wraplength=360,
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
        # CHANGE: Dynamic window sizing fix
        wraplength=360,
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

    # CHANGE: Dynamic window sizing fix
    ai = create_section(
        content,
        "Artificial Intelligence",
    )


    # Program info section with features and project info
    program_info_frame = ctk.CTkFrame(
        ai,
        fg_color="transparent",
        border_width=0,
    )
    program_info_frame.pack(
        fill="x",
        padx=22,
        pady=(0, 10),
    )

    program_title = ctk.CTkLabel(
        program_info_frame,
        text="TaskSorter AI",
        font=("Arial", 18, "bold"),
    )
    program_title.pack(pady=(5, 5))

    program_description = ctk.CTkLabel(
        program_info_frame,
        text="Organise tasks smarter with AI.\n\n"
             "• Automatic task recognition\n"
             "• Deadline detection\n"
             "• Priority sorting\n"
             "• Google Calendar integration\n\n"
             "Developed for the HTL ITP Project 2025/26.",
        font=("Arial", 13),
        justify="center",
    )
    program_description.pack(pady=(0, 10))


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

    # ─────────────────────────────────────
    # CLOSE BUTTON
    # ─────────────────────────────────────

    ctk.CTkButton(
        win,
        text="Close",
        height=45,
        width=200,
        font=("Arial", 16, "bold"),
        # CHANGE: Parent-child focus handling
        command=lambda: on_settings_closing(),
    ).pack(
        pady=(0, 24),
    )

    # CHANGE: Parent-child focus handling
    def on_settings_closing():
        win.grab_release()
        win.destroy()
        root.focus_set()

    win.protocol("WM_DELETE_WINDOW", on_settings_closing)

    # CHANGE: Added automatic geometry calculation
    fit_scrollable_frame_to_content(
        content,
        min_height=260,
        max_height_ratio=0.68,
    )

    # CHANGE: Delayed window initialization - show after all widgets created
    win.update_idletasks()
    fit_window_to_content(
        win,
        min_width=460,
        min_height=420,
        max_width_ratio=0.85,
        max_height_ratio=0.9,
    )
    win.deiconify()
    # CHANGE: Modal dialog behavior
    win.grab_set()
    win.focus_set()

    # CHANGE: Added automatic geometry calculation
    fit_window_after_idle(
        win,
        min_width=460,
        min_height=420,
        max_width_ratio=0.85,
        max_height_ratio=0.9,
    )

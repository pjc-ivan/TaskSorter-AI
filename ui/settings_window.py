# File: ui/settings_window.py

import customtkinter as ctk
import tkinter as tk


# ─────────────────────────────────────
# SECTION
# ─────────────────────────────────────


def create_section(parent, title):

    frame = ctk.CTkFrame(
        parent,
        corner_radius=18,
    )

    frame.pack(
        fill="x",
        padx=20,
        pady=10,
    )

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
# SETTINGS WINDOW
# ─────────────────────────────────────


def open_settings(
    root,
    config,
    save_config,
):

    win = ctk.CTkToplevel(root)

    win.title("Settings")

    win.geometry("560x650")

    win.resizable(False, False)


    # TITLE

    ctk.CTkLabel(
        win,
        text="Settings",
        font=("Arial", 28, "bold"),
    ).pack(
        pady=(24, 18)
    )


    # ─────────────────────────────────────
    # APPEARANCE
    # ─────────────────────────────────────


    appearance = create_section(
        win,
        "Appearance",
    )


    dark_var = tk.BooleanVar(
        value=config.get(
            "darkmode",
            True,
        )
    )


    def toggle_dark():

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
    # TASKS
    # ─────────────────────────────────────


    tasks = create_section(
        win,
        "Tasks",
    )


    done_var = tk.BooleanVar(
        value=config.get(
            "show_done",
            True,
        )
    )


    def toggle_done():

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
    # GOOGLE CALENDAR
    # ─────────────────────────────────────


    calendar = create_section(
        win,
        "Google Calendar",
    )


    google_var = tk.BooleanVar(
        value=config.get(
            "google_sync",
            True,
        )
    )


    def toggle_google():

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
        pady=(0, 18),
    )


    reminder_map = {
        "5 Minutes Before": 5,
        "15 Minutes Before": 15,
        "1 Hour Before": 60,
        "1 Day Before": 1440,
        "1 Week Before": 10080,
    }


    reverse_map = {
        v: k
        for k, v in reminder_map.items()
    }


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
    # AI
    # ─────────────────────────────────────


    ai = create_section(
        win,
        "Artificial Intelligence",
    )


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


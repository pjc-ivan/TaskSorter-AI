# File: ui/window_utils.py


# CHANGE: Windows/Linux icon compatibility fix
import os
import sys
import tkinter as tk


# CHANGE: Fixed task persistence - consistent user data directory for all platforms
def get_data_dir():
    """
    Return a writable directory for user data (tasks.json, token.json, config.json).
    Windows:  %%APPDATA%%\\TaskSorter
    Linux:    ~/.local/share/TaskSorter
    """

    if os.name == "nt":
        base = os.environ.get("APPDATA", os.path.expanduser("~"))
    else:
        base = os.environ.get(
            "XDG_DATA_HOME",
            os.path.join(os.path.expanduser("~"), ".local", "share"),
        )

    data_dir = os.path.join(base, "TaskSorter")

    try:
        os.makedirs(data_dir, exist_ok=True)
    except Exception:
        pass

    return data_dir


# CHANGE: Fixed file path handling - resolve bundled assets in dev or PyInstaller
def resource_path(relative_path):
    """
    Resolve asset paths in development and in PyInstaller executables.
    """

    # CHANGE: Windows/Linux icon compatibility fix
    base_path = getattr(
        sys,
        "_MEIPASS",
        os.path.abspath("."),
    )

    # CHANGE: Windows/Linux icon compatibility fix
    return os.path.join(
        base_path,
        relative_path,
    )


# CHANGE: Windows/Linux icon compatibility fix
def set_windows_app_user_model_id():
    """
    Set a Windows AppUserModelID so the packaged executable uses the app icon in the taskbar.
    """

    # CHANGE: Windows/Linux icon compatibility fix
    if os.name != "nt":
        return

    try:

        # CHANGE: Windows/Linux icon compatibility fix
        import ctypes

        # CHANGE: Windows/Linux icon compatibility fix
        ctypes.windll.shell32.SetCurrentProcessExplicitAppUserModelID(
            "TaskSorter.TaskSorterAI.1"
        )

    except Exception as e:

        print(e)


# CHANGE: Shared icon handling - protect against customtkinter icon override
def apply_app_icon(window):
    """
    Apply the application icon with platform-specific Tk methods.
    Prevents customtkinter from overriding the icon on CTkToplevel windows.
    """

    # CHANGE: Cross-platform icon support
    ico_path = resource_path(
        "assets/icon.ico"
    )

    # CHANGE: Cross-platform icon support
    png_path = resource_path(
        "assets/icon.png"
    )

    try:

        # CHANGE: Cross-platform icon support
        if os.name == "nt" and os.path.exists(ico_path):
            window.iconbitmap(ico_path)

    except Exception as e:

        print(e)

    try:

        # CHANGE: Cross-platform icon support
        if os.path.exists(png_path):
            icon = tk.PhotoImage(
                file=png_path
            )

            # CHANGE: Cross-platform icon support
            window.iconphoto(
                True,
                icon,
            )

            # CHANGE: Cross-platform icon support
            window._icon_image = icon

    except Exception as e:

        print(e)

    # CHANGE: Apply icon to Toplevel window - prevent customtkinter override
    window._iconbitmap_method_called = True

    # CHANGE: CTkToplevel unconditionally sets its own icon after 200ms
    # on Windows. Re-apply our icon after that to ensure it stays.
    if os.name == "nt":
        window.after(300, lambda: _reapply_icon(window))


# CHANGE: Shared icon handling - re-apply after customtkinter deferred callback
def _reapply_icon(window):
    try:
        ico_path = resource_path("assets/icon.ico")
        if os.path.exists(ico_path):
            window.iconbitmap(ico_path)
        png_path = resource_path("assets/icon.png")
        if os.path.exists(png_path):
            icon = tk.PhotoImage(file=png_path)
            window.iconphoto(True, icon)
            window._icon_image = icon
    except Exception:
        pass


# CHANGE: Added automatic geometry calculation
def fit_window_to_content(
    window,
    min_width=360,
    min_height=260,
    max_width_ratio=0.9,
    max_height_ratio=0.9,
    extra_width=24,
    extra_height=24,
):
    """
    Size a window from its requested content size while keeping it inside the screen.
    """

    # CHANGE: Added automatic geometry calculation
    window.update_idletasks()

    # CHANGE: Added automatic geometry calculation
    screen_width = window.winfo_screenwidth()

    # CHANGE: Added automatic geometry calculation
    screen_height = window.winfo_screenheight()

    # CHANGE: Added automatic geometry calculation
    max_width = max(
        min_width,
        int(screen_width * max_width_ratio),
    )

    # CHANGE: Added automatic geometry calculation
    max_height = max(
        min_height,
        int(screen_height * max_height_ratio),
    )

    # CHANGE: Added automatic geometry calculation
    width = min(
        max(
            window.winfo_reqwidth() + extra_width,
            min_width,
        ),
        max_width,
    )

    # CHANGE: Added automatic geometry calculation
    height = min(
        max(
            window.winfo_reqheight() + extra_height,
            min_height,
        ),
        max_height,
    )

    # CHANGE: Added automatic geometry calculation
    x = max(
        0,
        (screen_width - width) // 2,
    )

    # CHANGE: Added automatic geometry calculation
    y = max(
        0,
        (screen_height - height) // 2,
    )

    # CHANGE: Added automatic geometry calculation
    window.geometry(
        f"{width}x{height}+{x}+{y}"
    )

    # CHANGE: Dynamic window sizing fix
    window.minsize(
        min_width,
        min_height,
    )

    # CHANGE: Dynamic window sizing fix
    window.maxsize(
        max_width,
        max_height,
    )


# CHANGE: Added automatic geometry calculation
def fit_window_after_idle(
    window,
    **kwargs,
):
    """
    Defer content fitting until Tk has calculated all widget sizes.
    """

    # CHANGE: Added automatic geometry calculation
    window.after(
        0,
        lambda: fit_window_to_content(
            window,
            **kwargs,
        ),
    )


# CHANGE: Added automatic geometry calculation
def fit_scrollable_frame_to_content(
    scrollable_frame,
    min_height=180,
    max_height_ratio=0.7,
):
    """
    Give scrollable content enough height for its children without exceeding the screen.
    """

    # CHANGE: Added automatic geometry calculation
    scrollable_frame.update_idletasks()

    # CHANGE: Added automatic geometry calculation
    content_height = sum(
        child.winfo_reqheight()
        for child in scrollable_frame.winfo_children()
    )

    # CHANGE: Added automatic geometry calculation
    screen_height = scrollable_frame.winfo_screenheight()

    # CHANGE: Added automatic geometry calculation
    max_height = int(
        screen_height * max_height_ratio
    )

    # CHANGE: Added automatic geometry calculation
    scrollable_frame.configure(
        height=min(
            max(
                content_height,
                min_height,
            ),
            max_height,
        )
    )


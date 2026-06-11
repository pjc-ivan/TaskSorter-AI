# -*- mode: python ; coding: utf-8 -*-
# File: TaskSorter.spec
# Production-ready PyInstaller build specification for TaskSorter AI
#
# Build command:
#   pyinstaller TaskSorter.spec --clean
#
# ── Bundled data files ──────────────────────────────
#   assets/icon.ico           Windows titlebar/taskbar icon (iconbitmap)
#   assets/icon.png           Linux/macOS window icon (tk.PhotoImage)
#   assets/icon21.png         Alternative PNG icon (legacy support)
#   assets/icon22.ico         Alternative ICO icon (legacy support)
#   config.json               Application defaults (bundled, copied to user dir)
#   credentials.json          Google Calendar OAuth client secrets
#   customtkinter/assets/     Theme .json, fonts, shared icons (runtime assets)
#   de_core_news_sm/          spaCy German NLP model data (offline fallback)
#
# ── Hidden imports (dynamically loaded at runtime) ──
#   googleapiclient.discovery           build() for Calendar API v3
#   google_auth_oauthlib.flow           OAuth 2.0 InstalledAppFlow
#   google.auth.transport.requests      Token refresh via Request()
#   spacy                               NLP library (optional offline fallback)
#   de_core_news_sm                     German model for spacy.load()
#   spacy.lang.de                       German language pipeline data
#   ollama                              LLM backend for AI task parsing
#   dateparser                          Natural-language date parsing
#   pytz                                Timezone data (dateparser requirement)
#   tzlocal                             Local timezone detection (dateparser)
#   darkdetect                          System theme detection (customtkinter)


import os
from PyInstaller.utils.hooks import collect_data_files


# ── Project assets ──────────────────────────────────
extra_datas = [
    ('assets/icon.ico', 'assets'),
    ('assets/icon.png', 'assets'),
    ('assets/icon21.png', 'assets'),
    ('assets/icon22.ico', 'assets'),
    ('config.json', '.'),
    ('credentials.json', '.'),
]

# ── CustomTkinter theme assets (fonts, icons, themes) ──
# CHANGE: EXE build support - bundle CustomTkinter runtime assets
try:
    ctk_datas = collect_data_files('customtkinter')
    extra_datas.extend(ctk_datas)
except Exception:
    pass

# ── spaCy German model data files ───────────────────
# CHANGE: EXE build support - bundle de_core_news_sm model data
try:
    model_datas = collect_data_files('de_core_news_sm')
    extra_datas.extend(model_datas)
except Exception:
    pass


a = Analysis(
    ['TaskSorter.py'],
    pathex=[],
    binaries=[],
    datas=extra_datas,
    hiddenimports=[
        # Google Calendar
        'googleapiclient.discovery',
        'google_auth_oauthlib.flow',
        'google.auth.transport.requests',
        # spaCy NLP (optional offline fallback)
        'spacy',
        'de_core_news_sm',
        'spacy.lang.de',
        # Ollama AI
        'ollama',
        # Date parser
        'dateparser',
        'pytz',
        'tzlocal',
        # CustomTkinter system theme detection
        # CHANGE: EXE build support - darkdetect needed by customtkinter
        'darkdetect',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[
        # CHANGE: EXE build support - exclude unnecessary modules to reduce size
        'tkinter.test',
        'unittest',
        'pdb',
        'test',
    ],
    noarchive=False,
    optimize=0,
)

pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='TaskSorter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=False,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='assets/icon.ico',
)

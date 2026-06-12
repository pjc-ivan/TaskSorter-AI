# TaskSorter AI

TaskSorter AI is a desktop task management application developed as a software engineering project at HTL Wels.

The application helps students organize their tasks by automatically detecting deadlines and priorities from natural language input. Tasks can optionally be synchronized with Google Calendar to receive reminders on multiple devices.

---

# Features

* Create, edit and delete tasks
* Automatic task sorting by deadline and priority
* AI-supported task recognition from natural language input
* Automatic due date detection
* Priority detection
* Task notes
* Google Calendar synchronization
* Dark mode support
* Local data storage
* Linux desktop integration
* Offline AI processing after installation

---

# Download

Latest release:

OneDrive Project Files:

https://office365htlwels-my.sharepoint.com/:f:/g/personal/ivan_pejic_htl-wels_at/IgAQLv4Gx029RYun7jW-zDIBAR584Qua2ATm_By39x8G9Yw?e=V5YMip

---

# Requirements

Linux:

* Python 3
* sudo permissions
* Internet connection for initial installation

Windows:

* Use the provided installer package from the release folder.

---

# Linux Installation

Open a terminal inside the TaskSorter directory.

Make the installer executable:

```bash
chmod +x install_linux.sh
```

Start the installation:

```bash
./install_linux.sh
```

The installer automatically:

* Installs Python dependencies
* Installs Ollama
* Downloads the AI model
* Installs the German spaCy language model
* Creates a desktop application entry
* Creates the virtual environment

---

# Starting TaskSorter

After installation you can start TaskSorter either from the application menu:

```text
TaskSorter AI
```

or manually:

```bash
./run.sh
```

---

# AI System

TaskSorter AI uses a locally running AI model through Ollama.

Technologies:

* Ollama
* Gemma 3 1B
* spaCy NLP

Example input:

```text
I have to finish the math homework by tomorrow. It is important.
```

Detected information:

```text
Task: Math homework
Due date: Tomorrow
Priority: High
```

All AI processing runs locally on the device after installation.

---

# Google Calendar Synchronization

TaskSorter can synchronize tasks with Google Calendar.

Requirements:

* Google account
* credentials.json file provided by the developer

During the first synchronization process a Google login window will open automatically.

Note:

Google Calendar integration is only available when the required Google API credentials have been provided by the developer.

---

# Project Structure

```text
TaskSorter
│
├── assets/
├── ui/
├── TaskSorter.py
├── task_ai.py
├── task_parser.py
├── task_storage.py
├── config_manager.py
├── calendar_sync.py
├── install_linux.sh
├── run.sh
└── README.md
```

---

# Technologies

* Python
* CustomTkinter
* Ollama
* Gemma 3
* spaCy
* Google Calendar API

---

# Data Storage

User data is stored locally on the device.

Linux:

```text
~/.local/share/TaskSorter/
```

Windows:

```text
%APPDATA%\TaskSorter\
```

---

# Authors

Developed by:

* Ivan Pejic
* Lukas Sokic
* Leo Fichtner

HTL Wels

Software Engineering Project 2025/2026

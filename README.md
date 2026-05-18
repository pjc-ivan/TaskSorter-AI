# TaskSorter AI

TaskSorter AI is a task management application developed as a school project.

The application allows users to:

* create and manage tasks
* automatically sort tasks by deadline and priority
* synchronize tasks with Google Calendar
* use local AI for intelligent task recognition
* add notes to tasks
* edit and complete tasks

The AI system uses a local Ollama language model and works offline after installation.

---

# Features

* AI-based task extraction
* Automatic date recognition
* Priority management
* Google Calendar synchronization
* Notes for tasks
* Modern graphical interface
* Offline AI support
* Linux application menu integration

---

# Requirements

Linux distribution with:

* Python 3
* sudo permissions
* internet connection for first installation

---

# Installation

Open terminal inside the project folder.

Make the installer executable:

```bash
chmod +x install_linux.sh
```

Run the installer:

```bash
./install_linux.sh
```

The installer automatically:

* installs Python dependencies
* installs Ollama
* downloads the AI model
* installs spaCy language data
* creates the application menu entry

---

# Starting The Application

After installation:

From Linux application menu:

```text
TaskSorter AI
```

Or manually:

```bash
./run.sh
```

---

# AI System

TaskSorter AI uses:

* Ollama
* gemma3:1b
* spaCy NLP

The AI system extracts:

* task title
* due date
* priority
* notes

Example:

Input:

```text
Ich muss bis morgen dringend die Mathe Hausübung machen
```

Output:

```text
Mathe Hausübung
```

---

# Google Calendar

Google Calendar synchronization requires:

* credentials.json

On first start, Google authentication will open automatically.

---

# Project Structure

```text
TaskSorter/
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
└── README.md
```

---

# Technologies

* Python
* CustomTkinter
* Ollama
* spaCy
* Google Calendar API

---

# Authors

TaskSorter AI was developed as part of a HTL software engineering school project.

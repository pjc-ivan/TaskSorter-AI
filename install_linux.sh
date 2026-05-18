#!/bin/bash

echo ""
echo "Installing TaskSorter AI..."
echo ""

# ─────────────────────────────────────
# SYSTEM UPDATE
# ─────────────────────────────────────

sudo dnf update -y

# ─────────────────────────────────────
# PYTHON
# ─────────────────────────────────────

sudo dnf install python3 -y
sudo dnf install python3-pip -y
sudo dnf install python3-virtualenv -y

# ─────────────────────────────────────
# OLLAMA
# ─────────────────────────────────────

curl -fsSL https://ollama.com/install.sh | sh

# START OLLAMA

systemctl --user enable ollama
systemctl --user start ollama

sleep 5

# ─────────────────────────────────────
# AI MODEL
# ─────────────────────────────────────

ollama pull gemma3:1b

# ─────────────────────────────────────
# VIRTUAL ENVIRONMENT
# ─────────────────────────────────────

python3 -m venv venv

source venv/bin/activate

# ─────────────────────────────────────
# PYTHON PACKAGES
# ─────────────────────────────────────

pip install --upgrade pip

pip install customtkinter
pip install dateparser
pip install ollama
pip install spacy
pip install google-api-python-client
pip install google-auth-httplib2
pip install google-auth-oauthlib

# ─────────────────────────────────────
# SPACY MODEL
# ─────────────────────────────────────

python -m spacy download de_core_news_sm

# ─────────────────────────────────────
# RUN SCRIPT
# ─────────────────────────────────────

cat > run.sh <<EOL
#!/bin/bash

cd "$(pwd)"

source venv/bin/activate

python TaskSorter.py
EOL

chmod +x run.sh

# ─────────────────────────────────────
# APPLICATION MENU ENTRY
# ─────────────────────────────────────

cat > TaskSorterAI.desktop <<EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=TaskSorter AI
Comment=AI powered task management

Exec=$(pwd)/run.sh

Path=$(pwd)

Icon=$(pwd)/assets/icon.png

Terminal=false

Categories=Utility;

StartupNotify=true
EOL

chmod +x TaskSorterAI.desktop

mkdir -p ~/.local/share/applications

cp TaskSorterAI.desktop ~/.local/share/applications/

update-desktop-database ~/.local/share/applications

# ─────────────────────────────────────
# FINISHED
# ─────────────────────────────────────

echo ""
echo "Installation complete."
echo ""
echo "You can now start TaskSorter AI from:"
echo "- Linux Application Menu"
echo "- ./run.sh"
echo ""

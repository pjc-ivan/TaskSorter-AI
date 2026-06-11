#!/bin/bash

# CHANGE: Fixed Linux installer performance - complete rewrite
# Previous version had all commands on one line (broken formatting)
# and contained unnecessary waits and redundant installations.

echo ""
echo "Installing TaskSorter AI..."
echo ""

# ─────────────────────────────────────
# PYTHON DEPENDENCIES
# ─────────────────────────────────────
# CHANGE: Combined three dnf install commands into one

sudo dnf install -y python3 python3-pip python3-virtualenv

# ─────────────────────────────────────
# OLLAMA
# ─────────────────────────────────────

curl -fsSL https://ollama.com/install.sh | sh

systemctl --user enable ollama
systemctl --user start ollama

# CHANGE: Replace sleep 5 with a readiness check loop
echo "Waiting for Ollama server to start..."
for i in $(seq 1 30); do
    if ollama list >/dev/null 2>&1; then
        echo "Ollama server is ready."
        break
    fi
    echo "Waiting for Ollama... ($i/30)"
    sleep 1
done

# ─────────────────────────────────────
# VIRTUAL ENVIRONMENT
# ─────────────────────────────────────

python3 -m venv venv
source venv/bin/activate

# ─────────────────────────────────────
# PYTHON PACKAGES
# ─────────────────────────────────────
# CHANGE: Combined all pip installs into one, removed pip --upgrade

pip install customtkinter dateparser ollama spacy google-api-python-client google-auth-httplib2 google-auth-oauthlib

# ─────────────────────────────────────
# SPACY MODEL
# ─────────────────────────────────────

python -m spacy download de_core_news_sm

# ─────────────────────────────────────
# AI MODEL (runs in background while pip installs)
# ─────────────────────────────────────
# CHANGE: Pull model after dependencies to avoid timeout
# The model download is large and runs in the foreground
# so the user can monitor progress.

ollama pull gemma3:1b

# ─────────────────────────────────────
# RUN SCRIPT
# ─────────────────────────────────────

cat > run.sh << 'EOL'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python TaskSorter.py
EOL

chmod +x run.sh

# ─────────────────────────────────────
# APPLICATION MENU ENTRY
# ─────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cat > TaskSorterAI.desktop << EOL
[Desktop Entry]
Version=1.0
Type=Application
Name=TaskSorter AI
Comment=AI powered task management
Exec=${SCRIPT_DIR}/run.sh
Path=${SCRIPT_DIR}
Icon=${SCRIPT_DIR}/assets/icon.png
Terminal=false
Categories=Utility;
StartupNotify=true
EOL

chmod +x TaskSorterAI.desktop
mkdir -p ~/.local/share/applications
cp TaskSorterAI.desktop ~/.local/share/applications/
update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

# ─────────────────────────────────────
# FINISHED
# ─────────────────────────────────────

echo ""
echo "Installation complete!"
echo ""
echo "Run: ./run.sh"
echo ""

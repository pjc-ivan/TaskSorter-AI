#!/bin/bash

echo ""
echo "Installing TaskSorter AI..."
echo ""

# ─────────────────────────────────────
# SYSTEM DEPENDENCIES
# ─────────────────────────────────────

sudo dnf install -y \
    python3 \
    python3-pip \
    python3-virtualenv \
    python3-tkinter \
    curl

# ─────────────────────────────────────
# OLLAMA
# ─────────────────────────────────────

if ! command -v ollama >/dev/null 2>&1; then
    curl -fsSL https://ollama.com/install.sh | sh
fi

systemctl --user enable ollama >/dev/null 2>&1 || true
systemctl --user start ollama >/dev/null 2>&1 || true

echo "Waiting for Ollama server..."

for i in $(seq 1 30); do
    if ollama list >/dev/null 2>&1; then
        echo "Ollama ready."
        break
    fi
    sleep 1
done

# ─────────────────────────────────────
# PYTHON VENV
# ─────────────────────────────────────

if [ ! -d "venv" ]; then
    python3 -m venv venv
fi

source venv/bin/activate

# ─────────────────────────────────────
# PYTHON PACKAGES
# ─────────────────────────────────────

pip install -q \
    customtkinter \
    spacy \
    ollama \
    google-api-python-client \
    google-auth-httplib2 \
    google-auth-oauthlib

# ─────────────────────────────────────
# SPACY MODEL
# ─────────────────────────────────────

python -c "import spacy; spacy.load('de_core_news_sm')" >/dev/null 2>&1 || \
python -m spacy download de_core_news_sm

# ─────────────────────────────────────
# AI MODEL
# ─────────────────────────────────────

ollama list | grep -q "gemma3:1b" || ollama pull gemma3:1b

# ─────────────────────────────────────
# RUN SCRIPT
# ─────────────────────────────────────

cat > run.sh << 'EOF'
#!/bin/bash
cd "$(dirname "$0")"
source venv/bin/activate
python TaskSorter.py
EOF

chmod +x run.sh

# ─────────────────────────────────────
# DESKTOP ENTRY
# ─────────────────────────────────────

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

cat > TaskSorterAI.desktop << EOF
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
EOF

chmod +x TaskSorterAI.desktop

mkdir -p ~/.local/share/applications
cp TaskSorterAI.desktop ~/.local/share/applications/

update-desktop-database ~/.local/share/applications/ 2>/dev/null || true

echo ""
echo "Installation complete!"
echo ""
echo "Start with:"
echo "./run.sh"
echo ""
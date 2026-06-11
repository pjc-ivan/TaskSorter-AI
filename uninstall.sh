#!/bin/bash
# File: uninstall.sh
# Uninstall script for TaskSorter AI
# Removes all installed files, configurations, and menu entries


echo ""
echo "Uninstalling TaskSorter AI..."
echo ""


# ─────────────────────────────────────
# CONFIRMATION
# ─────────────────────────────────────
# Ask user for confirmation before proceeding

read -p "Are you sure you want to uninstall TaskSorter AI? (y/N): " confirm

if [[ ! "$confirm" =~ ^[Yy]$ ]]; then
    echo "Uninstallation cancelled."
    exit 0
fi


# ─────────────────────────────────────
# REMOVE DESKTOP ENTRY
# ─────────────────────────────────────
# Remove application from Linux application menu

echo "Removing desktop entry..."

rm -f ~/.local/share/applications/TaskSorterAI.desktop

update-desktop-database ~/.local/share/applications 2>/dev/null


# ─────────────────────────────────────
# REMOVE VIRTUAL ENVIRONMENT
# ─────────────────────────────────────
# Delete Python virtual environment folder

echo "Removing virtual environment..."

rm -rf venv


# ─────────────────────────────────────
# REMOVE RUN SCRIPT
# ─────────────────────────────────────
# Delete the run script

echo "Removing run script..."

rm -f run.sh


# ─────────────────────────────────────
# REMOVE CONFIGURATION FILES
# ─────────────────────────────────────
# Delete configuration and task data files

echo "Removing configuration files..."

rm -f config.json
rm -f tasks.json
rm -f token.pickle


# ─────────────────────────────────────
# REMOVE OLLAMA MODEL (OPTIONAL)
# ─────────────────────────────────────
# Optionally remove the AI model to free up space

read -p "Do you also want to remove the Ollama AI model? (y/N): " remove_model

if [[ "$remove_model" =~ ^[Yy]$ ]]; then
    echo "Removing Ollama model..."
    ollama rm gemma3:1b 2>/dev/null || echo "Model not found or already removed."
fi


# ─────────────────────────────────────
# FINISHED
# ─────────────────────────────────────
# Display completion message

echo ""
echo "Uninstallation complete."
echo ""
echo "Note: The following items were NOT removed:"
echo "- This uninstall script (uninstall.sh)"
echo "- The installer script (install_linux.sh)"
echo "- Source code files (you can delete manually if desired)"
echo "- credentials.json (Google API credentials, if exists)"
echo ""
echo "To reinstall, run ./install_linux.sh again."
echo ""

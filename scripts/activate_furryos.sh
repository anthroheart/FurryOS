#!/bin/bash
# Convenient wrapper to activate FurryOS venv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/furryos_venv/bin/activate"

echo "🐾 FurryOS venv activated!"
echo "Python: $(which python3)"
echo "Pip: $(which pip3)"
echo ""
echo "To deactivate: type 'deactivate'"

#!/bin/bash
# setup_venv.sh - Creates isolated Python environment for FurryOS build system
# Location: /TOP/setup_venv.sh
# This venv can be distributed WITH the ISO for offline builds

set -e

VENV_DIR="furryos_venv"
PYTHON_VERSION=$(python3 --version | cut -d' ' -f2 | cut -d'.' -f1,2)

echo "========================================"
echo "   🐾 FurryOS venv Setup 🐾"
echo "========================================"
echo ""

# Check if already exists
if [ -d "$VENV_DIR" ]; then
    echo "⚠️  venv already exists at $VENV_DIR"
    read -p "Remove and recreate? [y/N]: " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "🗑️  Removing old venv..."
        rm -rf "$VENV_DIR"
    else
        echo "✓ Using existing venv"
        exit 0
    fi
fi

# Create venv
echo "📦 Creating Python $PYTHON_VERSION virtual environment..."
python3 -m venv "$VENV_DIR"

# Activate venv
source "$VENV_DIR/bin/activate"

# Upgrade pip
echo "⬆️  Upgrading pip..."
pip install --upgrade pip setuptools wheel

# Install ALL FurryOS dependencies
echo "📥 Installing FurryOS dependencies..."
echo "   This may take 2-5 minutes..."

# Core dependencies
pip install pyyaml
pip install requests
pip install pillow
pip install mutagen
pip install cryptography
pip install jinja2

# Build tools
pip install pipreqs

# Optional but useful
pip install python-magic-bin 2>/dev/null || pip install python-magic 2>/dev/null || true

echo ""
echo "✅ All packages installed successfully!"

# Create activation wrapper
cat > activate_furryos.sh << 'WRAPPER'
#!/bin/bash
# Convenient wrapper to activate FurryOS venv

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/furryos_venv/bin/activate"

echo "🐾 FurryOS venv activated!"
echo "Python: $(which python3)"
echo "Pip: $(which pip3)"
echo ""
echo "To deactivate: type 'deactivate'"
WRAPPER

chmod +x activate_furryos.sh

# Create requirements.txt
pip freeze > "$VENV_DIR/requirements.txt"

# Also create a clean requirements.txt in /TOP
cat > requirements.txt << 'REQS'
# FurryOS Build System Requirements
# Install with: pip install -r requirements.txt

# Core Framework
pyyaml>=6.0
requests>=2.31.0

# Media Processing
pillow>=10.0.0
mutagen>=1.47.0

# Cryptography & Signing
cryptography>=41.0.0

# Template Engine
jinja2>=3.1.2

# Build Tools
pipreqs>=0.5.0

# Additional Requirements
sudo apt-get install genisoimage xorriso grub-pc-bin grub-efi-amd64-bin

# Optional Dependencies
python-magic-bin>=0.4.14; platform_system == "Windows"
python-magic>=0.4.27; platform_system != "Windows"
REQS

echo "✓ requirements.txt created in /TOP and venv/"

# Deactivate
deactivate

echo ""
echo "✅ FurryOS venv created successfully!"
echo ""
echo "📍 Location: $(pwd)/$VENV_DIR"
echo "📦 Packages installed:"
cat "$VENV_DIR/requirements.txt" | wc -l
echo ""
echo "🔐 cryptography package: INSTALLED"
echo "   (Ed25519 signing ready)"
echo ""
echo "🚀 Usage:"
echo "   Method 1 (recommended):"
echo "      source activate_furryos.sh"
echo ""
echo "   Method 2 (manual):"
echo "      source $VENV_DIR/bin/activate"
echo ""
echo "   Method 3 (scripts do it automatically):"
echo "      Just run: ./quick_start.sh"
echo "      (scripts detect and use venv if available)"
echo ""
echo "📦 To bundle with ISO:"
echo "   tar -czf furryos_venv.tar.gz furryos_venv/"
echo ""
echo "🐾 Go touch grass; venv setup complete! 🌱"

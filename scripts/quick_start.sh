#!/bin/bash
# FurryOS Quick Start - Golden State Edition
set -e

echo "==============================================================================="
echo "   🐾 FURRYOS GOLDEN STATE BUILDER 🐾"
echo "==============================================================================="
echo "   1. CLEANUP: Wiping old artifacts"
echo "   2. SETUP: Creating environment"
echo "   3. DOCS: Generating PDF Guide"
echo "   4. COMPILE: Building C/ASM core"
echo "   5. DEPLOY: Building ISO with Library & Docs"
echo "==============================================================================="

# --- STEP 1: CLEAN ---
if [ -d "furryos_venv" ]; then rm -rf furryos_venv; fi
if [ -d "output" ]; then rm -rf output; fi
if [ -d "furryos_build" ]; then rm -rf furryos_build; fi

# --- STEP 2: SETUP ---
echo ""
echo "🔍 [2/6] CHECKING DEPENDENCIES..."
sudo apt-get update -qq
sudo apt-get install -y python3 python3-pip python3-venv build-essential nasm gcc g++ genisoimage xorriso mtools grub-pc-bin grub-efi-amd64-bin parted dosfstools rsync

echo ""
echo "🐍 [3/6] SETTING UP VENV..."
chmod +x setup_venv.sh
./setup_venv.sh
source furryos_venv/bin/activate

# --- STEP 3: DOCS ---
echo ""
echo "📘 [3.5/6] COMPILING USER GUIDE..."
# Ensure PDF deps are installed in venv (xhtml2pdf)
pip install -q xhtml2pdf markdown
python3 compile_docs.py

# --- STEP 4: KEYS & COMPILE ---
echo ""
echo "🔐 [4/6] CHECKING KEYS..."
if [ ! -f "signing_keys/furryos_signing.key" ]; then
    python3 assets/generate_signing_keys.py
fi

echo ""
echo "🔨 [5/6] COMPILING MODULES..."
sudo furryos_venv/bin/python3 assets/launcher.py

# --- STEP 5: BUILD ---
echo ""
echo "💿 [6/6] BUILDING ISO..."
sudo furryos_venv/bin/python3 assets/deploy_iso.py

# --- DONE ---
echo ""
if ls output/furryos-*.iso 1> /dev/null 2>&1; then
    ISO_FILE=$(ls output/furryos-*.iso | head -n 1)
    echo "📀 ISO Created: $ISO_FILE"
    echo "   Next: sudo python3 assets/create_partitions.py"
else
    echo "❌ Error: ISO generation failed."
    exit 1
fi

#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
#              🦊 FurryOS Gen2.1 Development Folder Setup Script
#═══════════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║           🦊 FurryOS Gen2.1 Development Folder Setup 🦊                      ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""
echo "Project root: $PROJECT_ROOT"
echo ""

# Function to open folder in file manager
open_folder() {
    if command -v xdg-open &> /dev/null; then
        xdg-open "$1" &
    elif command -v nautilus &> /dev/null; then
        nautilus "$1" &
    elif command -v dolphin &> /dev/null; then
        dolphin "$1" &
    elif command -v thunar &> /dev/null; then
        thunar "$1" &
    else
        echo "⚠️  Could not detect file manager. Please manually open: $1"
    fi
}

echo "Opening asset folders for you to add files..."
echo ""

# Open all asset folders
echo "📁 Opening: wallpapers/ (ADD: default.jpg)"
open_folder "$PROJECT_ROOT/payload/assets/wallpapers"
sleep 1

echo "📁 Opening: splash/ (ADD: splash.png)"
open_folder "$PROJECT_ROOT/payload/assets/splash"
sleep 1

echo "📁 Opening: sounds/startup/ (ADD: startup.ogg)"
open_folder "$PROJECT_ROOT/payload/assets/sounds/startup"
sleep 1

echo "📁 Opening: sounds/shutdown/ (ADD: shutdown.ogg - optional)"
open_folder "$PROJECT_ROOT/payload/assets/sounds/shutdown"
sleep 1

echo "📁 Opening: images/ (ADD: any UI images - optional)"
open_folder "$PROJECT_ROOT/payload/assets/images"
sleep 1

echo "📁 Opening: icons/ (ADD: any custom icons - optional)"
open_folder "$PROJECT_ROOT/payload/assets/icons"
sleep 1

echo "📁 Opening: music/ (ADD: any theme music - optional)"
open_folder "$PROJECT_ROOT/payload/assets/music"
sleep 1

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ All asset folders are now open!"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📋 REQUIRED FILES (must add these):"
echo "   • wallpapers/default.jpg     (Desktop background, 1920x1080+ JPEG)"
echo "   • splash/splash.png          (Boot screen, 1024x768 or 1920x1080 PNG)"
echo "   • sounds/startup/startup.ogg (Login sound, 2-5 sec OGG Vorbis)"
echo ""
echo "📋 OPTIONAL FILES (add if you want):"
echo "   • sounds/shutdown/shutdown.ogg (Logout sound, 2-5 sec OGG)"
echo "   • images/* (Any UI images, backgrounds, etc.)"
echo "   • icons/* (Custom app icons, logo files)"
echo "   • music/* (Theme songs, background music)"
echo ""
echo "⚠️  IMPORTANT: All filenames must be LOWERCASE!"
echo "   ✅ default.jpg (correct)"
echo "   ❌ Default.jpg (WRONG - capital D)"
echo ""
echo "📖 Read the README.txt file in each folder for detailed specifications."
echo ""
echo "After adding your files, run: ./create_asset_zip.sh"
echo "═══════════════════════════════════════════════════════════════════════════════"

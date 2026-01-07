#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
#              🦊 FurryOS Gen2.1 Asset ZIP Creator Script
#═══════════════════════════════════════════════════════════════════════════════

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(dirname "$SCRIPT_DIR")"

echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
echo "║              🦊 FurryOS Gen2.1 Asset ZIP Creator 🦊                          ║"
echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
echo ""

# Verify required files exist
ERRORS=0

echo "🔍 Verifying required files..."
echo ""

if [ ! -f "$PROJECT_ROOT/payload/assets/wallpapers/default.jpg" ]; then
    echo "❌ MISSING: payload/assets/wallpapers/default.jpg"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ Found: wallpapers/default.jpg"
fi

if [ ! -f "$PROJECT_ROOT/payload/assets/splash/splash.png" ]; then
    echo "❌ MISSING: payload/assets/splash/splash.png"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ Found: splash/splash.png"
fi

if [ ! -f "$PROJECT_ROOT/payload/assets/sounds/startup/startup.ogg" ]; then
    echo "❌ MISSING: payload/assets/sounds/startup/startup.ogg"
    ERRORS=$((ERRORS + 1))
else
    echo "✅ Found: sounds/startup/startup.ogg"
fi

# Check optional files
if [ -f "$PROJECT_ROOT/payload/assets/sounds/shutdown/shutdown.ogg" ]; then
    echo "✅ Found: sounds/shutdown/shutdown.ogg (optional)"
fi

# Count optional assets
IMAGE_COUNT=$(find "$PROJECT_ROOT/payload/assets/images" -type f ! -name "README.txt" 2>/dev/null | wc -l)
ICON_COUNT=$(find "$PROJECT_ROOT/payload/assets/icons" -type f ! -name "README.txt" 2>/dev/null | wc -l)
MUSIC_COUNT=$(find "$PROJECT_ROOT/payload/assets/music" -type f ! -name "README.txt" 2>/dev/null | wc -l)

echo ""
echo "📊 Optional assets:"
echo "   • Images: $IMAGE_COUNT file(s)"
echo "   • Icons: $ICON_COUNT file(s)"
echo "   • Music: $MUSIC_COUNT file(s)"
echo ""

if [ $ERRORS -gt 0 ]; then
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo "❌ ERROR: Missing $ERRORS required file(s)!"
    echo "═══════════════════════════════════════════════════════════════════════════════"
    echo ""
    echo "Please add the missing files and run this script again."
    echo "Read the README.txt files in each folder for specifications."
    exit 1
fi

echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ All required files found!"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""

# Create the ZIP
echo "📦 Creating FurryOS_Gen2.1_Payload_Assets.zip..."
echo ""

cd "$PROJECT_ROOT"

# Create temporary folder with proper structure
TEMP_DIR="FurryOS_Gen2.1_Payload_Assets"
rm -rf "$TEMP_DIR"
mkdir -p "$TEMP_DIR"

# Copy assets
cp -r payload/assets/wallpapers "$TEMP_DIR/"
cp -r payload/assets/splash "$TEMP_DIR/"
cp -r payload/assets/sounds "$TEMP_DIR/"
cp -r payload/assets/images "$TEMP_DIR/"
cp -r payload/assets/icons "$TEMP_DIR/"
cp -r payload/assets/music "$TEMP_DIR/"

# Remove README files from ZIP
find "$TEMP_DIR" -name "README.txt" -delete

# Create ZIP
zip -r FurryOS_Gen2.1_Payload_Assets.zip "$TEMP_DIR"

# Cleanup
rm -rf "$TEMP_DIR"

echo ""
echo "═══════════════════════════════════════════════════════════════════════════════"
echo "✅ SUCCESS! Asset ZIP created!"
echo "═══════════════════════════════════════════════════════════════════════════════"
echo ""
echo "📦 ZIP file: FurryOS_Gen2.1_Payload_Assets.zip"
echo "📁 Location: $PROJECT_ROOT/FurryOS_Gen2.1_Payload_Assets.zip"
echo ""
echo "📤 Next steps:"
echo "   1. Upload FurryOS_Gen2.1_Payload_Assets.zip to:"
echo "      https://furry-os.org/assets/FurryOS_Gen2.1_Payload_Assets.zip"
echo ""
echo "   2. Upload install_furryos_assets.sh to:"
echo "      https://furry-os.org/install_furryos_assets.sh"
echo ""
echo "   3. Users download and run:"
echo "      wget https://furry-os.org/install_furryos_assets.sh"
echo "      chmod +x install_furryos_assets.sh"
echo "      ./install_furryos_assets.sh"
echo ""
echo "🦊 Your custom FurryOS assets are ready for distribution!"
echo "═══════════════════════════════════════════════════════════════════════════════"

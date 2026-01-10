#!/bin/bash
# ══════════════════════════════════════════════════════════════════════════════
# 🐾 FurryOS Asset Restorer
# ══════════════════════════════════════════════════════════════════════════════
# Function: Refreshes the ~/FurryOS mansion from the system's immutable root.
# Use this if you accidentally deleted your wallpapers, sounds, or docs.
# ══════════════════════════════════════════════════════════════════════════════

# 1. Define the Source of Truth
SYSTEM_ROOT="/usr/share/furryos"
USER_MANSION="$HOME/FurryOS"

echo "🦊 FurryOS Asset Manager"
echo "════════════════════════════"
echo "This will refresh the assets in your home folder ($USER_MANSION)"
echo "from the system's secure storage."
echo ""
echo "Any custom files you added will be kept."
echo "Any missing system files will be restored."
echo ""
read -p "Press [Enter] to begin..."

# 2. Verify System Root
if [ ! -d "$SYSTEM_ROOT" ]; then
    echo "❌ Critical Error: System assets not found in $SYSTEM_ROOT"
    echo "   Are you running this on a genuine FurryOS install?"
    read -p "Press Enter to exit..."
    exit 1
fi

# 3. Perform the Sync
echo "📦 Restoring Assets..."
mkdir -p "$USER_MANSION"

# rsync flags: -a (archive), -v (verbose), -u (update/only newer), --ignore-existing (don't overwrite user edits)
rsync -avu --ignore-existing "$SYSTEM_ROOT/" "$USER_MANSION/"

# 4. Re-apply Configurations (Just in case)
echo "🎨 Refreshing Wallpaper & Sound configurations..."
export GSETTINGS_BACKEND=dconf

if [ -f "$USER_MANSION/wallpapers/default.jpg" ]; then
    gsettings set org.mate.desktop.background picture-filename "$USER_MANSION/wallpapers/default.jpg"
fi

echo ""
echo "✅ Restoration Complete!"
echo "   Your Mansion is fully stocked."
echo ""
read -p "Press Enter to close..."

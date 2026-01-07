#!/bin/bash
# FurryOS Gen2.1 Live Multimedia Setup - Auto-executes on first boot
# This script runs automatically when booting into Live mode

set -e

LIVE_USER="$(whoami)"
HOME_DIR="$HOME"
ASSET_SRC="/usr/share/furryos"

echo "==================================="
echo "  FurryOS Gen2.1 Live Setup"
echo "==================================="
echo "Live user: $LIVE_USER"
echo "Home directory: $HOME_DIR"

# Create ~/FurryOS folder in user's home (appears in file manager sidebar)
FURRYOS_HOME="$HOME_DIR/FurryOS"
echo "Creating FurryOS home folder..."
mkdir -p "$FURRYOS_HOME"

# Create XDG user-dirs entry so it appears in sidebar like Documents, Pictures, etc.
XDG_DIRS_FILE="$HOME_DIR/.config/user-dirs.dirs"
mkdir -p "$HOME_DIR/.config"

# Add FurryOS to user directories
if ! grep -q "XDG_FURRYOS_DIR" "$XDG_DIRS_FILE" 2>/dev/null; then
    echo "XDG_FURRYOS_DIR="\$HOME/FurryOS"" >> "$XDG_DIRS_FILE"
fi

# Copy all assets from /usr/share/furryos to ~/FurryOS
if [ -d "$ASSET_SRC" ]; then
    echo "Copying FurryOS assets..."
    cp -r "$ASSET_SRC"/* "$FURRYOS_HOME"/ 2>/dev/null || true
    chmod -R u+rw "$FURRYOS_HOME"
    echo "✓ Assets copied to ~/FurryOS"
else
    echo "⚠ Warning: Asset directory $ASSET_SRC not found"
fi

# Set wallpaper for MATE desktop
WALLPAPER="$ASSET_SRC/wallpapers/default.jpg"
if [ -f "$WALLPAPER" ]; then
    echo "Setting wallpaper..."
    # Use gsettings for MATE
    gsettings set org.mate.background picture-filename "$WALLPAPER" 2>/dev/null || true
    # Also set via dconf as backup
    dconf write /org/mate/desktop/background/picture-filename "'$WALLPAPER'" 2>/dev/null || true
    echo "✓ Wallpaper set"
else
    echo "⚠ Wallpaper not found: $WALLPAPER"
fi

# Play startup sound
STARTUP_SOUND="$ASSET_SRC/sounds/startup.ogg"
if [ -f "$STARTUP_SOUND" ]; then
    echo "Playing startup sound..."
    # Try multiple audio players
    if command -v paplay &>/dev/null; then
        paplay "$STARTUP_SOUND" &
    elif command -v aplay &>/dev/null; then
        aplay "$STARTUP_SOUND" &
    elif command -v mpg123 &>/dev/null; then
        mpg123 "$STARTUP_SOUND" &
    fi
    echo "✓ Startup sound played"
else
    echo "⚠ Startup sound not found: $STARTUP_SOUND"
fi

# Create desktop shortcuts for key FurryOS content
DESKTOP_DIR="$HOME_DIR/Desktop"
mkdir -p "$DESKTOP_DIR"

# Create shortcut to FurryOS folder
cat > "$DESKTOP_DIR/FurryOS.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Link
Name=FurryOS Content
Icon=folder
URL=$HOME/FurryOS
EOF
chmod +x "$DESKTOP_DIR/FurryOS.desktop"

# Copy any .desktop files from payload
if [ -d "$ASSET_SRC/desktop" ]; then
    echo "Installing desktop files..."
    cp "$ASSET_SRC"/desktop/*.desktop "$DESKTOP_DIR"/ 2>/dev/null || true
    chmod +x "$DESKTOP_DIR"/*.desktop 2>/dev/null || true
    echo "✓ Desktop files installed"
fi

echo "==================================="
echo "  ✓ FurryOS Live Setup Complete"
echo "==================================="
echo ""
echo "Your FurryOS content is in: ~/FurryOS"
echo ""

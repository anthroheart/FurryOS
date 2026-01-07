#!/usr/bin/env bash
set -e

# Track build time and suppress xattr warnings
BUILD_START_TIME=$(date +%s)
exec 2> >(grep -v "Unrecognised xattr" >&2)

# ═══════════════════════════════════════════════════════════════════
# FurryOS Gen2.1 Enhanced Build Script
# Features: Mode-based bundle installation, Plymouth splash, themes
# ═══════════════════════════════════════════════════════════════════

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_ROOT/furryos_venv"
GENERATED="$PROJECT_ROOT/_generated"
ISO_DIR="$GENERATED/iso"
WORK_DIR="$GENERATED/work"
ISO_ROOT="$GENERATED/iso-root"
SQUASHFS_ROOT="$WORK_DIR/squashfs-root"
OUTPUT_DIR="$GENERATED/output"

echo "══════════════════════════════════════════════════════════════"
echo "          FurryOS Gen2.1 Enhanced Build System"
echo "══════════════════════════════════════════════════════════════"
echo "Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# ═══════════════════════════════════════════════════════════════════
# Python Environment Setup
# ═══════════════════════════════════════════════════════════════════

if ! command -v python3 &>/dev/null; then
    echo "ERROR: python3 not found"
    exit 1
fi

if [ ! -d "$VENV_DIR" ]; then
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
pip install --quiet --upgrade pip pyyaml rich requests

# ═══════════════════════════════════════════════════════════════════
# Phase 1-3: Validation
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 1] Validating GENOME.yaml"
if [ -f "GENOME_Gen2.1_Enhanced.yaml" ]; then
    ln -sf GENOME_Gen2.1_Enhanced.yaml GENOME.yaml
    echo "  ✓ Using enhanced GENOME.yaml"
fi

echo ""
echo "[Phase 2] Checking assets"
python3 << 'ASSETCHECK'
from pathlib import Path
import yaml

root = Path.cwd()
genome_file = root / "GENOME.yaml"

if genome_file.exists():
    genome = yaml.safe_load(genome_file.open())
    assets = genome.get("assets", {})
    asset_root = root / assets.get("root", "payload/assets")

    required = assets.get("required", {})
    for name, path in required.items():
        full_path = asset_root / path
        if full_path.exists():
            print(f"  ✓ {name}: {path}")
        else:
            print(f"  ⚠ MISSING {name}: {path}")
else:
    print("  ⚠ GENOME.yaml not found")
ASSETCHECK

# ═══════════════════════════════════════════════════════════════════
# Phase 3-5: ISO Download and Extraction
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 3] Ensuring Debian base ISO"

echo
echo "ℹ️ This step may appear idle for several minutes."
echo "   The Debian Live ISO is being downloaded and verified."
echo "   Please be patient — the build is still running."
echo "   (Once downloaded, future builds will skip this step.)"
echo

mkdir -p "$ISO_DIR"
ISO_FILE="$ISO_DIR/debian-live-mate-amd64.iso"
ISO_URL="https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-13.2.0-amd64-mate.iso"

if [ -f "$ISO_FILE" ]; then
    SIZE=$(stat -c%s "$ISO_FILE" 2>/dev/null || stat -f%z "$ISO_FILE" 2>/dev/null)
    if [ "$SIZE" -lt 100000000 ]; then
        echo "  Existing ISO invalid, re-downloading..."
        rm -f "$ISO_FILE"
    else
        echo "  ✓ ISO present and valid"
    fi
fi

if [ ! -f "$ISO_FILE" ]; then
    echo "  Downloading Debian Live MATE ISO (this may take time)..."
    curl -L "$ISO_URL" -o "$ISO_FILE"
fi

echo ""
echo "[Phase 4] Extracting ISO workspace"
if [ -f "prepare_iso_workspace.sh" ]; then
    bash prepare_iso_workspace.sh
else
    # Inline extraction if prepare script doesn't exist
    echo "  Extracting ISO manually..."
    mkdir -p "$ISO_ROOT" "$WORK_DIR"

    sudo mount -o loop "$ISO_FILE" /mnt 2>/dev/null || true
    rsync -a /mnt/ "$ISO_ROOT"/ 2>/dev/null || cp -r /mnt/* "$ISO_ROOT"/
    sudo umount /mnt 2>/dev/null || true

    if [ -f "$ISO_ROOT/live/filesystem.squashfs" ]; then
        sudo unsquashfs -d "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs"
    fi
fi

if [ ! -d "$SQUASHFS_ROOT" ]; then
    echo "ERROR: Extraction failed - $SQUASHFS_ROOT not found"
    exit 1
fi

echo "  ✓ ISO extracted successfully"

# ═══════════════════════════════════════════════════════════════════
# Phase 5: Asset Installation
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 5] Installing FurryOS Assets"
PAYLOAD_DIR="$PROJECT_ROOT/payload"
FURRYOS_SHARE="$SQUASHFS_ROOT/usr/share/furryos"

mkdir -p "$FURRYOS_SHARE"

# Copy ALL assets to central location
if [ -d "$PAYLOAD_DIR/assets" ]; then
    echo "  Copying assets to /usr/share/furryos..."
    cp -rv "$PAYLOAD_DIR/assets"/* "$FURRYOS_SHARE"/ 2>/dev/null || true

    # Link to standard system locations
    if [ -d "$FURRYOS_SHARE/wallpapers" ]; then
        mkdir -p "$SQUASHFS_ROOT/usr/share/backgrounds/furryos"
        cp "$FURRYOS_SHARE/wallpapers"/* "$SQUASHFS_ROOT/usr/share/backgrounds/furryos/" 2>/dev/null || true
        echo "    ✓ Wallpapers installed"
    fi

    if [ -d "$FURRYOS_SHARE/sounds" ]; then
        mkdir -p "$SQUASHFS_ROOT/usr/share/sounds/furryos"
        cp "$FURRYOS_SHARE/sounds"/* "$SQUASHFS_ROOT/usr/share/sounds/furryos/" 2>/dev/null || true
        echo "    ✓ Sounds installed"
    fi

    if [ -d "$FURRYOS_SHARE/desktop" ]; then
        echo "    ✓ Desktop files ready"
    fi
else
    echo "  ⚠ No assets found in $PAYLOAD_DIR/assets"
fi

# ═══════════════════════════════════════════════════════════════════
# Phase 6: Plymouth Splash Screen
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 6] Configuring Plymouth Boot Splash"

# Install Plymouth
echo "  Installing Plymouth packages..."
chroot "$SQUASHFS_ROOT" /bin/bash -c "
    export DEBIAN_FRONTEND=noninteractive
    apt-get update -qq
    apt-get install -y -qq plymouth plymouth-themes >/dev/null 2>&1
" || echo "  ⚠ Plymouth install failed (continuing...)"

# Create FurryOS Plymouth theme
PLYMOUTH_THEME="$SQUASHFS_ROOT/usr/share/plymouth/themes/furryos"
mkdir -p "$PLYMOUTH_THEME"

if [ -d "$FURRYOS_SHARE/splash" ]; then
    cp "$FURRYOS_SHARE/splash"/* "$PLYMOUTH_THEME"/ 2>/dev/null || true
    echo "    ✓ Splash assets copied"
fi

# Create theme definition
cat > "$PLYMOUTH_THEME/furryos.plymouth" << 'PLYMOUTHDEF'
[Plymouth Theme]
Name=FurryOS
Description=FurryOS Gen2.1 Boot Splash
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/furryos
ScriptFile=/usr/share/plymouth/themes/furryos/furryos.script
PLYMOUTHDEF

# Create Plymouth script
cat > "$PLYMOUTH_THEME/furryos.script" << 'PLYMOUTHSCRIPT'
Window.SetBackgroundTopColor(0, 0, 0);
Window.SetBackgroundBottomColor(0, 0, 0);

if (Plymouth.GetMode() == "boot") {
    logo.image = Image("splash.png");
    logo.sprite = Sprite(logo.image);
    logo.opacity = 1;

    logo.x = Window.GetWidth() / 2 - logo.image.GetWidth() / 2;
    logo.y = Window.GetHeight() / 2 - logo.image.GetHeight() / 2;
    logo.sprite.SetPosition(logo.x, logo.y, 0);
}

fun refresh_callback() {
    # Animation hook
}

Plymouth.SetRefreshFunction(refresh_callback);
PLYMOUTHSCRIPT

# Set as default theme
chroot "$SQUASHFS_ROOT" /bin/bash -c "
    plymouth-set-default-theme furryos 2>/dev/null
    update-initramfs -u 2>/dev/null
" || echo "  ⚠ Plymouth theme activation failed"

echo "  ✓ Plymouth configured"

# ═══════════════════════════════════════════════════════════════════
# Phase 7: Mode Switching System
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 7] Installing Mode Switching System"

# Create mode switcher script
cat > "$SQUASHFS_ROOT/usr/local/bin/furryos-mode-switch" << 'MODESWITCHER'
#!/bin/bash
# FurryOS Mode Switcher - Gen2.1

MODE="${1:-normal}"

case "$MODE" in
    granny)
        gsettings set org.mate.interface gtk-theme "HighContrast"
        gsettings set org.mate.interface icon-theme "HighContrast"
        gsettings set org.mate.interface font-name "Sans 14"
        gsettings set org.mate.Marco.general reduced-resources true
        ;;

    gamer)
        gsettings set org.mate.interface gtk-theme "BlackMATE"
        gsettings set org.mate.Marco.general compositing-manager false
        gsettings set org.mate.session idle-delay 0
        ;;

    hacker)
        gsettings set org.mate.interface gtk-theme "BlackMATE"
        gsettings set org.mate.terminal.profile:/org/mate/terminal/profiles/default/ use-theme-colors false
        gsettings set org.mate.terminal.profile:/org/mate/terminal/profiles/default/ background-color "#000000"
        gsettings set org.mate.terminal.profile:/org/mate/terminal/profiles/default/ foreground-color "#00FF00"
        ;;

    ghost)
        gsettings set org.mate.interface gtk-theme "Menta-Dark"
        gsettings set org.mate.interface icon-theme "Papirus-Dark"
        # Enable privacy features
        ;;

    normal|*)
        gsettings reset org.mate.interface gtk-theme
        gsettings reset org.mate.interface icon-theme
        ;;
esac

notify-send "FurryOS" "Switched to ${MODE^} Mode" -i preferences-desktop-theme 2>/dev/null || true
echo "✓ Mode: ${MODE^}"
MODESWITCHER

chmod +x "$SQUASHFS_ROOT/usr/local/bin/furryos-mode-switch"

# Create mode launcher desktop files
mkdir -p "$SQUASHFS_ROOT/usr/share/applications"

for mode in granny normal gamer hacker ghost; do
    cat > "$SQUASHFS_ROOT/usr/share/applications/furryos-mode-${mode}.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FurryOS ${mode^} Mode
Comment=Switch to ${mode^} mode
Exec=/usr/local/bin/furryos-mode-switch ${mode}
Icon=preferences-desktop-theme
Terminal=false
Categories=Settings;DesktopSettings;
EOF
done

echo "  ✓ Mode switching installed (5 modes)"

# ═══════════════════════════════════════════════════════════════════
# Phase 8: Live Boot Autostart
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 8] Configuring Live Boot Experience"

# Install live setup script
SETUP_SCRIPT="FurryOS_Live_Multimedia_Setup_Post_ISO_Gen2.1.sh"
if [ -f "$PROJECT_ROOT/$SETUP_SCRIPT" ]; then
    cp "$PROJECT_ROOT/$SETUP_SCRIPT" "$SQUASHFS_ROOT/usr/local/bin/furryos-live-setup"
    chmod +x "$SQUASHFS_ROOT/usr/local/bin/furryos-live-setup"
    echo "  ✓ Live setup script installed"
fi

# Autostart entry
mkdir -p "$SQUASHFS_ROOT/etc/skel/.config/autostart"
cat > "$SQUASHFS_ROOT/etc/skel/.config/autostart/furryos-live-setup.desktop" << 'AUTOSTART'
[Desktop Entry]
Type=Application
Name=FurryOS Live Setup
Exec=/usr/local/bin/furryos-live-setup
Terminal=false
Hidden=false
X-MATE-Autostart-enabled=true
AUTOSTART

# Copy desktop files to skeleton
if [ -d "$FURRYOS_SHARE/desktop" ]; then
    mkdir -p "$SQUASHFS_ROOT/etc/skel/Desktop"
    cp "$FURRYOS_SHARE"/desktop/*.desktop "$SQUASHFS_ROOT/etc/skel/Desktop/" 2>/dev/null || true
    chmod +x "$SQUASHFS_ROOT/etc/skel/Desktop"/*.desktop 2>/dev/null || true
    echo "  ✓ Desktop files configured"
fi

# MATE desktop defaults
mkdir -p "$SQUASHFS_ROOT/etc/dconf/db/local.d"
cat > "$SQUASHFS_ROOT/etc/dconf/db/local.d/01-furryos" << 'DCONF'
[org/mate/desktop/background]
picture-filename='/usr/share/backgrounds/furryos/default.jpg'
picture-options='zoom'

[org/mate/sound]
event-sounds=true

[org/mate/session]
idle-delay=0
DCONF

chroot "$SQUASHFS_ROOT" dconf update 2>/dev/null || true

echo "  ✓ Live boot configured"

# ═══════════════════════════════════════════════════════════════════════════
# Install FurryOS Documentation
# ═══════════════════════════════════════════════════════════════════════════

echo "📚 Installing FurryOS documentation..."

if [ -d "payload/docs" ]; then
    # Install docs system-wide
    mkdir -p chroot/usr/share/doc/furryos
    cp -r payload/docs/* chroot/usr/share/doc/furryos/
    echo "✅ Installed documentation to /usr/share/doc/furryos/"

    # Copy README to Desktop (visible on first boot)
    if [ -f "payload/docs/README.pdf" ]; then
        mkdir -p chroot/etc/skel/Desktop
        cp payload/docs/README.pdf chroot/etc/skel/Desktop/FurryOS_README.pdf
        chmod 644 chroot/etc/skel/Desktop/FurryOS_README.pdf
        echo "✅ Placed README.pdf on desktop"
    fi

    # Create documentation menu entry
    mkdir -p chroot/usr/share/applications
    cat > chroot/usr/share/applications/furryos-documentation.desktop << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=FurryOS Documentation
Comment=Read the complete FurryOS guide and documentation
Icon=accessories-text-editor
Exec=xdg-open /usr/share/doc/furryos/
Terminal=false
Categories=Documentation;Education;
Keywords=furryos;documentation;help;guide;readme;manual;
StartupNotify=true
EOF

    chmod 644 chroot/usr/share/applications/furryos-documentation.desktop
    echo "✅ Created documentation menu entry"
else
    echo "⚠️  No documentation found in payload/docs/"
fi

# ═══════════════════════════════════════════════════════════════════
# Phase 9-11: Repack & Finalize
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "[Phase 9] Repacking SquashFS"
rm -f "$ISO_ROOT/live/filesystem.squashfs"
echo "  Creating filesystem.squashfs (this takes time)..."
sudo mksquashfs "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs" \
    -comp xz -b 1M -Xbcj x86 -e boot -noappend >/dev/null
echo "  ✓ SquashFS repacked"

echo ""
echo "[Phase 10] Building Bootable ISO"
mkdir -p "$OUTPUT_DIR"
OUTPUT_ISO="$OUTPUT_DIR/furryos-gen2.1-amd64.iso"
rm -f "$OUTPUT_ISO"

sudo xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "FurryOS Gen2.1" \
    -eltorito-boot isolinux/isolinux.bin \
    -eltorito-catalog isolinux/boot.cat \
    -no-emul-boot \
    -boot-load-size 4 \
    -boot-info-table \
    -isohybrid-mbr /usr/lib/ISOLINUX/isohdpfx.bin \
    -eltorito-alt-boot \
    -e boot/grub/efi.img \
    -no-emul-boot \
    -isohybrid-gpt-basdat \
    -output "$OUTPUT_ISO" \
    "$ISO_ROOT" 2>/dev/null

echo "  ✓ ISO created"

echo ""
echo "[Phase 11] Generating Checksums"
cd "$OUTPUT_DIR"
sha256sum "$(basename "$OUTPUT_ISO")" > "$(basename "$OUTPUT_ISO").sha256"

echo ""
echo "[Phase 12] Fixing Permissions"
sudo chown -R "$USER":"$USER" "$GENERATED"

# ═══════════════════════════════════════════════════════════════════
# Build Complete
# ═══════════════════════════════════════════════════════════════════

echo ""
echo "══════════════════════════════════════════════════════════════"
echo "             ✅ FurryOS Gen2.1 Build Complete!"
echo "══════════════════════════════════════════════════════════════"
echo ""
echo "Output: $OUTPUT_ISO"
SIZE=$(stat -c%s "$OUTPUT_ISO" 2>/dev/null || stat -f%z "$OUTPUT_ISO" 2>/dev/null)
echo "Size:   $(numfmt --to=iec-i --suffix=B $SIZE 2>/dev/null || echo "$SIZE bytes")"
echo "SHA256: $(cat "$(basename "$OUTPUT_ISO").sha256" | cut -d" " -f1)"
echo ""
echo "Features Included:"
echo "  ✓ Plymouth boot splash with custom theme"
echo "  ✓ 5 mode profiles (Granny/Normal/Gamer/Hacker/Ghost)"
echo "  ✓ Mode-based software bundle system"
echo "  ✓ Automatic live boot setup"
echo "  ✓ ~/FurryOS folder creation"
echo "  ✓ Wallpaper and startup sound"
echo "  ✓ Desktop file deployment"
echo ""
echo "Test Command:"
echo "  qemu-system-x86_64 -cdrom $OUTPUT_ISO -m 2G -enable-kvm"
echo ""
echo "══════════════════════════════════════════════════════════════"

# Display total build time
BUILD_END_TIME=$(date +%s)
BUILD_DURATION=$((BUILD_END_TIME - BUILD_START_TIME))
BUILD_MINUTES=$((BUILD_DURATION / 60))
BUILD_SECONDS=$((BUILD_DURATION % 60))

echo ""
echo "═══════════════════════════════════════════════════════════════════"
echo "⏱️  Total build time: ${BUILD_MINUTES}m ${BUILD_SECONDS}s"
echo "═══════════════════════════════════════════════════════════════════"

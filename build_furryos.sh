#!/usr/bin/env bash

set -e

# ============================================================
# FurryOS Complete Build Script (with Desktop Scripts)
# ============================================================

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
VENV_DIR="$PROJECT_ROOT/furryos_venv"
GENERATED="$PROJECT_ROOT/_generated"
ISO_DIR="$GENERATED/iso"
WORK_DIR="$GENERATED/work"
ISO_ROOT="$GENERATED/iso-root"
SQUASHFS_ROOT="$WORK_DIR/squashfs-root"
OUTPUT_DIR="$GENERATED/output"

echo "== FurryOS Complete Build Script =="
echo "Project root: $PROJECT_ROOT"
cd "$PROJECT_ROOT"

# ------------------------------------------------------------
# Python availability
# ------------------------------------------------------------
if ! command -v python3 &>/dev/null; then
    echo "ERROR: python not found in PATH"
    exit 1
fi

# ------------------------------------------------------------
# Virtual environment
# ------------------------------------------------------------
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating furryos_venv..."
    python3 -m venv "$VENV_DIR"
fi

source "$VENV_DIR/bin/activate"
echo "Python: $(python --version)"
pip install --quiet --upgrade pip
pip install --quiet pyyaml rich requests

# ------------------------------------------------------------
# Phase 1: Validate GENOME
# ------------------------------------------------------------
echo
echo "[Phase 1] Validating GENOME.yaml"
if [ -f "validate_genome.py" ]; then
    python validate_genome.py
else
    echo "  (validate_genome.py not found, skipping)"
fi

# ------------------------------------------------------------
# Phase 2: Generate build plan
# ------------------------------------------------------------
echo
echo "[Phase 2] Generating build plan"
if [ -f "generate_build_plan.py" ]; then
    python generate_build_plan.py
else
    echo "  (generate_build_plan.py not found, skipping)"
fi

# ------------------------------------------------------------
# Phase 3: Verify assets exist
# ------------------------------------------------------------
echo
echo "[Phase 3] Verifying asset paths"
python - << 'EOF'
from pathlib import Path
import yaml, sys

root = Path.cwd()
if not (root / "GENOME.yaml").exists():
    print("WARNING: GENOME.yaml not found, skipping asset verification")
    sys.exit(0)

g = yaml.safe_load(open("GENOME.yaml"))
assets = g.get("assets", {})
base = root / assets.get("root", "payload/assets")

missing = False
for k,v in assets.items():
    if k == "root":
        continue
    p = base / v
    if not p.exists():
        print(f"WARNING: Missing asset {k}: {p}")
    else:
        print(f"OK: {k} -> {p}")
EOF

# ------------------------------------------------------------
# Phase 4: Download Debian ISO (if needed)
# ------------------------------------------------------------
echo
echo "[Phase 4] Ensuring Debian ISO"
mkdir -p "$ISO_DIR"
ISO_FILE="$ISO_DIR/debian-live-mate-amd64.iso"
ISO_URL="https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-13.2.0-amd64-mate.iso"

if [ -f "$ISO_FILE" ]; then
    SIZE=$(stat -c%s "$ISO_FILE" 2>/dev/null || stat -f%z "$ISO_FILE" 2>/dev/null)
    if [ "$SIZE" -lt 100000000 ]; then
        echo "WARNING: Existing ISO is too small ($SIZE bytes). Re-downloading."
        rm -f "$ISO_FILE"
    else
        echo "ISO already present and size looks valid."
    fi
fi

if [ ! -f "$ISO_FILE" ]; then
    echo "Downloading Debian Live MATE ISO..."
    curl -L "$ISO_URL" -o "$ISO_FILE"
fi

SIZE=$(stat -c%s "$ISO_FILE" 2>/dev/null || stat -f%z "$ISO_FILE" 2>/dev/null)
if [ "$SIZE" -lt 100000000 ]; then
    echo "ERROR: Downloaded ISO is invalid (only $SIZE bytes)"
    exit 1
fi

echo "Debian ISO verified: $ISO_FILE ($SIZE bytes)"

# ------------------------------------------------------------
# Phase 5: Extract ISO (run prepare_iso_workspace.sh)
# ------------------------------------------------------------
echo
echo "[Phase 5] Extracting ISO workspace"

if [ ! -f "prepare_iso_workspace.sh" ]; then
    echo "ERROR: prepare_iso_workspace.sh not found!"
    exit 1
fi

echo "Running prepare_iso_workspace.sh..."
bash prepare_iso_workspace.sh

# Verify extraction worked
if [ ! -d "$SQUASHFS_ROOT" ]; then
    echo "ERROR: Squashfs extraction failed. $SQUASHFS_ROOT not found."
    exit 1
fi

echo "✓ ISO extracted successfully"

# ============================================================
# Phase 6: Apply GENOME.yaml Assets (Wallpaper/Splash/Sounds)
# ============================================================
echo
echo "[Phase 6] Applying GENOME.yaml default assets"

PAYLOAD_DIR="$PROJECT_ROOT/payload"

# Copy wallpapers
if [ -d "$PAYLOAD_DIR/assets/wallpapers" ]; then
    echo "  Installing wallpapers..."
    mkdir -p "$SQUASHFS_ROOT/usr/share/backgrounds/furryos"
    cp -rv "$PAYLOAD_DIR/assets/wallpapers/"* "$SQUASHFS_ROOT/usr/share/backgrounds/furryos/" 2>/dev/null || echo "  ⚠ No wallpaper files found"
    echo "  ✓ Wallpapers installed"
fi

# Copy splash screens
if [ -d "$PAYLOAD_DIR/assets/splash" ]; then
    echo "  Installing splash screens..."
    mkdir -p "$SQUASHFS_ROOT/usr/share/plymouth/themes/furryos"
    cp -rv "$PAYLOAD_DIR/assets/splash/"* "$SQUASHFS_ROOT/usr/share/plymouth/themes/furryos/" 2>/dev/null || echo "  ⚠ No splash files found"
    echo "  ✓ Splash screens installed"
fi

# Copy sounds
if [ -d "$PAYLOAD_DIR/assets/sounds" ]; then
    echo "  Installing system sounds..."
    mkdir -p "$SQUASHFS_ROOT/usr/share/sounds/furryos"
    cp -rv "$PAYLOAD_DIR/assets/sounds/"* "$SQUASHFS_ROOT/usr/share/sounds/furryos/" 2>/dev/null || echo "  ⚠ No sound files found"
    echo "  ✓ Sounds installed"
fi

# Copy music
if [ -d "$PAYLOAD_DIR/assets/music" ]; then
    echo "  Installing music..."
    mkdir -p "$SQUASHFS_ROOT/usr/share/furryos/music"
    cp -rv "$PAYLOAD_DIR/assets/music/"* "$SQUASHFS_ROOT/usr/share/furryos/music/" 2>/dev/null || echo "  ⚠ No music files found"
    echo "  ✓ Music installed"
fi

# Copy docs
if [ -d "$PAYLOAD_DIR/assets/docs" ]; then
    echo "  Installing documentation..."
    mkdir -p "$SQUASHFS_ROOT/usr/share/furryos/docs"
    cp -rv "$PAYLOAD_DIR/assets/docs/"* "$SQUASHFS_ROOT/usr/share/furryos/docs/" 2>/dev/null || echo "  ⚠ No doc files found"
    echo "  ✓ Documentation installed"
fi

# Copy images
if [ -d "$PAYLOAD_DIR/assets/images" ]; then
    echo "  Installing images..."
    mkdir -p "$SQUASHFS_ROOT/usr/share/furryos/images"
    cp -rv "$PAYLOAD_DIR/assets/images/"* "$SQUASHFS_ROOT/usr/share/furryos/images/" 2>/dev/null || echo "  ⚠ No image files found"
    echo "  ✓ Images installed"
fi

# Set MATE defaults in dconf
echo "  Configuring MATE defaults..."
mkdir -p "$SQUASHFS_ROOT/etc/dconf/db/local.d"
cat > "$SQUASHFS_ROOT/etc/dconf/db/local.d/01-furryos-defaults" << 'EOF'
[org/mate/desktop/background]
picture-filename='/usr/share/backgrounds/furryos/default.jpg'

[org/mate/sound]
event-sounds=true
input-feedback-sounds=false
EOF

chroot "$SQUASHFS_ROOT" dconf update 2>/dev/null || echo "  ℹ dconf not available (will use defaults)"
echo "  ✓ MATE defaults configured"

echo "✓ Phase 6 complete: Assets applied"

echo
# ============================================================

# ------------------------------------------------------------
# Phase 7: CUSTOMIZE SQUASHFS (Install Desktop Scripts)
# ------------------------------------------------------------
echo
echo "[Phase 7] Customizing FurryOS (Installing Desktop Scripts)"

# Check if desktop scripts exist
if [ -d "payload/assets/desktop" ]; then
    echo "Installing FurryOS desktop scripts..."

    # Copy desktop scripts to chroot temp folder
    mkdir -p "$SQUASHFS_ROOT/tmp/desktop-scripts"

    if [ -f "payload/assets/desktop/install-desktop-scripts.sh" ]; then
        cp payload/assets/desktop/*.sh "$SQUASHFS_ROOT/tmp/desktop-scripts/" 2>/dev/null || true
        cp payload/assets/desktop/*.desktop "$SQUASHFS_ROOT/tmp/desktop-scripts/" 2>/dev/null || true

        # Copy icons if they exist
        if [ -d "payload/assets/desktop/icons" ]; then
            cp -r payload/assets/desktop/icons "$SQUASHFS_ROOT/tmp/desktop-scripts/"
            echo "  ✓ Icons copied"
        fi

        # Make install script executable
        chmod +x "$SQUASHFS_ROOT/tmp/desktop-scripts/install-desktop-scripts.sh"

        # Install from within chroot
        echo "  Installing scripts via chroot..."
        sudo chroot "$SQUASHFS_ROOT" /bin/bash -c "cd /tmp/desktop-scripts && ./install-desktop-scripts.sh /"

        # Clean up
        rm -rf "$SQUASHFS_ROOT/tmp/desktop-scripts"

        echo "  ✓ Desktop scripts installed"
    else
        echo "  WARNING: install-desktop-scripts.sh not found, skipping desktop scripts"
    fi
else
    echo "  No desktop scripts found in payload/assets/desktop/, skipping"
fi

# ------------------------------------------------------------
# Phase 8: Repack SquashFS
# ------------------------------------------------------------
echo
echo "[Phase 8] Repacking SquashFS"

# Remove old squashfs
if [ -f "$ISO_ROOT/live/filesystem.squashfs" ]; then
    rm -f "$ISO_ROOT/live/filesystem.squashfs"
fi

echo "Creating new filesystem.squashfs (this may take a few minutes)..."
sudo mksquashfs "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs" \
    -comp xz \
    -b 1M \
    -Xbcj x86 \
    -e boot

echo "✓ SquashFS repacked"

# ------------------------------------------------------------
# Phase 9: Rebuild ISO
# ------------------------------------------------------------
echo
echo "[Phase 9] Building final FurryOS ISO"

mkdir -p "$OUTPUT_DIR"
OUTPUT_ISO="$OUTPUT_DIR/furryos-gen2-amd64.iso"

# Remove old ISO if exists
rm -f "$OUTPUT_ISO"

echo "Creating bootable ISO..."
sudo xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "FurryOS Gen2" \
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
    "$ISO_ROOT"

echo "✓ ISO created: $OUTPUT_ISO"

# ------------------------------------------------------------
# Phase 10: Generate SHA256
# ------------------------------------------------------------
echo
echo "[Phase 10] Generating SHA256 checksum"

cd "$OUTPUT_DIR"
sha256sum "$(basename "$OUTPUT_ISO")" > "$(basename "$OUTPUT_ISO").sha256"

echo "✓ SHA256: $(cat "$(basename "$OUTPUT_ISO").sha256")"

# ------------------------------------------------------------
# Phase 10: Fix permissions
# ------------------------------------------------------------
echo
echo "[Phase 10] Fixing permissions"
sudo chown -R "$USER":"$USER" "$GENERATED"
echo "✓ Permissions normalized"

# ------------------------------------------------------------
# Summary
# ------------------------------------------------------------
echo
echo "=========================================="
echo "✅ FurryOS Gen2 BUILD COMPLETE"
echo "=========================================="
echo
echo "Output:"
echo "  ISO: $OUTPUT_ISO"
SIZE=$(stat -c%s "$OUTPUT_ISO" 2>/dev/null || stat -f%z "$OUTPUT_ISO" 2>/dev/null)
echo "  Size: $(numfmt --to=iec-i --suffix=B $SIZE 2>/dev/null || echo "$SIZE bytes")"
echo "  SHA256: $OUTPUT_ISO.sha256"
echo
echo "Next steps:"
echo "  1. Test ISO in VirtualBox/QEMU"
echo "  2. Write to USB: sudo dd if=$OUTPUT_ISO of=/dev/sdX bs=4M status=progress"
echo "  3. Verify desktop scripts appear in Settings menu"
echo "=========================================="

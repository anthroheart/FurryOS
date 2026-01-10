#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  🐾 FurryOS Gen2.1_v2: The Sovereign Mansion Launcher
# ══════════════════════════════════════════════════════════════════════════════
#  Function: Instantly boots the unpacked OS folder into a High-Performance VM.
#  Tech: KVM Acceleration, LZ4 Rapid Sync, Hybrid-MBR Boot.
#  Lore: The Portal to the 2,000-Year Rest.
# ══════════════════════════════════════════════════════════════════════════════

set -e

# ------------------------------------------------------------------------------
# [Phase 0] Path Configuration
# ------------------------------------------------------------------------------
PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "$PROJECT_ROOT/.." && pwd)"

# Define the "Anatomy" of the Mansion
GENERATED="$PARENT_DIR/_generated"
ISO_ROOT="$GENERATED/iso-root"           # The Bootloader staging area
SQUASHFS_ROOT="$GENERATED/work/squashfs-root" # The Living Quarters (Filesystem)
FURRYOS_SHARE="$SQUASHFS_ROOT/usr/share/furryos" # The Treasure Room (Assets)

# The temporary ISO used as the vehicle (deleted after use)
TEST_ISO="$GENERATED/mansion_portal.iso"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🦊 Opening the Portal to the Sovereign Mansion...        ║"
echo "╚════════════════════════════════════════════════════════════╝"

# ------------------------------------------------------------------------------
# [Phase 1] Validation & Safety Checks
# ------------------------------------------------------------------------------
# We cannot launch a mansion that hasn't been built yet.

if [ ! -d "$SQUASHFS_ROOT" ]; then
    echo "❌ ERROR: The Mansion (squashfs-root) was not found."
    echo "   Please run './build_furryos.sh' first to build the foundation."
    exit 1
fi

if [ ! -d "$ISO_ROOT/isolinux" ]; then
    echo "⚠️  WARNING: ISO Bootloader structure missing. Attempting to repair..."
    # If the user did a partial clean, we might need to regenerate this path
    mkdir -p "$ISO_ROOT/isolinux"
fi

# ------------------------------------------------------------------------------
# [Phase 2] Grounding the Boot Configuration
# ------------------------------------------------------------------------------
# This is where we "Write the Law" into the bootloader.
# We force the kernel to use the username 'anthro' and high-res graphics (vga=791).

echo "🔧 Grounding Boot Parameters (User: anthro | Res: 1024x768)..."

# Find all config files (.cfg) inside the ISO root and inject our will.
# We replace "boot=live" with our specific sovereignty flags.
sudo find "$ISO_ROOT" -name "*.cfg" -type f -exec sed -i \
    "s/boot=live/boot=live live-username=anthro vga=791/g" {} +

# ------------------------------------------------------------------------------
# [Phase 3] Branding the Threshold (BIOS Splash Fix)
# ------------------------------------------------------------------------------
# Ensure that even the BIOS boot menu shows Master Tempter's face.

echo "🖼️  Branding the Threshold..."

if [ -f "$FURRYOS_SHARE/splash/splash.png" ]; then
    # Copy the splash from the inner system to the outer bootloader
    sudo cp "$FURRYOS_SHARE/splash/splash.png" "$ISO_ROOT/isolinux/splash.png"

    # Patch the ISOLINUX config to actually USE the image.
    # 1. Set the background image
    sudo sed -i 's/menu background.*/menu background splash.png/g' "$ISO_ROOT/isolinux/menu.cfg" 2>/dev/null || true
    # 2. Remove the "stdmenu" include which often overrides our settings
    sudo sed -i 's/include stdmenu.cfg//g' "$ISO_ROOT/isolinux/menu.cfg" 2>/dev/null || true

    echo "   ✓ Splash screen applied to BIOS Menu."
else
    echo "   ⚠️  No splash.png found in payload. Using default blue theme."
fi

# ------------------------------------------------------------------------------
# [Phase 4] Rapid Synchronization (LZ4)
# ------------------------------------------------------------------------------
# We compress the folder into a read-only filesystem so the Kernel can mount it.
# We use LZ4 because it is nearly instant, allowing for rapid iteration.

echo "📦 Unpacking changes into the virtual medium..."

# Remove the old body
sudo rm -f "$ISO_ROOT/live/filesystem.squashfs"

# Create the new body (Using nice/ionice to prevent system freeze)
sudo nice -n 19 ionice -c 3 mksquashfs "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs" \
    -comp lz4 -noappend -b 256K -info

# ------------------------------------------------------------------------------
# [Phase 5] Finalizing the Portal (ISO Generation)
# ------------------------------------------------------------------------------
# We wrap the filesystem and bootloader into a bootable ISO image.

echo "💿 Stabilizing Boot Records..."

# Find the Hybrid MBR binary on the host system for maximum compatibility
MBR_BIN=$(find /usr/lib -name isohdpfx.bin 2>/dev/null | head -n 1 || echo "")

sudo nice -n 19 xorriso -as mkisofs \
    -iso-level 3 \
    -full-iso9660-filenames \
    -volid "FurryOS" \
    -eltorito-boot isolinux/isolinux.bin \
    -eltorito-catalog isolinux/boot.cat \
    -no-emul-boot -boot-load-size 4 -boot-info-table \
    ${MBR_BIN:+-isohybrid-mbr "$MBR_BIN"} \
    -output "$TEST_ISO" "$ISO_ROOT" 2>/dev/null

# ------------------------------------------------------------------------------
# [Phase 6] Entering the Mansion (QEMU Launch)
# ------------------------------------------------------------------------------
# We allocate High-End resources to ensure the AnthroHeart Ska plays smoothly.

# Resource Calculation: Use 3GB RAM if available, else 2GB
HOST_RAM=$(free -m | awk '/^Mem:/{print $2}')
if [ "$HOST_RAM" -gt 6000 ]; then
    VM_RAM="3072M" # 3GB for smooth performance
else
    VM_RAM="2048M" # 2GB Minimum
fi

echo "🚀 PORTAL OPEN: Master Tempter is arriving..."
echo "   • RAM: $VM_RAM"
echo "   • CPU: Host Passthrough (4 Cores)"
echo "   • VGA: Virtio (Accelerated)"

# Launch QEMU
# -cdrom: Fixes 'medium not found'
# -cpu host: Uses your actual processor instructions for speed
# -vga virtio + -display gtk,gl=on: Enables 3D acceleration for the desktop
sudo qemu-system-x86_64 \
    -cdrom "$TEST_ISO" \
    -m "$VM_RAM" \
    -smp cores=4,threads=1 \
    -enable-kvm \
    -cpu host \
    -vga virtio \
    -display gtk,gl=on,zoom-to-fit=on \
    -usb -device usb-tablet \
    -device virtio-net-pci,netdev=n1 -netdev user,id=n1

# ------------------------------------------------------------------------------
# [Phase 7] Cleanup & Closing
# ------------------------------------------------------------------------------
# Remove the temporary portal ISO to save space.

echo ""
echo "🧹 Closing the Portal..."
sudo rm -f "$TEST_ISO"
echo "✅ Session Complete. Welcome back to the physical realm."

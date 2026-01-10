#!/usr/bin/env bash
# ══════════════════════════════════════════════════════════════════════════════
#  🐾 FurryOS Gen2.1_v2: The Sovereign Universe Build Engine
# ══════════════════════════════════════════════════════════════════════════════
#  Lead Architect: Thomas B. Sweet (Anthro Entertainment LLC)
#  Franchise Lore: AnthroHeart Saga / Warlock Name Universe (est. 2004)
#  Technical Base: Debian 13 (Trixie/Testing)
#  License: MIT
# ══════════════════════════════════════════════════════════════════════════════

# [Init] Start the Chronometer
BUILD_START_TIME=$(date +%s)

# [Init] Safety First: Exit immediately if any command fails
set -e

# ------------------------------------------------------------------------------
# [Phase 0] Path Configuration & Resource Logic
# ------------------------------------------------------------------------------
# We define the "Sacred Geometry" of the build folders here.

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"
PARENT_DIR="$(cd "$PROJECT_ROOT/.." && pwd)"

# The "Backstage" areas where the messy work happens
GENERATED="$PARENT_DIR/_generated"
BUILD_DIR="$PARENT_DIR/build"

# The specific staging grounds
ISO_DIR="$GENERATED/iso"                 # Where we download the base Debian ISO
WORK_DIR="$GENERATED/work"               # Temporary scratch space
ISO_ROOT="$GENERATED/iso-root"           # The unpacked ISO structure (Bootloader, Menus)
SQUASHFS_ROOT="$WORK_DIR/squashfs-root"  # The unpacked Linux Filesystem (The Mansion)
OUTPUT_DIR="$BUILD_DIR/output"           # Where the final "Jewel" is placed

# [Init] Logging System
# We capture every breath of the machine into a log file.
LOG_FILE="build_$(date +%Y%m%d_%H%M%S).log"
exec > >(tee -a "$LOG_FILE") 2>&1
echo "📝 Logging active: $LOG_FILE"

echo "╔════════════════════════════════════════════════════════════╗"
echo "║   🐾 FurryOS Gen2.1_v2: Sovereign Universe Build Engine    ║"
echo "╚════════════════════════════════════════════════════════════╝"

# [Phase 0.1] Resource Calculation (The "Polite" Logic)
# We calculate 75% of available RAM to ensure the build never freezes your PC.
if command -v free >/dev/null 2>&1; then
    AVAIL_GB=$(free --giga | awk '/^Mem:/ {print int($7)}')
    SQUASH_MEM=$((AVAIL_GB * 75 / 100))

    # Safety bounds: Minimum 2G, Maximum 20G
    [ "$SQUASH_MEM" -lt 2 ] && SQUASH_MEM=2
    [ "$SQUASH_MEM" -gt 20 ] && SQUASH_MEM=20

    echo "📊 System Health Check:"
    echo "   • Available RAM: ${AVAIL_GB} GB"
    echo "   • Allocated to Compression: ${SQUASH_MEM} GB (75% Cap)"
else
    SQUASH_MEM="4"
    echo "⚠️  'free' command not found. Defaulting to 4GB RAM allocation."
fi

# [Phase 0.2] The "Redemption" Menu
# Allows you to skip the heavy lifting if you just want to tweak assets.
echo ""
echo "Select Build Mode:"
echo "  [C] Clean Everything  (Fresh Start - Recommended for Kernel changes)"
echo "  [K] Keep Folders      (Incremental - Recommended for Asset/Lore tweaks)"
echo "  [D] Keep ISO Only     (Redownload safety)"
echo ""
read -p "Selection [C]: " -n 1 -r BUILD_MODE
echo ""

# Handle the cleanup logic based on choice
case ${BUILD_MODE,,} in
    k )
        echo "➡️  KEEP MODE ACTIVE: Preserving the Mansion structure..."
        ;;
    d )
        echo "💾 Protecting Base ISO, cleaning workspace..."
        sudo umount -l "$SQUASHFS_ROOT" "$ISO_ROOT" 2>/dev/null || true
        sudo rm -rf "$WORK_DIR" "$ISO_ROOT"
        ;;
    * )
        echo "🔥 FULL PURGE: Cleaning all previous timelines..."
        sudo umount -l "$SQUASHFS_ROOT" "$ISO_ROOT" 2>/dev/null || true
        sudo rm -rf "$BUILD_DIR" "$GENERATED" "$WORK_DIR" "$ISO_ROOT"
        ;;
esac

# Create the skeleton directories
mkdir -p "$OUTPUT_DIR" "$ISO_DIR" "$WORK_DIR" "$ISO_ROOT"

# ------------------------------------------------------------------------------
# [Phase 1] Base System Extraction (The "Unpacking")
# ------------------------------------------------------------------------------
ISO_FILE="$ISO_DIR/debian-live-mate-amd64.iso"
# Using the reliable Debian Global Mirror
ISO_URL="https://cdimage.debian.org/debian-cd/current-live/amd64/iso-hybrid/debian-live-13.2.0-amd64-mate.iso"

if [ ! -f "$ISO_FILE" ]; then
    echo "⬇️  Downloading Debian 13 Base (The Foundation)..."
    curl -L "$ISO_URL" -o "$ISO_FILE"
fi

# [Phase 1.1] Extract ISO Structure (Bootloaders, EFI)
if [[ ${BUILD_MODE,,} == "k" && -d "$ISO_ROOT/live" ]]; then
    echo "✅ ISO structure grounded. Skipping extraction."
else
    echo "[Phase 1.1] Extracting ISO structure..."
    sudo rm -rf "$ISO_ROOT" && mkdir -p "$ISO_ROOT"
    sudo bsdtar -C "$ISO_ROOT" -xf "$ISO_FILE"
fi

# [Phase 1.2] Extract Filesystem (The Heavy Lift)
if [[ ${BUILD_MODE,,} == "k" && -d "$SQUASHFS_ROOT/etc" ]]; then
    echo "✅ Filesystem grounded. Skipping unsquash."
else
    echo "[Phase 1.2] Extracting Master Filesystem (Unsquashing the 5D Node)..."
    sudo rm -rf "$SQUASHFS_ROOT" && mkdir -p "$SQUASHFS_ROOT"
    sudo unsquashfs -f -d "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs"

    # Permission Fix: We take ownership so we can edit without constant sudo later
    echo "   • Adjusting permissions..."
    sudo chown -R "$USER":"$USER" "$SQUASHFS_ROOT"
fi

# ------------------------------------------------------------------------------
# [Phase 2] The Universal Bridge (Chroot Prep)
# ------------------------------------------------------------------------------
echo "[Phase 2] Grounding the Chroot Bridge..."

# 1. DNS Fix: Copy the host's phonebook so the Chroot can find the internet
sudo cp /etc/resolv.conf "$SQUASHFS_ROOT/etc/resolv.conf"

# 2. Hardware Bridge: Mount the host's devices into the Chroot
# This fixes the "cannot write log" and "posix_openpt" errors.
echo "   • Mounting virtual filesystems..."
for mp in /dev /dev/pts /proc /sys /run; do
    sudo mount --bind "$mp" "$SQUASHFS_ROOT$mp" 2>/dev/null || true
done

# [Phase 2.1] Injecting Developer Tools (Monastic Mode)
echo "[Phase 2.1] Injecting Core Packages (Monastic Mode LC_ALL=C)..."

# We use LC_ALL=C to silence the "Perl Locale" warnings.
# We install 'pulseaudio-utils' to ensure 'paplay' works for your Ska songs.
sudo chroot "$SQUASHFS_ROOT" /usr/bin/env LC_ALL=C LANGUAGE=C LANG=C bash -c "
    export DEBIAN_FRONTEND=noninteractive

    echo '   • Updating Repositories...'
    apt-get update -qq

    echo '   • Installing The Sovereign Toolkit...'
    apt-get install -y -qq \
        vlc geeqie ffmpeg \
        mate-utils \
        fonts-jetbrains-mono \
        p7zip-full lz4 \
        xdg-user-dirs dconf-cli \
        pulseaudio-utils \
        locales

    echo '   • Generating Locales...'
    echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen
    locale-gen -q || true

    echo '   • Cleaning up...'
    apt-get clean
"

# 3. Close the Bridge: Unmount everything to keep the host safe
echo "   • Unmounting virtual filesystems..."
for mp in /dev/pts /dev /proc /sys /run; do
    sudo umount -l "$SQUASHFS_ROOT$mp" 2>/dev/null || true
done

# ------------------------------------------------------------------------------
# [Phase 3] Absolute Asset Deployment
# ------------------------------------------------------------------------------
echo "[Phase 3] Deploying FurryOS Master Assets..."

FURRYOS_SHARE="$SQUASHFS_ROOT/usr/share/furryos"

# Force clean the target directory in the ISO to ensure no old files remain
sudo rm -rf "$FURRYOS_SHARE"
sudo mkdir -p "$FURRYOS_SHARE"

# Copy the assets from your project folder
if [ -d "$PROJECT_ROOT/payload/assets" ]; then
    echo "   • Injecting 20 Years of Lore into /usr/share/furryos..."
    sudo cp -ra "$PROJECT_ROOT/payload/assets/." "$FURRYOS_SHARE/"
else
    echo "❌ ERROR: Payload not found! Please check $PROJECT_ROOT/payload/assets"
    exit 1
fi

# ------------------------------------------------------------------------------
# [Phase 4] The "Sovereign" Setup Script (Audio/Visual Core)
# ------------------------------------------------------------------------------
echo "[Phase 4] Generating the Sovereign Internal Controller..."

cat << 'EOF' | sudo tee "$SQUASHFS_ROOT/usr/local/bin/furryos-live-setup" > /dev/null
#!/bin/bash
# --- Runs on boot inside the ISO ---
sleep 5
L_USER=$(whoami)
L_HOME="/home/$L_USER"
SRC="/usr/share/furryos"
DEST="$L_HOME/FurryOS"

# 1. Physical Grounding (Asset Copy)
mkdir -p "$DEST"
cp -ra "$SRC/." "$DEST/"
chown -R $L_USER:$L_USER "$L_HOME"
xdg-user-dirs-update

# 2. UI Calibration (XSO Wallpaper)
export GSETTINGS_BACKEND=dconf
export $(dbus-launch)

# Force the XSO Rainbow Fox Wallpaper
if [ -f "$DEST/wallpapers/default.jpg" ]; then
    gsettings set org.mate.desktop.background picture-filename "$DEST/wallpapers/default.jpg"
    gsettings set org.mate.desktop.background picture-options 'zoom'
fi

# 🐾 Terminal Injection (Ember-Night)
PR="/org/mate/terminal/profiles/default"
dconf write $PR/use-theme-colors false
dconf write $PR/background-color "'#1A1414'"
dconf write $PR/foreground-color "'#FEE2E2'"
dconf write $PR/font "'JetBrains Mono Medium 13'"

# 3. Audio Proclamation (Startup Sound)
if [ -f "$DEST/sounds/startup.ogg" ]; then
    (sleep 2 && paplay "$DEST/sounds/startup.ogg" || aplay "$DEST/sounds/startup.ogg") &
fi
EOF
sudo chmod +x "$SQUASHFS_ROOT/usr/local/bin/furryos-live-setup"

# --- SHUTDOWN SOUND LOGIC ---
# Create a helper script that plays the sound
cat << 'EOF' | sudo tee "$SQUASHFS_ROOT/usr/local/bin/furryos-shutdown-sound" > /dev/null
#!/bin/bash
SOUND="/home/anthro/FurryOS/sounds/shutdown.ogg"
if [ -f "$SOUND" ]; then
    paplay "$SOUND" || aplay "$SOUND"
fi
EOF
sudo chmod +x "$SQUASHFS_ROOT/usr/local/bin/furryos-shutdown-sound"

# ------------------------------------------------------------------------------
# [Phase 5] Autostart Registration (Startup & Shutdown)
# ------------------------------------------------------------------------------
echo "[Phase 5] Registering Lifecycle Hooks..."
sudo mkdir -p "$SQUASHFS_ROOT/etc/skel/.config/autostart"

# 1. Register Startup Script
cat << 'EOF' | sudo tee "$SQUASHFS_ROOT/etc/skel/.config/autostart/furryos-setup.desktop" > /dev/null
[Desktop Entry]
Type=Application
Name=FurryOS Setup
Exec=/usr/local/bin/furryos-live-setup
Terminal=false
X-MATE-Autostart-enabled=true
EOF

# 2. Register Shutdown Listener
# This runs in the background and waits for the "EXIT" signal (Logout/Shutdown)
cat << 'EOF' | sudo tee "$SQUASHFS_ROOT/etc/skel/.config/autostart/furryos-shutdown-listener.desktop" > /dev/null
[Desktop Entry]
Type=Application
Name=FurryOS Shutdown Listener
Exec=/bin/bash -c 'trap "/usr/local/bin/furryos-shutdown-sound" EXIT; sleep infinity'
Terminal=false
NoDisplay=true
X-MATE-Autostart-enabled=true
EOF

# ------------------------------------------------------------------------------
# [Phase 6] Boot Branding (BIOS & UEFI)
# ------------------------------------------------------------------------------
echo "[Phase 6] Branding the Threshold (Boot Splash)..."

if [ -f "$FURRYOS_SHARE/splash/splash.png" ]; then
    # 1. GRUB (UEFI Mode)
    sudo mkdir -p "$SQUASHFS_ROOT/boot/grub"
    sudo cp "$FURRYOS_SHARE/splash/splash.png" "$SQUASHFS_ROOT/boot/grub/splash.png"

    # 2. ISOLINUX (BIOS Mode)
    # We must copy this to ISO_ROOT because ISOLINUX lives outside the SquashFS
    sudo mkdir -p "$ISO_ROOT/isolinux"
    sudo cp "$FURRYOS_SHARE/splash/splash.png" "$ISO_ROOT/isolinux/splash.png"

    # Patch the BIOS config to use the image
    sudo sed -i 's/menu background.*/menu background splash.png/g' "$ISO_ROOT/isolinux/menu.cfg" 2>/dev/null || true
    # Remove the standard menu include to force our style
    sudo sed -i 's/include stdmenu.cfg//g' "$ISO_ROOT/isolinux/menu.cfg" 2>/dev/null || true

    echo "   ✓ Splash screens applied to both BIOS and UEFI."
fi

# ------------------------------------------------------------------------------
# [Phase 7] Mode Switcher Core
# ------------------------------------------------------------------------------
echo "[Phase 7] Deploying Mode Switcher Logic..."

cat << 'EOF' | sudo tee "$SQUASHFS_ROOT/usr/local/bin/furryos-mode" > /dev/null
#!/bin/bash
# Logic for switching between Granny, Hacker, and Ghost modes
MODE=$1
case $MODE in
  hacker) gsettings set org.mate.interface gtk-theme 'BlackMATE' ;;
  granny) gsettings set org.mate.interface font-name 'Sans 14' ;;
  ghost)  nmcli connection modify id "Wired connection 1" ipv4.dns "9.9.9.9" ;;
  *) echo "Usage: furryos-mode [hacker|granny|ghost]" ;;
esac
EOF
sudo chmod +x "$SQUASHFS_ROOT/usr/local/bin/furryos-mode"

# ------------------------------------------------------------------------------
# [Phase 8.5] The Test Drive (Stability-First Portal)
# ------------------------------------------------------------------------------
echo ""
echo "🚗 [Phase 8.5] Test Drive Checkpoint"
read -p "   Launch QEMU to verify the Mansion? [y/N]: " -r TEST_DRIVE

if [[ $TEST_DRIVE =~ ^[Yy]$ ]]; then
    echo "📦 Rapid-Packing for Test (Priority: LOW to prevent host freeze)..."
    TEST_ISO="$GENERATED/test_drive.iso"

    # Clean up old test artifacts
    sudo rm -f "$ISO_ROOT/live/filesystem.squashfs"

    # USE 'nice' and 'ionice' so your PC doesn't freeze!
    # USE LZ4 for speed (Seconds instead of minutes)
    sudo nice -n 19 ionice -c 3 mksquashfs "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs" \
        -comp lz4 -noappend -b 256K -info

    # GROUNDING PARAMETERS: Force 'anthro' username directly into boot configs
    echo "   • Grounding Username 'anthro' in bootloaders..."
    sudo find "$ISO_ROOT" -name "*.cfg" -type f -exec sed -i "s/boot=live/boot=live live-username=anthro vga=791/g" {} +

    echo "💿 Creating Test ISO..."
    sudo nice -n 19 xorriso -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid "FurryOS" \
        -eltorito-boot isolinux/isolinux.bin \
        -eltorito-catalog isolinux/boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        -output "$TEST_ISO" "$ISO_ROOT" 2>/dev/null

    echo "🚀 Portal Open. High-Resolution Mode Active."

    # QEMU LAUNCHER
    # -cdrom: Fixes 'medium not found'
    # -m 2G: Enough RAM for smooth playback
    # NO -append: Because we patched the ISO directly!
    sudo qemu-system-x86_64 \
        -cdrom "$TEST_ISO" \
        -m 2G \
        -smp 4 \
        -enable-kvm \
        -vga virtio \
        -display gtk,gl=on,zoom-to-fit=on \
        -usb -device usb-tablet

    # Cleanup
    sudo rm -f "$TEST_ISO"
fi

# ------------------------------------------------------------------------------
# [Phase 9/10] High-Density XZ Packing (The Final Sovereign Release)
# ------------------------------------------------------------------------------
echo ""
echo "🚀 [Phase 9] Finalization"
read -p "   Pack final High-Density XZ ISO? [P/e]: " -n 1 -r NEXT_STEP
echo ""

if [[ ${NEXT_STEP,,} != "e" ]]; then
    echo "[Phase 9] Repacking SquashFS (High-Density XZ Mode)..."
    echo "   • This may take time. Master Tempter is compressing the timeline..."

    sudo rm -f "$ISO_ROOT/live/filesystem.squashfs"

    # XZ Compression: Slow, but creates the smallest, fastest-loading ISO
    sudo nice -n 19 mksquashfs "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs" \
        -comp xz -b 1048576 -mem "${SQUASH_MEM}G" -noappend >/dev/null

    echo "[Phase 10] Finalizing bootable ISO..."

    # Re-Apply the Grounding (Force 'anthro' username)
    sudo find "$ISO_ROOT" -name "*.cfg" -type f -exec sed -i 's/boot=live/boot=live live-username=anthro/g' {} +

    OUTPUT_ISO="$OUTPUT_DIR/furryos-gen2.1-v2.iso"

    # Find Hybrid MBR for maximum BIOS compatibility
    MBR_BIN=$(find /usr/lib -name isohdpfx.bin 2>/dev/null | head -n 1 || echo "")

    sudo xorriso -as mkisofs \
        -iso-level 3 \
        -full-iso9660-filenames \
        -volid "FurryOS" \
        -eltorito-boot isolinux/isolinux.bin \
        -eltorito-catalog isolinux/boot.cat \
        -no-emul-boot -boot-load-size 4 -boot-info-table \
        ${MBR_BIN:+-isohybrid-mbr "$MBR_BIN"} \
        -output "$OUTPUT_ISO" "$ISO_ROOT" 2>/dev/null

    echo ""
    echo "✅ MASTERPIECE CREATED: $OUTPUT_ISO"
    echo "   The Sovereign Universe is ready for distribution."
fi

# [Final] Time Calculation
BUILD_END_TIME=$(date +%s)
DURATION=$((BUILD_END_TIME - BUILD_START_TIME))
echo "⏱️  Total build time: $((DURATION / 60))m $((DURATION % 60))s"

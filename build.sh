#!/bin/bash
# FurryOS Master Build Script (Golden Master)
# Usage: sudo ./build.sh

set -e

# Configuration
OS_NAME="FurryOS"
CODENAME="trixie" # Debian 13
ARCH="amd64"
DATE=$(date +%Y%m%d)

# 1. Check Root
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo ./build.sh)"
  exit 1
fi

echo "🦊 Starting FurryOS Build [$DATE]..."

# 2. Clean Previous Build
lb clean

# 3. Configure
lb config \
    --distribution $CODENAME \
    --architecture $ARCH \
    --archive-areas "main contrib non-free-firmware" \
    --bootappend-live "boot=live components quiet splash hostname=furryos persistence" \
    --linux-packages "linux-image linux-headers" \
    --iso-volume "$OS_NAME Live $DATE" \
    --iso-application "$OS_NAME" \
    --memtest none

# 4. Inject Assets & Configs
echo "🎨 Injecting configuration..."
mkdir -p config/includes.chroot/usr/share/backgrounds/furryos/
mkdir -p config/includes.chroot/usr/share/icons/furryos/
mkdir -p config/includes.chroot/etc/skel/Desktop/

# Smart Asset Copy
if [ -d "assets/wallpapers" ]; then
    rsync -av assets/wallpapers/* config/includes.chroot/usr/share/backgrounds/furryos/
fi
if [ -d "assets/icons" ]; then
    rsync -av assets/icons/* config/includes.chroot/usr/share/icons/furryos/
fi

# 5. Build
echo "🚀 Building ISO..."
lb build

# 6. Finalize
if [ -f "live-image-amd64.hybrid.iso" ]; then
    mv live-image-amd64.hybrid.iso FurryOS_GoldenMaster.iso
    # Fix ownership so you can touch it
    chown $SUDO_USER:$SUDO_USER FurryOS_GoldenMaster.iso
    echo "✅ BUILD SUCCESSFUL: FurryOS_GoldenMaster.iso"
else
    echo "❌ Build failed. Check build.log"
fi

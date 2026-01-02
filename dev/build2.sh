#!/bin/bash
# FurryOS Build System v8.1.0
# Steam-Fixed Edition - Generated 2026-01-01 11:44:52

set -e
set -o pipefail

OS_NAME="Furryos"
CODENAME="trixie"
ARCH="amd64"
DATE=$(date +%Y%m%d)
BUILD_LOG="build-${DATE}.log"

GREEN='\033[0;32m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

log_info() { echo -e "${BLUE}[INFO]${NC} $1" | tee -a "$BUILD_LOG"; }
log_success() { echo -e "${GREEN}[SUCCESS]${NC} $1" | tee -a "$BUILD_LOG"; }
log_error() { echo -e "${RED}[ERROR]${NC} $1" | tee -a "$BUILD_LOG"; }

if [ "$EUID" -ne 0 ]; then
    log_error "This script must be run as root (use sudo)"
    exit 1
fi

log_info "============================================"
log_info "${OS_NAME} Build System v8.1.0"
log_info "============================================"

for cmd in lb rsync debootstrap; do
    if ! command -v "$cmd" &> /dev/null; then
        log_error "Missing dependency: $cmd"
        log_info "Install with: sudo apt install live-build rsync debootstrap"
        exit 1
    fi
done

log_info "Cleaning previous build artifacts..."
lb clean --purge 2>&1 | tee -a "$BUILD_LOG"
rm -f *.iso

log_info "Configuring live-build for Debian ${CODENAME}..."
lb config \
    --distribution "$CODENAME" \
    --architecture "$ARCH" \
    --archive-areas "main contrib non-free non-free-firmware" \
    --security true \
    --updates true \
    --bootappend-live "boot=live components quiet splash hostname=furryos" \
    --linux-packages "linux-image linux-headers" \
    --iso-volume "${OS_NAME}_Live_${DATE}" \
    --iso-application "${OS_NAME}" \
    --iso-publisher "Anthro Entertainment LLC" \
    --memtest none \
    2>&1 | tee -a "$BUILD_LOG"

log_info "Injecting assets and configurations..."
mkdir -p config/includes.chroot/usr/share/backgrounds/furryos
mkdir -p config/includes.chroot/usr/share/icons/furryos
mkdir -p config/includes.chroot/etc/skel/Desktop
mkdir -p config/includes.chroot/usr/local/bin
mkdir -p config/hooks/live

if [ -d "assets/wallpapers" ]; then
    log_info "Copying wallpapers..."
    rsync -a assets/wallpapers/ config/includes.chroot/usr/share/backgrounds/furryos/
fi

if [ -d "assets/icons" ]; then
    log_info "Copying icons..."
    rsync -a assets/icons/ config/includes.chroot/usr/share/icons/furryos/
fi

if [ -f "config/includes.chroot/usr/local/bin/furry-admin" ]; then
    chmod +x config/includes.chroot/usr/local/bin/furry-admin
fi

chmod +x config/hooks/live/*.hook.chroot 2>/dev/null || true

log_info "Building ISO (this will take a while)..."
if lb build 2>&1 | tee -a "$BUILD_LOG"; then
    log_success "ISO build completed!"
else
    log_error "ISO build failed! Check $BUILD_LOG for details."
    exit 1
fi

ISO_FILENAME="${OS_NAME}_v8.1.0_${DATE}.iso"

if [ -f "live-image-${ARCH}.hybrid.iso" ]; then
    mv "live-image-${ARCH}.hybrid.iso" "$ISO_FILENAME"

    if [ -n "$SUDO_USER" ]; then
        chown "$SUDO_USER:$SUDO_USER" "$ISO_FILENAME"
    fi

    sha256sum "$ISO_FILENAME" > "${ISO_FILENAME}.sha256"
    if [ -n "$SUDO_USER" ]; then
        chown "$SUDO_USER:$SUDO_USER" "${ISO_FILENAME}.sha256"
    fi

    log_success "============================================"
    log_success "BUILD SUCCESSFUL!"
    log_success "============================================"
    log_success "ISO: $ISO_FILENAME"
    log_success "Size: $(du -h "$ISO_FILENAME" | cut -f1)"
    log_success "SHA256: $(cat "${ISO_FILENAME}.sha256" | cut -d' ' -f1)"
    log_success "Log: $BUILD_LOG"
else
    log_error "Build failed - no ISO file generated!"
    log_error "Check $BUILD_LOG for details"
    exit 1
fi

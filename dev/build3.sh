#!/bin/bash
################################################################################
# FurryOS Complete Build System v3.1
# "I designed the OS, and AI wrote the code."
################################################################################

set -e
set -o pipefail
set -u

# Configuration
readonly OS_NAME="Furryos"
readonly VERSION="8.1.0"
readonly DEBIAN_RELEASE="trixie"
readonly ARCH="amd64"
readonly DATE=$(date +%Y%m%d-%H%M%S)
readonly BUILD_LOG="build-${DATE}.log"

readonly WORK_DIR="$(pwd)"
readonly PARENT_DIR="$(dirname "$WORK_DIR")"
readonly BUILD_OUTPUT_DIR="$PARENT_DIR/FurryOS-Builds"

# Colors
readonly C_GREEN='\033[0;32m'
readonly C_BLUE='\033[0;34m'
readonly C_RED='\033[0;31m'
readonly C_YELLOW='\033[0;33m'
readonly C_NC='\033[0m'

log_info() { 
    echo -e "${C_BLUE}[INFO]${C_NC} ${*}" | tee -a "$BUILD_LOG"
}

log_success() { 
    echo -e "${C_GREEN}[SUCCESS]${C_NC} ${*}" | tee -a "$BUILD_LOG"
}

log_error() { 
    echo -e "${C_RED}[ERROR]${C_NC} ${*}" | tee -a "$BUILD_LOG"
}

log_warning() {
    echo -e "${C_YELLOW}[WARNING]${C_NC} ${*}" | tee -a "$BUILD_LOG"
}

log_section() {
    echo "" | tee -a "$BUILD_LOG"
    echo -e "${C_BLUE}========================================${C_NC}" | tee -a "$BUILD_LOG"
    echo -e "${C_BLUE}${*}${C_NC}" | tee -a "$BUILD_LOG"
    echo -e "${C_BLUE}========================================${C_NC}" | tee -a "$BUILD_LOG"
}

check_root() {
    if [ "$EUID" -ne 0 ]; then
        log_error "This script must be run as root"
        log_info "Usage: sudo ./build3.sh"
        exit 1
    fi
}

check_dependencies() {
    log_info "Checking dependencies..."

    local missing=()
    for cmd in lb rsync debootstrap xorriso mksquashfs; do
        if ! command -v "$cmd" &>/dev/null; then
            missing+=("$cmd")
        fi
    done

    if [ ${#missing[@]} -gt 0 ]; then
        log_error "Missing: ${missing[*]}"
        log_info "Install: sudo apt install live-build rsync debootstrap xorriso squashfs-tools"
        exit 1
    fi

    log_success "Dependencies OK"
}

cleanup_environment() {
    log_section "Cleaning Environment"

    log_info "Running lb clean --purge..."
    lb clean --purge 2>&1 | tee -a "$BUILD_LOG" || true

    log_info "Removing old ISOs..."
    rm -f *.iso *.iso.* 2>/dev/null || true

    log_success "Cleaned"
}

configure_system() {
    log_section "Configuring Live-Build"

    log_info "Distribution: $DEBIAN_RELEASE"
    log_info "Architecture: $ARCH"

    lb config \
        --distribution "$DEBIAN_RELEASE" \
        --architecture "$ARCH" \
        --archive-areas "main contrib non-free non-free-firmware" \
        --security true \
        --updates true \
        --backports false \
        --bootappend-live "boot=live components quiet splash hostname=furryos persistence username=anthro" \
        --linux-packages "linux-image linux-headers" \
        --iso-volume "${OS_NAME}_${VERSION}_${DATE}" \
        --iso-application "$OS_NAME" \
        --iso-publisher "Anthro Entertainment LLC" \
        --memtest none \
        --checksums sha256 \
        2>&1 | tee -a "$BUILD_LOG"

    log_success "Configured"
}

inject_assets() {
    log_section "Injecting Assets"

    local chroot="config/includes.chroot"

    # Create directory structure
    log_info "Creating directory structure..."
    mkdir -p "${chroot}/usr/share/backgrounds/furryos"
    mkdir -p "${chroot}/usr/share/icons/furryos"
    mkdir -p "${chroot}/usr/share/sounds/furryos"
    mkdir -p "${chroot}/usr/share/furryos/lore"
    mkdir -p "${chroot}/usr/share/pixmaps"
    mkdir -p "${chroot}/etc/skel/Desktop"
    mkdir -p "${chroot}/etc/skel/Music/FurryOS_Soundtrack"
    mkdir -p "${chroot}/etc/skel/Documents/FurryOS_Lore"

    # Wallpapers
    if [ -d "assets/wallpapers" ]; then
        log_info "Copying wallpapers..."
        rsync -a assets/wallpapers/ "${chroot}/usr/share/backgrounds/furryos/" 2>&1 | tee -a "$BUILD_LOG"
        local count=$(find assets/wallpapers -type f 2>/dev/null | wc -l)
        log_success "Wallpapers: $count files"
    else
        log_warning "No wallpapers directory found"
    fi

    # Icons
    if [ -d "assets/icons" ]; then
        log_info "Copying icons..."
        rsync -a assets/icons/ "${chroot}/usr/share/icons/furryos/" 2>&1 | tee -a "$BUILD_LOG"
        find assets/icons -name "*.png" -exec cp {} "${chroot}/usr/share/pixmaps/" \; 2>/dev/null || true
        local count=$(find assets/icons -type f 2>/dev/null | wc -l)
        log_success "Icons: $count files"
    else
        log_warning "No icons directory found"
    fi

    # Sounds & Music
    if [ -d "assets/sounds" ]; then
        log_info "Copying sounds & music..."
        rsync -a assets/sounds/ "${chroot}/usr/share/sounds/furryos/" 2>&1 | tee -a "$BUILD_LOG"
        rsync -a assets/sounds/ "${chroot}/etc/skel/Music/FurryOS_Soundtrack/" 2>&1 | tee -a "$BUILD_LOG"
        local count=$(find assets/sounds -type f 2>/dev/null | wc -l)
        log_success "Audio: $count files"
    else
        log_warning "No sounds directory found"
    fi

    # Splash
    if [ -d "assets/splash" ]; then
        log_info "Copying splash screen..."
        mkdir -p "${chroot}/usr/share/plymouth/themes/furryos"
        rsync -a assets/splash/ "${chroot}/usr/share/plymouth/themes/furryos/" 2>&1 | tee -a "$BUILD_LOG"
        log_success "Splash injected"
    else
        log_warning "No splash directory found"
    fi

    # Lore
    if [ -d "assets/lore" ]; then
        log_info "Copying lore documents..."
        rsync -a assets/lore/ "${chroot}/usr/share/furryos/lore/" 2>&1 | tee -a "$BUILD_LOG"
        rsync -a assets/lore/ "${chroot}/etc/skel/Documents/FurryOS_Lore/" 2>&1 | tee -a "$BUILD_LOG"
        local count=$(find assets/lore -type f 2>/dev/null | wc -l)
        log_success "Lore: $count files"
    else
        log_warning "No lore directory found"
    fi

    # Set permissions on hooks
    if [ -d "config/hooks/live" ]; then
        log_info "Setting hook permissions..."
        chmod +x config/hooks/live/*.hook.chroot 2>/dev/null || true
    fi

    log_success "Asset injection complete"
}

build_iso() {
    log_section "Building ISO"

    log_info "Starting ISO build (this will take 15-45 minutes)..."
    log_info "Build log: $BUILD_LOG"

    local start_time=$(date +%s)

    if lb build 2>&1 | tee -a "$BUILD_LOG"; then
        local end_time=$(date +%s)
        local duration=$((end_time - start_time))
        local minutes=$((duration / 60))
        local seconds=$((duration % 60))

        log_success "Built in ${minutes}m ${seconds}s"
    else
        log_error "Build failed!"
        log_error "Check $BUILD_LOG for details"
        exit 1
    fi
}

finalize_iso() {
    log_section "Finalizing ISO"

    local iso_name="${OS_NAME}_v${VERSION}_${DATE}.iso"
    local source="live-image-${ARCH}.hybrid.iso"

    if [ ! -f "$source" ]; then
        log_error "No ISO file generated: $source"
        exit 1
    fi

    log_info "Creating output directory..."
    mkdir -p "$BUILD_OUTPUT_DIR"

    log_info "Moving ISO to output directory..."
    mv "$source" "$BUILD_OUTPUT_DIR/$iso_name"

    log_info "Generating checksum..."
    (cd "$BUILD_OUTPUT_DIR" && sha256sum "$iso_name" > "${iso_name}.sha256")

    # Fix ownership if running via sudo
    if [ -n "${SUDO_USER:-}" ]; then
        log_info "Fixing file ownership..."
        chown "$SUDO_USER:$SUDO_USER" "$BUILD_OUTPUT_DIR/$iso_name"*
    fi

    local size=$(du -h "$BUILD_OUTPUT_DIR/$iso_name" | cut -f1)

    log_success "ISO: $iso_name"
    log_success "Size: $size"
    log_success "Location: $BUILD_OUTPUT_DIR"
}

move_artifacts() {
    log_section "Cleaning Repository"

    log_info "Moving build artifacts outside repository..."

    if [ -d "chroot" ]; then
        log_info "Moving chroot..."
        rm -rf "$PARENT_DIR/FurryOS-Chroot" 2>/dev/null || true
        mv chroot "$PARENT_DIR/FurryOS-Chroot" 2>&1 | tee -a "$BUILD_LOG" || true
    fi

    if [ -d "binary" ]; then
        log_info "Moving binary..."
        rm -rf "$PARENT_DIR/FurryOS-Binary" 2>/dev/null || true
        mv binary "$PARENT_DIR/FurryOS-Binary" 2>&1 | tee -a "$BUILD_LOG" || true
    fi

    if [ -d "cache" ]; then
        log_info "Moving cache..."
        rm -rf "$PARENT_DIR/FurryOS-Cache" 2>/dev/null || true
        mv cache "$PARENT_DIR/FurryOS-Cache" 2>&1 | tee -a "$BUILD_LOG" || true
    fi

    if [ -d ".build" ]; then
        rm -rf "$PARENT_DIR/FurryOS-Build-Metadata" 2>/dev/null || true
        mv .build "$PARENT_DIR/FurryOS-Build-Metadata" 2>&1 | tee -a "$BUILD_LOG" || true
    fi

    if [ -f "$BUILD_LOG" ]; then
        cp "$BUILD_LOG" "$BUILD_OUTPUT_DIR/" 2>/dev/null || true
    fi

    log_success "Repository cleaned"
}

main() {
    log_section "Furryos v8.1.0 Build System"
    log_info "I designed the OS, and AI wrote the code."
    log_info "Build started: $(date)"
    echo ""

    check_root
    check_dependencies
    cleanup_environment
    configure_system
    inject_assets
    build_iso
    finalize_iso
    move_artifacts

    log_section "BUILD COMPLETE!"
    echo ""
    log_success "✅ ISO Location: $BUILD_OUTPUT_DIR"
    log_success "✅ Build Log: $BUILD_OUTPUT_DIR/$BUILD_LOG"
    log_success "✅ Repository Clean: Ready for Git"
    echo ""
    log_info "Default Credentials:"
    log_info "  • User: anthro / Password: anthro"
    log_info "  • Root: root / Password: root"
    echo ""
    log_info "Test your ISO:"
    log_info "  1. Burn to USB: sudo dd if=$BUILD_OUTPUT_DIR/${OS_NAME}_*.iso of=/dev/sdX bs=4M status=progress"
    log_info "  2. Or use in VM: VirtualBox/QEMU"
    echo ""
}

# Execute main function
main "$@"

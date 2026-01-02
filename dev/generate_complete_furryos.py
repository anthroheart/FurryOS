#!/usr/bin/env python3
"""
FurryOS Complete Asset Integration & Build System v3.1
"I designed the OS, and AI wrote the code."

Generates:
- Enhanced build3.sh with ALL asset integration
- Hooks for branding, wallpaper, icons, sounds, music
- Filename fixer (spaces → underscores)
"""

import os
import sys
from pathlib import Path

class CompleteFurryOSBuilder:
    def __init__(self):
        self.root = Path.cwd()
        self.config_dir = self.root / "config"

    def create_filename_fixer(self):
        """Script to rename files with spaces to underscores"""
        script = """#!/bin/bash
# fix_asset_filenames.sh
# Renames all asset files: spaces → underscores

echo "Fixing asset filenames (spaces → underscores)..."

find assets/ -depth -name "* *" -type f | while read -r file; do
    dir=$(dirname "$file")
    base=$(basename "$file")
    new="${base// /_}"

    if [ "$base" != "$new" ]; then
        mv -v "$file" "$dir/$new"
        echo "  ✓ $base → $new"
    fi
done

echo "✓ All filenames fixed!"
"""
        path = self.root / "fix_asset_filenames.sh"
        with open(path, 'w') as f:
            f.write(script)
        os.chmod(path, 0o755)
        print("✅ fix_asset_filenames.sh")

    def create_enhanced_build(self):
        """Enhanced build3.sh with complete asset integration"""
        # Load the build template from an external file would be cleaner,
        # but we'll inline it here
        script_path = self.root / "build3.sh"

        with open(script_path, 'w') as f:
            f.write("""#!/bin/bash
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
readonly C_GREEN='\\033[0;32m'
readonly C_BLUE='\\033[0;34m'
readonly C_RED='\\033[0;31m'
readonly C_NC='\\033[0m'

log_info() { echo -e "${C_BLUE}[INFO]${C_NC} ${*}" | tee -a "$BUILD_LOG"; }
log_success() { echo -e "${C_GREEN}[SUCCESS]${C_NC} ${*}" | tee -a "$BUILD_LOG"; }
log_error() { echo -e "${C_RED}[ERROR]${C_NC} ${*}" | tee -a "$BUILD_LOG"; }

log_section() {
    echo "" | tee -a "$BUILD_LOG"
    echo -e "${C_BLUE}========================================${C_NC}" | tee -a "$BUILD_LOG"
    echo -e "${C_BLUE}${*}${C_NC}" | tee -a "$BUILD_LOG"
    echo -e "${C_BLUE}========================================${C_NC}" | tee -a "$BUILD_LOG"
}

check_root() {
    [ "$EUID" -ne 0 ] && { log_error "Run as root: sudo ./build3.sh"; exit 1; }
}

check_dependencies() {
    log_info "Checking dependencies..."
    local missing=()
    for cmd in lb rsync debootstrap xorriso mksquashfs; do
        command -v "$cmd" &>/dev/null || missing+=("$cmd")
    done
    [ ${#missing[@]} -gt 0 ] && {
        log_error "Missing: ${missing[*]}"
        log_info "Install: sudo apt install live-build rsync debootstrap xorriso squashfs-tools"
        exit 1
    }
    log_success "Dependencies OK"
}

cleanup_environment() {
    log_section "Cleaning Environment"
    lb clean --purge 2>&1 | tee -a "$BUILD_LOG" || true
    rm -f *.iso *.iso.* 2>/dev/null || true
    log_success "Cleaned"
}

configure_system() {
    log_section "Configuring Live-Build"

    lb config \\
        --distribution "$DEBIAN_RELEASE" \\
        --architecture "$ARCH" \\
        --archive-areas "main contrib non-free non-free-firmware" \\
        --security true \\
        --updates true \\
        --backports false \\
        --bootappend-live "boot=live components quiet splash hostname=furryos persistence username=anthro" \\
        --linux-packages "linux-image linux-headers" \\
        --iso-volume "${OS_NAME}_${VERSION}_${DATE}" \\
        --iso-application "$OS_NAME" \\
        --iso-publisher "Anthro Entertainment LLC" \\
        --memtest none \\
        --checksums sha256 \\
        2>&1 | tee -a "$BUILD_LOG"

    log_success "Configured"
}

inject_assets() {
    log_section "Injecting Assets"

    local chroot="config/includes.chroot"

    # Directory structure
    mkdir -p "${chroot}/usr/share/backgrounds/furryos"
    mkdir -p "${chroot}/usr/share/icons/furryos"
    mkdir -p "${chroot}/usr/share/sounds/furryos"
    mkdir -p "${chroot}/usr/share/furryos/lore"
    mkdir -p "${chroot}/usr/share/pixmaps"
    mkdir -p "${chroot}/etc/skel/Desktop"
    mkdir -p "${chroot}/etc/skel/Music/FurryOS_Soundtrack"
    mkdir -p "${chroot}/etc/skel/Documents/FurryOS_Lore"

    # Wallpapers
    [ -d "assets/wallpapers" ] && {
        log_info "Wallpapers..."
        rsync -a assets/wallpapers/ "${chroot}/usr/share/backgrounds/furryos/"
        log_success "Wallpapers: $(find assets/wallpapers -type f 2>/dev/null | wc -l) files"
    }

    # Icons
    [ -d "assets/icons" ] && {
        log_info "Icons..."
        rsync -a assets/icons/ "${chroot}/usr/share/icons/furryos/"
        find assets/icons -name "*.png" -exec cp {} "${chroot}/usr/share/pixmaps/" \\; 2>/dev/null || true
        log_success "Icons: $(find assets/icons -type f 2>/dev/null | wc -l) files"
    }

    # Sounds & Music
    [ -d "assets/sounds" ] && {
        log_info "Sounds & Music..."
        rsync -a assets/sounds/ "${chroot}/usr/share/sounds/furryos/"
        rsync -a assets/sounds/ "${chroot}/etc/skel/Music/FurryOS_Soundtrack/"
        log_success "Audio: $(find assets/sounds -type f 2>/dev/null | wc -l) files"
    }

    # Splash
    [ -d "assets/splash" ] && {
        log_info "Splash screen..."
        mkdir -p "${chroot}/usr/share/plymouth/themes/furryos"
        rsync -a assets/splash/ "${chroot}/usr/share/plymouth/themes/furryos/"
        log_success "Splash injected"
    }

    # Lore
    [ -d "assets/lore" ] && {
        log_info "Lore..."
        rsync -a assets/lore/ "${chroot}/usr/share/furryos/lore/"
        rsync -a assets/lore/ "${chroot}/etc/skel/Documents/FurryOS_Lore/"
        log_success "Lore: $(find assets/lore -type f 2>/dev/null | wc -l) files"
    }

    # Permissions
    [ -d "config/hooks/live" ] && chmod +x config/hooks/live/*.hook.chroot 2>/dev/null || true

    log_success "Assets complete"
}

build_iso() {
    log_section "Building ISO"

    local start_time=$(date +%s)

    if lb build 2>&1 | tee -a "$BUILD_LOG"; then
        local duration=$(($(date +%s) - start_time))
        log_success "Built in $((duration / 60))m $((duration % 60))s"
    else
        log_error "Build failed!"
        exit 1
    fi
}

finalize_iso() {
    log_section "Finalizing"

    local iso_name="${OS_NAME}_v${VERSION}_${DATE}.iso"
    local source="live-image-${ARCH}.hybrid.iso"

    [ ! -f "$source" ] && { log_error "No ISO!"; exit 1; }

    mkdir -p "$BUILD_OUTPUT_DIR"
    mv "$source" "$BUILD_OUTPUT_DIR/$iso_name"
    (cd "$BUILD_OUTPUT_DIR" && sha256sum "$iso_name" > "${iso_name}.sha256")

    [ -n "${SUDO_USER:-}" ] && chown "$SUDO_USER:$SUDO_USER" "$BUILD_OUTPUT_DIR/$iso_name"*

    log_success "ISO: $iso_name ($(du -h "$BUILD_OUTPUT_DIR/$iso_name" | cut -f1))"
}

move_artifacts() {
    log_section "Cleaning Repository"

    [ -d "chroot" ] && mv chroot "$PARENT_DIR/FurryOS-Chroot" 2>/dev/null || true
    [ -d "binary" ] && mv binary "$PARENT_DIR/FurryOS-Binary" 2>/dev/null || true
    [ -d "cache" ] && mv cache "$PARENT_DIR/FurryOS-Cache" 2>/dev/null || true
    [ -d ".build" ] && mv .build "$PARENT_DIR/FurryOS-Build-Metadata" 2>/dev/null || true

    [ -f "$BUILD_LOG" ] && cp "$BUILD_LOG" "$BUILD_OUTPUT_DIR/"

    log_success "Repository clean"
}

main() {
    log_section "Furryos v8.1.0 Build System"
    log_info "I designed the OS, and AI wrote the code."

    check_root
    check_dependencies
    cleanup_environment
    configure_system
    inject_assets
    build_iso
    finalize_iso
    move_artifacts

    log_section "BUILD COMPLETE!"
    log_success "✅ ISO: $BUILD_OUTPUT_DIR"
    log_info "Credentials: anthro/anthro, root/root"
}

main "$@"
""")

        os.chmod(script_path, 0o755)
        print("✅ build3.sh (enhanced)")

    def create_branding_hook(self):
        """Hook for wallpaper, icons, sounds"""
        hooks_dir = self.config_dir / "hooks" / "live"
        hooks_dir.mkdir(parents=True, exist_ok=True)

        path = hooks_dir / "05-furryos-branding.hook.chroot"
        with open(path, 'w') as f:
            f.write("""#!/bin/sh
# 05-furryos-branding.hook.chroot

echo "Configuring FurryOS branding..."

# Default wallpaper
mkdir -p /usr/share/glib-2.0/schemas
cat > /usr/share/glib-2.0/schemas/20-furryos.gschema.override << 'EOF'
[org.mate.background]
picture-filename='/usr/share/backgrounds/furryos/wallpaper.png'
picture-options='zoom'
primary-color='#000000'

[org.mate.interface]
icon-theme='mate'
gtk-theme='Menta'

[org.mate.sound]
event-sounds=true
EOF

glib-compile-schemas /usr/share/glib-2.0/schemas/ 2>/dev/null || true

# LightDM wallpaper
mkdir -p /etc/lightdm/lightdm-gtk-greeter.conf.d
cat > /etc/lightdm/lightdm-gtk-greeter.conf.d/90-furryos.conf << 'EOF'
[greeter]
background=/usr/share/backgrounds/furryos/wallpaper.png
theme-name=Menta
icon-theme-name=mate
EOF

# Startup sound
if [ -f "/usr/share/sounds/furryos/startup.mp3" ]; then
    mkdir -p /usr/share/sounds/furryos/stereo
    ln -sf /usr/share/sounds/furryos/startup.mp3 /usr/share/sounds/furryos/stereo/desktop-login.oga 2>/dev/null || true
fi

# Plymouth splash
if [ -f "/usr/share/plymouth/themes/furryos/background.png" ]; then
    cat > /usr/share/plymouth/themes/furryos/furryos.plymouth << 'EOF'
[Plymouth Theme]
Name=FurryOS
Description=FurryOS Boot Splash
ModuleName=script

[script]
ImageDir=/usr/share/plymouth/themes/furryos
ScriptFile=/usr/share/plymouth/themes/furryos/furryos.script
EOF

    cat > /usr/share/plymouth/themes/furryos/furryos.script << 'EOF'
background = Image("background.png");
sprite = Sprite(background);
sprite.SetPosition(0, 0, -100);
EOF

    plymouth-set-default-theme furryos 2>/dev/null || true
fi

# File manager bookmarks
mkdir -p /etc/skel/.config/gtk-3.0
cat > /etc/skel/.config/gtk-3.0/bookmarks << 'EOF'
file:///usr/share/backgrounds/furryos FurryOS Wallpapers
file:///usr/share/furryos/lore FurryOS Lore
EOF

echo "✓ FurryOS branding configured"
""")
        os.chmod(path, 0o755)
        print("✅ 05-furryos-branding.hook.chroot")

    def create_music_hook(self):
        """Hook for VLC and music setup"""
        hooks_dir = self.config_dir / "hooks" / "live"
        path = hooks_dir / "06-furryos-music.hook.chroot"

        with open(path, 'w') as f:
            f.write("""#!/bin/sh
# 06-furryos-music.hook.chroot

echo "Configuring music player..."

# VLC defaults
mkdir -p /etc/skel/.local/share/applications
cat > /etc/skel/.local/share/applications/mimeapps.list << 'EOF'
[Default Applications]
audio/mpeg=vlc.desktop
audio/mp3=vlc.desktop
audio/ogg=vlc.desktop
audio/flac=vlc.desktop
EOF

# Desktop shortcut
cat > /etc/skel/Desktop/FurryOS_Music.desktop << 'EOF'
[Desktop Entry]
Type=Application
Name=FurryOS Music
Comment=150 Exclusive Tracks
Exec=vlc ~/Music/FurryOS_Soundtrack
Icon=vlc
Terminal=false
Categories=AudioVideo;
EOF

chmod +x /etc/skel/Desktop/FurryOS_Music.desktop

# Welcome doc
cat > /etc/skel/WELCOME_TO_FURRYOS.txt << 'EOF'
═══════════════════════════════════════════════════════════
  🦊 FURRYOS v8.1.0 - SOVEREIGN UNIVERSE 🦊
═══════════════════════════════════════════════════════════

"I designed the OS, and AI wrote the code."

📁 YOUR CONTENT
• Music/FurryOS_Soundtrack/ - 150 exclusive tracks
• Documents/FurryOS_Lore/ - Story and lore
• Custom wallpapers & icons

🎵 MUSIC
VLC is your default player. Click "FurryOS Music" on desktop!

🔐 CREDENTIALS
Username: anthro / Password: anthro
Root: root / Password: root

Visit: furry-os.com | anthroheart.com

Enjoy your experience!
═══════════════════════════════════════════════════════════
EOF

echo "✓ Music player configured"
""")
        os.chmod(path, 0o755)
        print("✅ 06-furryos-music.hook.chroot")

    def generate_all(self):
        """Generate everything"""
        print("=" * 80)
        print("FURRYOS COMPLETE ASSET INTEGRATION")
        print("=" * 80)
        print()

        self.create_filename_fixer()
        self.create_enhanced_build()
        self.create_branding_hook()
        self.create_music_hook()

        print()
        print("=" * 80)
        print("COMPLETE!")
        print("=" * 80)
        print()
        print("Asset Locations:")
        print("  • assets/sounds/ → startup.mp3 + 150 MP3s")
        print("  • assets/wallpapers/ → wallpaper.png (default)")
        print("  • assets/icons/ → custom icons")
        print("  • assets/splash/ → background.png")
        print("  • assets/lore/ → story documents")
        print()
        print("Build Instructions:")
        print("  1. ./fix_asset_filenames.sh")
        print("  2. sudo lb clean --purge")
        print("  3. sudo rm -rf .build/ chroot/ binary/ cache/")
        print("  4. sudo ./build3.sh")
        print()
        print("ISO Output: ../FurryOS-Builds/")
        print()

if __name__ == "__main__":
    builder = CompleteFurryOSBuilder()
    builder.generate_all()

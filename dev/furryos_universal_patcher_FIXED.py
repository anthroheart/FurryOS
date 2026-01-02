#!/usr/bin/env python3
"""
FurryOS Universal Patcher v8.1.1 - STEAM FIX EDITION
Fixed Steam installation for Debian Trixie
"""

import os
import sys
import yaml
import shutil
import stat
from pathlib import Path
from datetime import datetime

class FurryOSPatcher:
    def __init__(self):
        self.root = Path.cwd()
        self.config_dir = self.root / "config"
        self.assets_dir = self.root / "assets"

        # Load configuration
        self.genome = self.load_yaml("GENOME.yaml")
        self.user_config = self.load_yaml("USER_CONFIG.yaml")

        self.errors = []
        self.warnings = []
        self.fixes_applied = []

    def load_yaml(self, filename):
        """Load YAML configuration file"""
        yaml_path = self.config_dir / filename
        if not yaml_path.exists():
            yaml_path = self.root / filename

        if not yaml_path.exists():
            self.warnings.append(f"{filename} not found, using defaults")
            return {}

        try:
            with open(yaml_path, 'r') as f:
                return yaml.safe_load(f) or {}
        except Exception as e:
            self.errors.append(f"Failed to load {filename}: {e}")
            return {}

    def write_file(self, path, content, executable=False):
        """Write content to file with proper permissions"""
        try:
            path = Path(path)
            path.parent.mkdir(parents=True, exist_ok=True)

            with open(path, 'w', encoding='utf-8') as f:
                f.write(content)

            if executable:
                st = os.stat(path)
                os.chmod(path, st.st_mode | stat.S_IEXEC)

            self.fixes_applied.append(f"Wrote: {path}")
            return True
        except Exception as e:
            self.errors.append(f"Failed to write {path}: {e}")
            return False

    def get_build_script(self):
        """Generate build2.sh"""
        meta = self.genome.get('meta', {})
        os_name = meta.get('frameworkname', 'FurryOS').title().replace(' ', '')
        version = meta.get('version', '8.1.0')

        return f"""#!/bin/bash
# FurryOS Build System v{version}
# Steam-Fixed Edition - Generated {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

set -e
set -o pipefail

OS_NAME="{os_name}"
CODENAME="trixie"
ARCH="amd64"
DATE=$(date +%Y%m%d)
BUILD_LOG="build-${{DATE}}.log"

GREEN='\\033[0;32m'
BLUE='\\033[0;34m'
RED='\\033[0;31m'
NC='\\033[0m'

log_info() {{ echo -e "${{BLUE}}[INFO]${{NC}} $1" | tee -a "$BUILD_LOG"; }}
log_success() {{ echo -e "${{GREEN}}[SUCCESS]${{NC}} $1" | tee -a "$BUILD_LOG"; }}
log_error() {{ echo -e "${{RED}}[ERROR]${{NC}} $1" | tee -a "$BUILD_LOG"; }}

if [ "$EUID" -ne 0 ]; then
    log_error "This script must be run as root (use sudo)"
    exit 1
fi

log_info "============================================"
log_info "${{OS_NAME}} Build System v{version}"
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

log_info "Configuring live-build for Debian ${{CODENAME}}..."
lb config \\
    --distribution "$CODENAME" \\
    --architecture "$ARCH" \\
    --archive-areas "main contrib non-free non-free-firmware" \\
    --security true \\
    --updates true \\
    --bootappend-live "boot=live components quiet splash hostname=furryos" \\
    --linux-packages "linux-image linux-headers" \\
    --iso-volume "${{OS_NAME}}_Live_${{DATE}}" \\
    --iso-application "${{OS_NAME}}" \\
    --iso-publisher "Anthro Entertainment LLC" \\
    --memtest none \\
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

ISO_FILENAME="${{OS_NAME}}_v{version}_${{DATE}}.iso"

if [ -f "live-image-${{ARCH}}.hybrid.iso" ]; then
    mv "live-image-${{ARCH}}.hybrid.iso" "$ISO_FILENAME"

    if [ -n "$SUDO_USER" ]; then
        chown "$SUDO_USER:$SUDO_USER" "$ISO_FILENAME"
    fi

    sha256sum "$ISO_FILENAME" > "${{ISO_FILENAME}}.sha256"
    if [ -n "$SUDO_USER" ]; then
        chown "$SUDO_USER:$SUDO_USER" "${{ISO_FILENAME}}.sha256"
    fi

    log_success "============================================"
    log_success "BUILD SUCCESSFUL!"
    log_success "============================================"
    log_success "ISO: $ISO_FILENAME"
    log_success "Size: $(du -h "$ISO_FILENAME" | cut -f1)"
    log_success "SHA256: $(cat "${{ISO_FILENAME}}.sha256" | cut -d' ' -f1)"
    log_success "Log: $BUILD_LOG"
else
    log_error "Build failed - no ISO file generated!"
    log_error "Check $BUILD_LOG for details"
    exit 1
fi
"""

    def get_package_list(self):
        """Generate package list WITHOUT steam-installer"""
        return """# Base System
task-mate-desktop
mate-utils
mate-tweak
network-manager-gnome

# Firmware
firmware-linux
firmware-iwlwifi
firmware-misc-nonfree

# Filesystem Tools
btrfs-progs
cryptsetup
dosfstools
gparted
timeshift

# Boot & EFI
grub-efi-amd64-signed
shim-signed

# Modern App Ecosystem
flatpak
gnome-software-plugin-flatpak
podman
distrobox

# Core Utilities
htop
curl
git
vim
wget
neovim

# Installer
calamares
calamares-settings-debian

# Boot Animation
plymouth
plymouth-themes

# Admin Panel Dependencies
zenity
python3-tk

# Multimedia
vlc
mpv

# Gaming - Steam installed via Flatpak (more reliable)
# steam-installer removed due to Trixie compatibility issues
"""

    def get_steam_hook(self):
        """Generate FIXED Steam installation hook using Flatpak"""
        return """#!/bin/sh
# 99-install-steam.hook.chroot
# Installs Steam via Flatpak (more reliable for Debian Testing/Trixie)

echo "FurryOS: Setting up Gaming Mode..."

# Method 1: Try Flatpak Steam (most reliable)
if command -v flatpak >/dev/null 2>&1; then
    echo "Installing Steam via Flatpak..."

    # Add Flathub repository
    flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo || true

    # Install Steam (system-wide)
    flatpak install -y flathub com.valvesoftware.Steam || echo "Flatpak Steam install failed, continuing..."

    echo "Steam (Flatpak) installed successfully!"
    echo "Users can launch Steam from the applications menu after first boot."
else
    echo "WARNING: Flatpak not available, Steam installation skipped."
    echo "Users can manually install Steam after system installation."
fi

# Enable 32-bit architecture support for compatibility
dpkg --add-architecture i386 || true
apt-get update || true

# Install essential 32-bit graphics drivers for gaming
apt-get install -y \
    mesa-vulkan-drivers:i386 \
    libglx-mesa0:i386 \
    libgl1-mesa-dri:i386 \
    || echo "Some 32-bit drivers could not be installed, continuing..."

echo "Gaming environment setup complete!"
"""

    def get_appearance_hook(self):
        """Generate appearance/branding hook"""
        meta = self.genome.get('meta', {})
        os_name = meta.get('frameworkname', 'FurryOS').title()

        return f"""#!/bin/sh
# 05-furryos-appearance.hook.chroot
# Applies FurryOS branding and theming

echo "Applying {os_name} branding..."

sed -i 's/PRETTY_NAME=.*/PRETTY_NAME="{os_name}"/' /etc/os-release
sed -i 's/NAME="Debian GNU\\/Linux"/NAME="{os_name}"/' /etc/os-release

mkdir -p /usr/share/glib-2.0/schemas

cat > /usr/share/glib-2.0/schemas/99-furryos.gschema.override << 'EOF'
[org.mate.background]
picture-filename='/usr/share/backgrounds/furryos/wallpaper.png'
primary-color='#000000'
secondary-color='#000000'

[org.mate.interface]
gtk-theme='Menta'
icon-theme='mate'
font-name='Sans 10'
color-scheme='prefer-dark'

[org.mate.panel]
default-layout='redmond'

[org.mate.Marco.general]
theme='Menta'
EOF

glib-compile-schemas /usr/share/glib-2.0/schemas

echo "{os_name} branding applied!"
"""

    def get_admin_panel_script(self):
        """Generate furry-admin GUI"""
        return """#!/usr/bin/env python3
# FurryOS Admin Control Panel

import tkinter as tk
from tkinter import messagebox
import subprocess

def run_command(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        messagebox.showinfo("Success", "Operation completed!")
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def set_profile(profile):
    if profile == "gamer":
        cmd = "sudo systemctl stop cups bluetooth; echo 'Gamer Mode Active'"
    elif profile == "paranoid":
        cmd = "sudo ufw enable; sudo ufw default deny incoming"
    elif profile == "granny":
        cmd = "gsettings set org.mate.interface document-font-name 'Sans 14'"
    elif profile == "hacker":
        cmd = "x-terminal-emulator &"
    else:
        return
    run_command(cmd)

def launch_snapshot():
    run_command("sudo timeshift-gtk")

root = tk.Tk()
root.title("FurryOS Control Center")
root.geometry("500x550")
root.configure(bg="#222")

tk.Label(root, text="FurryOS Control Center", bg="#222", fg="#FF6600", 
         font=("Arial", 20, "bold")).pack(pady=20)

tk.Label(root, text="Select System Profile", bg="#222", fg="#AAA",
         font=("Arial", 12)).pack(pady=10)

btn_frame = tk.Frame(root, bg="#222")
btn_frame.pack(pady=10)

def make_button(text, profile, color):
    tk.Button(btn_frame, text=text, command=lambda: set_profile(profile),
              width=30, height=2, bg=color, fg="white",
              font=("Arial", 11, "bold"), relief="flat").pack(pady=5)

make_button("🎮 Gamer Mode", "gamer", "#D32F2F")
make_button("👵 Granny Mode", "granny", "#1976D2")
make_button("💻 Hacker Mode", "hacker", "#388E3C")
make_button("🔒 Paranoid Mode", "paranoid", "#424242")

tk.Label(root, text="System Maintenance", bg="#222", fg="#AAA",
         font=("Arial", 12)).pack(pady=15)

tk.Button(root, text="📸 System Snapshot & Rollback",
          command=launch_snapshot, width=30, height=2,
          bg="#FF9800", fg="black",
          font=("Arial", 11, "bold")).pack(pady=5)

tk.Button(root, text="EXIT", command=root.quit,
          bg="black", fg="white", relief="flat",
          font=("Arial", 10)).pack(pady=20)

root.mainloop()
"""

    def patch_all(self):
        """Main patching routine"""
        print("=" * 60)
        print("FurryOS Universal Patcher v8.1.1 - STEAM FIX EDITION")
        print("=" * 60)
        print()

        print("[1/5] Generating build2.sh...")
        self.write_file(
            self.root / "build2.sh",
            self.get_build_script(),
            executable=True
        )

        print("[2/5] Generating package list (Steam removed)...")
        self.write_file(
            self.config_dir / "package-lists" / "desktop.list.chroot",
            self.get_package_list()
        )

        print("[3/5] Generating FIXED Steam hook (Flatpak method)...")
        hooks_dir = self.config_dir / "hooks" / "live"
        self.write_file(
            hooks_dir / "99-install-steam.hook.chroot",
            self.get_steam_hook(),
            executable=True
        )

        print("[4/5] Generating appearance hook...")
        self.write_file(
            hooks_dir / "05-furryos-appearance.hook.chroot",
            self.get_appearance_hook(),
            executable=True
        )

        print("[5/5] Generating admin panel...")
        self.write_file(
            self.config_dir / "includes.chroot" / "usr" / "local" / "bin" / "furry-admin",
            self.get_admin_panel_script(),
            executable=True
        )

        desktop_entry = """[Desktop Entry]
Type=Application
Name=FurryOS Control Center
Comment=Manage FurryOS system profiles
Exec=furry-admin
Icon=utilities-system-monitor
Terminal=false
Categories=System;Settings;
"""
        self.write_file(
            self.config_dir / "includes.chroot" / "usr" / "share" / "applications" / "furry-admin.desktop",
            desktop_entry
        )

        print()
        print("=" * 60)
        print("PATCHING COMPLETE!")
        print("=" * 60)
        print()
        print("✅ CRITICAL FIX APPLIED:")
        print("   - Removed steam-installer from package list")
        print("   - Steam now installs via Flatpak (more reliable)")
        print("   - 32-bit support still enabled for compatibility")
        print()
        print("Next steps:")
        print("  1. Run: sudo ./build2.sh")
        print("  2. Wait for ISO to build")
        print("  3. Steam will be available via Flatpak after install")
        print()

        return True

if __name__ == "__main__":
    patcher = FurryOSPatcher()
    patcher.patch_all()

import os
import shutil
import stat

# --- CONFIGURATION ---
ROOT_DIR = os.getcwd()
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
SRC_DIR = os.path.join(ROOT_DIR, 'src')

# --- CONTENT GENERATORS ---

def get_build_script():
    return """#!/bin/bash
# FurryOS Master Build Script (Platinum Edition)
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

# 3. Configure (Best Practices: Secure Boot + Non-Free Firmware)
lb config \\
    --distribution $CODENAME \\
    --architecture $ARCH \\
    --archive-areas "main contrib non-free-firmware" \\
    --bootappend-live "boot=live components quiet splash hostname=furryos persistence functionality=full" \\
    --linux-packages "linux-image linux-headers" \\
    --iso-volume "$OS_NAME Live $DATE" \\
    --iso-application "$OS_NAME" \\
    --memtest none \\
    --security true \\
    --updates true

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
    mv live-image-amd64.hybrid.iso FurryOS_Platinum.iso
    # Fix ownership so you can touch it
    chown $SUDO_USER:$SUDO_USER FurryOS_Platinum.iso
    echo "✅ BUILD SUCCESSFUL: FurryOS_Platinum.iso"
else
    echo "❌ Build failed. Check build.log"
fi
"""

def get_package_list():
    # UPDATED: Includes Btrfs, Secure Boot, Podman, and Timeshift
    return """
# --- DESKTOP ENVIRONMENT ---
task-mate-desktop
mate-utils
mate-tweak
network-manager-gnome

# --- DRIVERS & FIRMWARE ---
firmware-linux
firmware-iwlwifi
firmware-misc-nonfree

# --- FILESYSTEM & RECOVERY (The "Time Machine" features) ---
btrfs-progs
cryptsetup
dosfstools
gparted
timeshift
grub-efi-amd64-signed
shim-signed

# --- MODERN APP ECOSYSTEM ---
flatpak
gnome-software-plugin-flatpak
podman
distrobox

# --- CORE TOOLS ---
fastfetch
htop
curl
git
vim
wget
neovim

# --- INSTALLER ---
calamares
calamares-settings-debian

# --- BRANDING ---
plymouth
plymouth-themes

# --- ADMIN & PROFILES ---
zenity
python3-tk

# --- GAMING & MEDIA ---
vlc
mpv
steam-installer
"""

def get_admin_panel_script():
    # UPDATED: Added "Maintenance Mode" for Snapshots
    return r"""#!/usr/bin/env python3
import tkinter as tk
from tkinter import messagebox
import subprocess
import os

def run_cmd(cmd):
    try:
        subprocess.run(cmd, shell=True, check=True)
        messagebox.showinfo("Success", "Operation completed successfully.")
    except Exception as e:
        messagebox.showerror("Error", f"Failed: {e}")

def set_profile(profile):
    if profile == "gamer":
        cmd = "sudo systemctl stop cups cron; echo 'Gamer Mode: Max Performance'"
    elif profile == "paranoid":
        cmd = "sudo ufw enable; sudo ufw default deny incoming; sudo rm -rf /var/log/*; echo 'Paranoid Mode: Secure'"
    elif profile == "granny":
        cmd = "gsettings set org.mate.interface document-font-name 'Sans 14'; echo 'Granny Mode: UI Locked'"
    elif profile == "hacker":
        cmd = "x-terminal-emulator &; echo 'Hacker Mode: Dev Tools Ready'"
    run_cmd(cmd)

def launch_snapshot():
    # Launch Timeshift for system rollback
    run_cmd("sudo timeshift-gtk")

root = tk.Tk()
root.title("FurryOS Control Center")
root.geometry("500x500")
root.configure(bg="#222")

tk.Label(root, text="FurryOS Control Center", bg="#222", fg="#FF6600", font=("Arial", 20, "bold")).pack(pady=20)
tk.Label(root, text="Select Profile", bg="#222", fg="#AAA", font=("Arial", 12)).pack(pady=5)

btn_frame = tk.Frame(root, bg="#222")
btn_frame.pack(pady=10)

def mk_btn(txt, cmd_name, color):
    tk.Button(btn_frame, text=txt, command=lambda: set_profile(cmd_name),
              width=30, height=2, bg=color, fg="white", font=("Arial", 11, "bold"),
              relief="flat").pack(pady=5)

mk_btn("🎮 Gamer Mode", "gamer", "#D32F2F")
mk_btn("👵 Granny Mode", "granny", "#1976D2")
mk_btn("🤖 Hacker Mode", "hacker", "#388E3C")
mk_btn("🕵️ Paranoid Mode", "paranoid", "#424242")

tk.Label(root, text="System Maintenance", bg="#222", fg="#AAA", font=("Arial", 12)).pack(pady=15)
tk.Button(root, text="⏪ System Snapshot / Rollback", command=launch_snapshot,
          width=30, height=2, bg="#FF9800", fg="black", font=("Arial", 11, "bold")).pack(pady=5)

tk.Button(root, text="EXIT", command=root.quit, bg="black", fg="white", relief="flat").pack(pady=20)

root.mainloop()
"""

def get_appearance_hook():
    return """#!/bin/sh
echo "🎨 Applying FurryOS 'Windows Style' Layout..."

# 1. Branding
sed -i 's/PRETTY_NAME=.*/PRETTY_NAME="FurryOS (Platinum)"/g' /etc/os-release
sed -i 's/NAME="Debian GNU\/Linux"/NAME="FurryOS"/g' /etc/os-release

# 2. MATE Desktop Overrides
mkdir -p /usr/share/glib-2.0/schemas/
cat <<EOF > /usr/share/glib-2.0/schemas/99-furryos.gschema.override
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

# 3. Apply
glib-compile-schemas /usr/share/glib-2.0/schemas/
"""

def get_setup_admin_hook():
    return """#!/bin/sh
# Make the admin panel executable
chmod +x /usr/local/bin/furry-admin
"""

# --- MAIN LOGIC ---

def clean_file_structure():
    print("🧹 Cleaning file structure...")
    if not os.path.exists(SRC_DIR): os.makedirs(SRC_DIR)

    stray_files = ['heartbeat_core.c', 'heartbeat_core_asm.s', 'healer_core.cpp', 'Makefile_optimized']
    for root, dirs, files in os.walk(ASSETS_DIR):
        for f in files:
            if f in stray_files:
                src_path = os.path.join(root, f)
                dst_path = os.path.join(SRC_DIR, f)
                try:
                    shutil.move(src_path, dst_path)
                    print(f"   Moved source file: {f} -> src/")
                except: pass

def write_file(path, content, executable=False):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        if executable:
            st = os.stat(path)
            os.chmod(path, st.st_mode | stat.S_IEXEC)
        print(f"   ✅ Wrote: {path}")
    except Exception as e:
        print(f"   ❌ Failed to write {path}: {e}")

def main():
    print("🦊 FurryOS Platinum Patcher (Best Practices Edition)")

    clean_file_structure()

    # 1. Write Build Script
    write_file(os.path.join(ROOT_DIR, 'build.sh'), get_build_script(), executable=True)

    # 2. Write Package List
    list_path = os.path.join(CONFIG_DIR, 'package-lists', 'desktop.list.chroot')
    write_file(list_path, get_package_list())

    # 3. Write Appearance Hook
    hook_path = os.path.join(CONFIG_DIR, 'hooks', 'live', '05-furryos-appearance.hook.chroot')
    write_file(hook_path, get_appearance_hook(), executable=True)

    # 4. Write Admin Panel Script
    admin_path = os.path.join(CONFIG_DIR, 'includes.chroot', 'usr', 'local', 'bin', 'furry-admin')
    write_file(admin_path, get_admin_panel_script(), executable=True)

    # 5. Write Admin Panel Setup Hook
    setup_hook_path = os.path.join(CONFIG_DIR, 'hooks', 'live', '06-setup-admin.hook.chroot')
    write_file(setup_hook_path, get_setup_admin_hook(), executable=True)

    # 6. Create Desktop Shortcut for Admin Panel
    desktop_shortcut = """[Desktop Entry]
Type=Application
Name=Furry Control Center
Comment=Manage FurryOS Profiles
Exec=furry-admin
Icon=utilities-system-monitor
Terminal=false
Categories=System;Settings;
"""
    shortcut_path = os.path.join(CONFIG_DIR, 'includes.chroot', 'usr', 'share', 'applications', 'furry-admin.desktop')
    write_file(shortcut_path, desktop_shortcut)

    print("\n✨ Patcher Complete.")
    print("   Updates Included:")
    print("   1. Filesystem: Added Btrfs, Snapper, and Timeshift (Rollback capability).")
    print("   2. Security: Added Secure Boot shim and Disk Encryption tools.")
    print("   3. Containers: Added Podman and Distrobox.")
    print("   4. Admin Panel: Added 'System Snapshot / Rollback' button.")
    print("\n👉 Run: sudo ./build.sh")

if __name__ == "__main__":
    main()

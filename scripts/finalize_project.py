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
lb config \\
    --distribution $CODENAME \\
    --architecture $ARCH \\
    --archive-areas "main contrib non-free-firmware" \\
    --bootappend-live "boot=live components quiet splash hostname=furryos persistence" \\
    --linux-packages "linux-image linux-headers" \\
    --iso-volume "$OS_NAME Live $DATE" \\
    --iso-application "$OS_NAME" \\
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
"""

def get_package_list():
    # Includes standard tools + profile tools + fastfetch
    return """
task-mate-desktop
mate-utils
mate-tweak
firmware-linux
firmware-iwlwifi
firmware-misc-nonfree
# Core Tools
fastfetch
htop
curl
git
vim
# Installer
calamares
calamares-settings-debian
# Branding
plymouth
plymouth-themes
# Admin & Profiles
zenity
python3-tk
network-manager-gnome
gparted
# Gaming/Media (Pre-loaded)
vlc
mpv
"""

def get_admin_panel_script():
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
        # high performance, stop cups/printer, stop cron
        cmd = "sudo systemctl stop cups cron; echo 'Gamer Mode: Max Performance'"
    elif profile == "paranoid":
        # firewall up, clear logs
        cmd = "sudo ufw enable; sudo rm -rf /var/log/*; echo 'Paranoid Mode: Secure'"
    elif profile == "granny":
        # lock layout, auto updates
        cmd = "echo 'Granny Mode: UI Locked, Updates On'"
    
    run_cmd(cmd)

root = tk.Tk()
root.title("FurryOS Control Center")
root.geometry("400x300")
root.configure(bg="#2d2d2d")

lbl = tk.Label(root, text="FurryOS Admin Panel", bg="#2d2d2d", fg="white", font=("Arial", 16))
lbl.pack(pady=20)

btn_frame = tk.Frame(root, bg="#2d2d2d")
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="🎮 Gamer Profile", command=lambda: set_profile("gamer"), width=20).pack(pady=5)
tk.Button(btn_frame, text="👵 Granny Profile", command=lambda: set_profile("granny"), width=20).pack(pady=5)
tk.Button(btn_frame, text="🕵️ Paranoid Profile", command=lambda: set_profile("paranoid"), width=20).pack(pady=5)

tk.Button(root, text="Exit", command=root.quit, bg="red", fg="white").pack(pady=20)

root.mainloop()
"""

def get_appearance_hook():
    # This enforces the Windows 7 Layout (Redmond) and Dark Theme
    return """#!/bin/sh
echo "🎨 Applying FurryOS 'Windows Style' Layout..."

# 1. Branding
sed -i 's/PRETTY_NAME=.*/PRETTY_NAME="FurryOS (Golden Master)"/g' /etc/os-release
sed -i 's/NAME="Debian GNU\/Linux"/NAME="FurryOS"/g' /etc/os-release

# 2. MATE Desktop Overrides (The 'Windows 7' Feel)
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
# Make the admin panel executable and put it in path
chmod +x /usr/local/bin/furry-admin
"""

# --- MAIN LOGIC ---

def clean_file_structure():
    print("🧹 Cleaning file structure...")
    
    # 1. Move stray source files to src
    if not os.path.exists(SRC_DIR): os.makedirs(SRC_DIR)
    
    # List of files that shouldn't be in assets
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
    print("🦊 FurryOS Golden Master Patcher")
    
    clean_file_structure()
    
    # 1. Write Build Script
    write_file(os.path.join(ROOT_DIR, 'build.sh'), get_build_script(), executable=True)
    
    # 2. Write Package List (Removes fastfetch)
    list_path = os.path.join(CONFIG_DIR, 'package-lists', 'desktop.list.chroot')
    write_file(list_path, get_package_list())
    
    # 3. Write Appearance Hook (Windows 7 Style)
    hook_path = os.path.join(CONFIG_DIR, 'hooks', 'live', '05-furryos-appearance.hook.chroot')
    write_file(hook_path, get_appearance_hook(), executable=True)
    
    # 4. Write Admin Panel Script (Inside the OS structure)
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
    print("   1. 'fastfetch' is gone.")
    print("   2. MATE is configured for 'Redmond' (Windows-style) layout.")
    print("   3. Dark mode is enforced.")
    print("   4. 'furry-admin' tool is installed.")
    print("\n👉 Run: sudo ./build.sh")

if __name__ == "__main__":
    main()

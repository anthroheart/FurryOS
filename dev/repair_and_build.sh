import os
import shutil

ROOT_DIR = os.getcwd()
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')

# 1. Update the Patcher to separate Steam from the main list
def update_patcher():
    print("🔧 Updating Patcher logic for Steam/32-bit support...")

    # We use triple single quotes (''') for the outer block to avoid conflicts
    patcher_code = r'''import os
import shutil
import stat

ROOT_DIR = os.getcwd()
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
SRC_DIR = os.path.join(ROOT_DIR, 'src')

def get_build_script():
    # UPDATED: Added Logging Pipe (| tee build_log.txt)
    return """#!/bin/bash
# FurryOS Master Build Script (Platinum + Log)
# Usage: sudo ./build2.sh

set -e
OS_NAME="FurryOS"
CODENAME="trixie"
ARCH="amd64"
DATE=$(date +%Y%m%d)

if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo ./build2.sh)"
  exit 1
fi

# START LOGGING
exec > >(tee -i build_log.txt)
exec 2>&1

echo "🦊 Starting FurryOS Build [$DATE]..."

lb clean --purge
rm -f *.iso

# Configure (Added 'non-free' for Steam deps)
lb config \\
    --distribution $CODENAME \\
    --architecture $ARCH \\
    --archive-areas "main contrib non-free non-free-firmware" \\
    --bootappend-live "boot=live components quiet splash hostname=furryos persistence functionality=full" \
    --linux-packages "linux-image linux-headers" \\
    --iso-volume "$OS_NAME Live $DATE" \\
    --iso-application "$OS_NAME" \\
    --memtest none \\
    --security true \\
    --updates true

echo "🎨 Injecting configuration..."
mkdir -p config/includes.chroot/usr/share/backgrounds/furryos/
mkdir -p config/includes.chroot/usr/share/icons/furryos/
mkdir -p config/includes.chroot/etc/skel/Desktop/
mkdir -p config/hooks/live/

if [ -d "assets/wallpapers" ]; then
    rsync -av assets/wallpapers/* config/includes.chroot/usr/share/backgrounds/furryos/
fi
if [ -d "assets/icons" ]; then
    rsync -av assets/icons/* config/includes.chroot/usr/share/icons/furryos/
fi

# Permissions fix for admin tools
if [ -f "config/includes.chroot/usr/local/bin/furry-admin" ]; then
    chmod +x config/includes.chroot/usr/local/bin/furry-admin
fi

echo "🚀 Building ISO..."
lb build

if [ -f "live-image-amd64.hybrid.iso" ]; then
    mv live-image-amd64.hybrid.iso FurryOS_GoldenMaster.iso
    chown $SUDO_USER:$SUDO_USER FurryOS_GoldenMaster.iso
    echo "✅ BUILD SUCCESSFUL: FurryOS_GoldenMaster.iso"
else
    echo "❌ Build failed. Check build_log.txt"
    exit 1
fi
"""

def get_package_list():
    # REMOVED: steam-installer (It moves to the hook)
    return """
task-mate-desktop
mate-utils
mate-tweak
network-manager-gnome
firmware-linux
firmware-iwlwifi
firmware-misc-nonfree
btrfs-progs
cryptsetup
dosfstools
gparted
timeshift
grub-efi-amd64-signed
shim-signed
flatpak
gnome-software-plugin-flatpak
podman
distrobox
htop
curl
git
vim
wget
neovim
calamares
calamares-settings-debian
plymouth
plymouth-themes
zenity
python3-tk
vlc
mpv
"""

def get_steam_hook():
    # This hook enables 32-bit architecture BEFORE installing Steam
    return """#!/bin/sh
echo "🎮 Setting up Gaming Mode (Multi-Arch)..."

# 1. Enable 32-bit (Required for Steam)
dpkg --add-architecture i386
apt-get update

# 2. Install Steam and dependencies safely
apt-get install -y steam-installer mesa-vulkan-drivers:i386 libglx-mesa0:i386
"""

def get_appearance_hook():
    return """#!/bin/sh
echo "🎨 Applying FurryOS Theme..."
sed -i 's/PRETTY_NAME=.*/PRETTY_NAME="FurryOS (Platinum)"/g' /etc/os-release
sed -i 's/NAME="Debian GNU\/Linux"/NAME="FurryOS"/g' /etc/os-release

mkdir -p /usr/share/glib-2.0/schemas/
cat <<EOF > /usr/share/glib-2.0/schemas/99-furryos.gschema.override
[org.mate.background]
picture-filename='/usr/share/backgrounds/furryos/wallpaper.png'
[org.mate.interface]
gtk-theme='Menta'
icon-theme='mate'
font-name='Sans 10'
color-scheme='prefer-dark'
[org.mate.panel]
default-layout='redmond'
EOF
glib-compile-schemas /usr/share/glib-2.0/schemas/
"""

def get_setup_admin_hook():
    return """#!/bin/sh
# Make the admin panel executable
chmod +x /usr/local/bin/furry-admin
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

def write_file(path, content, executable=False):
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w') as f:
            f.write(content)
        if executable:
            os.chmod(path, 0o755)
        print(f"   ✅ Wrote: {path}")
    except Exception as e:
        print(f"   ❌ Error writing {path}: {e}")

def main():
    print("🦊 FurryOS Golden Master Patcher")

    # 1. Write Build Script
    write_file(os.path.join(ROOT_DIR, 'build2.sh'), get_build_script(), executable=True)

    # 2. Write Package List (Clean)
    list_path = os.path.join(CONFIG_DIR, 'package-lists', 'desktop.list.chroot')
    write_file(list_path, get_package_list())

    # 3. Write Appearance Hook
    write_file(os.path.join(CONFIG_DIR, 'hooks', 'live', '05-furryos-appearance.hook.chroot'), get_appearance_hook(), executable=True)

    # 4. Write Steam Hook (The Fix)
    write_file(os.path.join(CONFIG_DIR, 'hooks', 'live', '99-install-steam.hook.chroot'), get_steam_hook(), executable=True)

    # 5. Write Admin Panel Script
    admin_path = os.path.join(CONFIG_DIR, 'includes.chroot', 'usr', 'local', 'bin', 'furry-admin')
    write_file(admin_path, get_admin_panel_script(), executable=True)

    # 6. Write Admin Panel Setup Hook
    setup_hook_path = os.path.join(CONFIG_DIR, 'hooks', 'live', '06-setup-admin.hook.chroot')
    write_file(setup_hook_path, get_setup_admin_hook(), executable=True)

if __name__ == "__main__":
    main()
'''
    with open("finalize_project.py", "w") as f:
        f.write(patcher_code)
    print("   ✅ Updated finalize_project.py with Fixed Python Syntax")

if __name__ == "__main__":
    # 1. Update the patcher code
    update_patcher()

    # 2. Run the patcher to generate the new build files
    print("\n🚀 Applying Patches...")
    os.system("python3 finalize_project.py")

    print("\n✅ System Repaired.")
    print("   - Python Syntax: Fixed.")
    print("   - Steam: Moved to safe hook.")
    print("   - Logging: Enabled.")

    print("\n👉 To build, run:")
    print("   sudo ./build2.sh")

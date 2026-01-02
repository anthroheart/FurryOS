import os
import stat

# --- 1. DEFINE THE CONTENT ---

# The Steam Hook (Installs 32-bit libraries safely)
steam_hook_content = r"""#!/bin/sh
echo "🎮 FurryOS: Configuring Gaming Mode..."

# Enable 32-bit architecture
dpkg --add-architecture i386
apt-get update

# Install Steam and 32-bit drivers
apt-get install -y steam-installer mesa-vulkan-drivers:i386 libglx-mesa0:i386
"""

# The Clean Package List (No Steam here to prevent crash)
package_list_content = """
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

# The Master Build Script (Bash)
# We use raw strings and careful quoting to avoid SyntaxErrors
build_script_content = r'''#!/bin/bash
# FurryOS Master Build Script
# Usage: sudo ./build2.sh

set -e
OS_NAME="FurryOS"
CODENAME="trixie"
ARCH="amd64"
DATE=$(date +%Y%m%d)

# 1. Root Check
if [ "$EUID" -ne 0 ]; then
  echo "❌ Please run as root (sudo ./build2.sh)"
  exit 1
fi

# 2. Setup Logging
exec > >(tee -i build_log.txt)
exec 2>&1

echo "🦊 Starting FurryOS Build [$DATE]..."

# 3. Clean
lb clean --purge
rm -f *.iso

# 4. Configure
lb config \
    --distribution $CODENAME \
    --architecture $ARCH \
    --archive-areas "main contrib non-free non-free-firmware" \
    --bootappend-live "boot=live components quiet splash hostname=furryos persistence functionality=full" \
    --linux-packages "linux-image linux-headers" \
    --iso-volume "$OS_NAME Live $DATE" \
    --iso-application "$OS_NAME" \
    --memtest none \
    --security true \
    --updates true

# 5. Inject Assets
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

# Fix permissions for admin tools
if [ -f "config/includes.chroot/usr/local/bin/furry-admin" ]; then
    chmod +x config/includes.chroot/usr/local/bin/furry-admin
fi

# 6. Build
echo "🚀 Building ISO..."
lb build

# 7. Finalize
if [ -f "live-image-amd64.hybrid.iso" ]; then
    mv live-image-amd64.hybrid.iso FurryOS_GoldenMaster.iso

    # Fix ownership if sudo user is detected
    if [ -n "$SUDO_USER" ]; then
        chown $SUDO_USER:$SUDO_USER FurryOS_GoldenMaster.iso
    fi

    echo "✅ BUILD SUCCESSFUL: FurryOS_GoldenMaster.iso"
    echo "📄 Log saved to build_log.txt"
else
    echo "❌ Build failed. Check build_log.txt for details."
    exit 1
fi
'''

# --- 2. APPLY THE FILES ---

def write_file(path, content, is_executable=False):
    # Ensure dir exists
    os.makedirs(os.path.dirname(path), exist_ok=True)

    # Write content
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content.strip())

    # Set permissions
    if is_executable:
        st = os.stat(path)
        os.chmod(path, st.st_mode | stat.S_IEXEC)

    print(f"✅ Wrote: {path}")

def main():
    print("🔧 Writing FurryOS Build System...")

    # 1. Write the package list (Cleaned)
    write_file('config/package-lists/desktop.list.chroot', package_list_content)

    # 2. Write the Steam Hook (The logic fix)
    write_file('config/hooks/live/99-install-steam.hook.chroot', steam_hook_content, is_executable=True)

    # 3. Write the Build Script (The logging fix)
    write_file('build2.sh', build_script_content, is_executable=True)

    print("\n🚀 Ready.")
    print("Run: sudo ./build2.sh")

if __name__ == "__main__":
    main()

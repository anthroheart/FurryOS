#!/bin/bash
set -e

echo "Installing FurryOS desktop launcher..."

mkdir -p /usr/share/furryos/desktop/icons
mkdir -p /usr/share/applications
mkdir -p /etc/skel/Desktop

cp FurryOS-Installer.sh /usr/share/furryos/desktop/
chmod +x /usr/share/furryos/desktop/FurryOS-Installer.sh

cp icons/furryos-installer.png /usr/share/furryos/desktop/icons/
cp icons/furryos-installer.png /usr/share/pixmaps/

cp FurryOS-Installer.desktop /usr/share/applications/
cp FurryOS-Installer.desktop /etc/skel/Desktop/
chmod 755 /etc/skel/Desktop/FurryOS-Installer.desktop

# Copy README to desktop (if exists)
if [ -f README.txt ]; then
    cp README.txt /etc/skel/Desktop/
    chmod 644 /etc/skel/Desktop/README.txt
    echo "  ✓ README copied to desktop"
else
    echo "  ℹ README.txt not found (skipping)"
fi

echo "✓ Desktop launcher installed"


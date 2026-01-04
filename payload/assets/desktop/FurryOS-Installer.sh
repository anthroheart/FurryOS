#!/bin/bash

if [ "$(id -u)" -ne 0 ]; then
    pkexec "$0" "$@"
    exit $?
fi

if grep -q "boot=live" /proc/cmdline; then
    zenity --info --title="FurryOS Installer" \
           --text="Welcome to FurryOS Gen2!\n\nThis will install FurryOS to your hard drive.\n\nClick OK to continue." \
           --width=400
    
    if command -v calamares &> /dev/null; then
        calamares
    elif command -v debian-installer-launcher &> /dev/null; then
        debian-installer-launcher
    else
        mate-terminal -e "sudo debian-installer"
    fi
else
    zenity --warning --title="Already Installed" \
           --text="FurryOS is already installed.\n\nThe installer is only available in Live mode." \
           --width=400
fi


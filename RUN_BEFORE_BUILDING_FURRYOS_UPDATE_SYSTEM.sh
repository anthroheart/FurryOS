#! /bin/bash

# Prevent Plymouth (splash page) problems

sudo apt clean
sudo apt update
sudo apt upgrade -y
sudo apt install -y plymouth plymouth-themes
sudo apt autoremove -y

# Remove previous stuck build folders

sudo rm -rf ./chroot
sudo rm -rf ./furryos_venv
sudo rm -rf ./_generated

# (Optional but recommended) Lock Plymouth packages

sudo apt-mark hold plymouth plymouth-themes

echo "After build run: RUN_AFTER_BUILDING_FURRYOS_UNLOCK_PLYMOUTH.sh"

echo

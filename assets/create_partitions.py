#!/usr/bin/env python3
"""
===============================================================================
FURRYOS SMART USB CREATOR (ROBUST)
===============================================================================
"""
import os
import sys
import subprocess
import time
from pathlib import Path

def run_cmd(cmd, ignore=False):
    try:
        subprocess.run(cmd, shell=True, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    except:
        if not ignore: print(f"Error: {cmd}")

def aggressive_unmount(dev):
    print(f"   🔓 Unmounting {dev}...")
    run_cmd(f"umount -f {dev}*", ignore=True)
    run_cmd(f"swapoff {dev}*", ignore=True)
    time.sleep(1)

def main():
    if os.geteuid() != 0: sys.exit("❌ Run as root")
    print("📀 Available Devices:")
    subprocess.run("lsblk -d -o NAME,SIZE,MODEL", shell=True)
    
    dev = input("\nTarget Device (e.g. sdb): ").strip()
    if not dev.startswith("/dev/"): dev = f"/dev/{dev}"
    
    if input(f"⚠️  ERASE {dev}? [y/N]: ") != "y": sys.exit()
    
    print("🔧 Partitioning...")
    aggressive_unmount(dev)
    run_cmd(f"wipefs -a {dev}")
    run_cmd(f"parted -s {dev} mklabel gpt")
    run_cmd(f"parted -s {dev} mkpart primary 1MiB 2MiB")
    run_cmd(f"parted -s {dev} set 1 bios_grub on")
    run_cmd(f"parted -s {dev} mkpart primary fat32 2MiB 514MiB")
    run_cmd(f"parted -s {dev} set 2 esp on")
    run_cmd(f"parted -s {dev} mkpart primary ext4 514MiB 100%")
    
    run_cmd(f"partprobe {dev}")
    time.sleep(2)
    
    print("💾 Formatting...")
    aggressive_unmount(dev)
    p = "p" if dev[-1].isdigit() else ""
    run_cmd(f"mkfs.vfat -F32 -n FURRY_EFI {dev}{p}2")
    run_cmd(f"mkfs.ext4 -F -L FURRY_ROOT {dev}{p}3")
    
    print("🔥 Installing Bootloader...")
    mnt = "/mnt/furry_install"
    run_cmd(f"mkdir -p {mnt}")
    run_cmd(f"mount {dev}{p}3 {mnt}")
    run_cmd(f"mkdir -p {mnt}/boot/efi")
    run_cmd(f"mount {dev}{p}2 {mnt}/boot/efi")
    
    iso = list(Path("output").glob("furryos-*.iso"))
    if iso:
        print(f"   Extracting {iso[0].name}...")
        subprocess.run(f"xorriso -osirrox on -indev {iso[0]} -extract / {mnt}", shell=True)
    
    try:
        subprocess.run(f"grub-install --target=x86_64-efi --efi-directory={mnt}/boot/efi --boot-directory={mnt}/boot --removable --recheck", shell=True)
        subprocess.run(f"grub-install --target=i386-pc --boot-directory={mnt}/boot --recheck {dev}", shell=True)
    except: pass
    
    run_cmd(f"umount -R {mnt}")
    print("✅ DONE! USB Ready.")

if __name__ == "__main__":
    main()

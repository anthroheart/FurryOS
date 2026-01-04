#!/usr/bin/env bash

set -e

echo "== Preparing ISO workspace =="

PROJECT_ROOT="$(cd "$(dirname "$0")" && pwd)"

GEN_DIR="$PROJECT_ROOT/_generated"

ISO_DIR="$GEN_DIR/iso"
ISO_MOUNT="$GEN_DIR/iso-mount"
ISO_ROOT="$GEN_DIR/iso-root"
WORK_DIR="$GEN_DIR/work"
SQUASHFS_ROOT="$WORK_DIR/squashfs-root"

ISO_FILE="$(ls "$GEN_DIR"/iso/*.iso 2>/dev/null | head -n 1)"

if [[ -z "$ISO_FILE" ]]; then
    echo "ERROR: No Debian ISO found in _generated/iso/"
    exit 1
fi

echo "Using ISO: $ISO_FILE"

# ---- Safety cleanup (idempotent) ----
sudo umount "$ISO_MOUNT" 2>/dev/null || true
rm -rf "$ISO_MOUNT"
rm -rf "$ISO_ROOT"
rm -rf "$WORK_DIR"

mkdir -p "$ISO_MOUNT" "$ISO_ROOT" "$WORK_DIR"

# ---- Mount ISO (read-only) ----
echo "Mounting ISO (read-only)..."
sudo mount -o loop,ro "$ISO_FILE" "$ISO_MOUNT"

# ---- Copy full ISO contents ----
echo "Copying ISO contents..."
rsync -a --delete "$ISO_MOUNT/" "$ISO_ROOT/"

# ---- Unmount ISO ASAP ----
sudo umount "$ISO_MOUNT"
rmdir "$ISO_MOUNT"

# ---- Verify required boot artifacts ----
echo "Verifying boot artifacts..."

if [[ ! -f "$ISO_ROOT/live/vmlinuz" ]]; then
    echo "ERROR: live/vmlinuz not found"
    exit 1
fi

if [[ ! -f "$ISO_ROOT/live/initrd.img" ]]; then
    echo "ERROR: live/initrd.img not found"
    exit 1
fi

if [[ ! -f "$ISO_ROOT/live/filesystem.squashfs" ]]; then
    echo "ERROR: filesystem.squashfs not found"
    exit 1
fi

echo "Kernel: $ISO_ROOT/live/vmlinuz"
echo "Initrd: $ISO_ROOT/live/initrd.img"
echo "Squashfs: $ISO_ROOT/live/filesystem.squashfs"

# ---- Extract squashfs (requires sudo for device nodes) ----
echo "Extracting squashfs..."
mkdir -p "$SQUASHFS_ROOT"
sudo unsquashfs -f -d "$SQUASHFS_ROOT" "$ISO_ROOT/live/filesystem.squashfs"

# ---- Fix ownership so future steps DON'T require sudo ----
echo "Fixing ownership..."
sudo chown -R "$USER":"$USER" "$WORK_DIR"

echo "========================================"
echo "ISO workspace READY"
echo
echo "Artifacts:"
echo "  ISO root: $ISO_ROOT"
echo "  Squashfs root: $SQUASHFS_ROOT"
echo
echo "Next phase: boot customization + installer wiring"
echo "========================================"

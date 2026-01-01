#!/bin/bash
################################################################################
# FurryOS Persistent Data Backup & Restore Script
################################################################################
# This script helps transfer your persistent USB data to a full installation
################################################################################

set -e

VERSION="8.0.0-origin"
SCRIPT_NAME="furryos-migrate.sh"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

banner() {
    echo ""
    echo "================================================================================"
    echo "   🐾 FURRYOS PERSISTENT DATA MIGRATION TOOL 🐾"
    echo "   Transfer your settings from USB to full install"
    echo "   Version: $VERSION"
    echo "================================================================================"
    echo ""
}

check_root() {
    if [ "$EUID" -ne 0 ]; then 
        echo "${RED}❌ Please run as root (use sudo)${NC}"
        exit 1
    fi
}

mode_select() {
    echo "${BLUE}Select mode:${NC}"
    echo "  1) Backup persistent USB data"
    echo "  2) Restore to full installation"
    echo "  3) Auto-migrate (backup + restore in one step)"
    echo ""
    read -p "Enter choice [1-3]: " mode
    echo ""
}

backup_persistent() {
    echo "${GREEN}[BACKUP MODE]${NC}"
    echo ""

    # Detect persistence partition
    PERSIST_PART=$(findmnt -n -o SOURCE /lib/live/mount/persistence 2>/dev/null ||                    findmnt -n -o SOURCE / 2>/dev/null | sed 's/[0-9]*$/3/')

    if [ -z "$PERSIST_PART" ]; then
        echo "${YELLOW}⚠️  Cannot auto-detect persistence partition${NC}"
        read -p "Enter persistence partition (e.g., /dev/sdb3): " PERSIST_PART
    fi

    echo "📀 Persistence partition: $PERSIST_PART"
    echo ""

    # Mount if needed
    if ! mountpoint -q /mnt/persistence 2>/dev/null; then
        echo "📂 Mounting persistence partition..."
        mkdir -p /mnt/persistence
        mount $PERSIST_PART /mnt/persistence
        MOUNTED=1
    fi

    # Backup location
    BACKUP_DIR="/tmp/furryos_backup_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$BACKUP_DIR"

    echo "${GREEN}🔄 Backing up data to: $BACKUP_DIR${NC}"
    echo ""

    # Backup home directory
    if [ -d "/mnt/persistence/home" ]; then
        echo "  📁 Backing up /home..."
        rsync -ah --info=progress2 /mnt/persistence/home/ "$BACKUP_DIR/home/"
    else
        echo "  📁 Backing up /home..."
        rsync -ah --info=progress2 /home/ "$BACKUP_DIR/home/"
    fi

    # Backup important configs
    echo "  ⚙️  Backing up configs..."
    mkdir -p "$BACKUP_DIR/etc"

    # Safe configs to backup
    for config in hostname hosts network/interfaces NetworkManager ssh; do
        if [ -e "/etc/$config" ]; then
            cp -a "/etc/$config" "$BACKUP_DIR/etc/" 2>/dev/null || true
        fi
    done

    # Backup installed packages list
    echo "  📦 Backing up package list..."
    dpkg --get-selections > "$BACKUP_DIR/packages.list"

    # Backup ANTHROHEART playlists and favorites
    if [ -d "/home" ]; then
        echo "  🎨 Backing up ANTHROHEART user data..."
        find /home -type f \( -name "*.m3u" -o -name "*.pls" \) -exec cp --parents {} "$BACKUP_DIR/" \; 2>/dev/null || true
    fi

    # Create tarball
    echo ""
    echo "  📦 Creating backup archive..."
    TARBALL="/tmp/furryos-backup-$(date +%Y%m%d_%H%M%S).tar.gz"
    tar -czf "$TARBALL" -C "$BACKUP_DIR" .

    # Unmount if we mounted it
    if [ "$MOUNTED" = "1" ]; then
        umount /mnt/persistence
    fi

    echo ""
    echo "${GREEN}✅ Backup complete!${NC}"
    echo ""
    echo "📦 Backup archive: $TARBALL"
    echo "📊 Size: $(du -h $TARBALL | cut -f1)"
    echo ""
    echo "💾 Copy this file to:"
    echo "   • External drive"
    echo "   • Cloud storage"
    echo "   • Network location"
    echo ""
    echo "🔄 Then boot your full install and run:"
    echo "   sudo $SCRIPT_NAME"
    echo "   Choose option 2 (Restore)"
    echo ""
}

restore_to_install() {
    echo "${GREEN}[RESTORE MODE]${NC}"
    echo ""

    # Find backup
    echo "🔍 Looking for backup archives..."
    BACKUPS=$(find /tmp /media /mnt -name "furryos-backup-*.tar.gz" 2>/dev/null || true)

    if [ -z "$BACKUPS" ]; then
        echo "${YELLOW}⚠️  No backup archives found${NC}"
        read -p "Enter path to backup archive: " TARBALL
    else
        echo "Found backups:"
        select TARBALL in $BACKUPS "Enter path manually"; do
            if [ "$TARBALL" = "Enter path manually" ]; then
                read -p "Enter path to backup archive: " TARBALL
            fi
            break
        done
    fi

    if [ ! -f "$TARBALL" ]; then
        echo "${RED}❌ Backup file not found: $TARBALL${NC}"
        exit 1
    fi

    echo "📦 Using backup: $TARBALL"
    echo ""

    # Extract to temp
    RESTORE_DIR="/tmp/furryos_restore_$(date +%Y%m%d_%H%M%S)"
    mkdir -p "$RESTORE_DIR"

    echo "📂 Extracting backup..."
    tar -xzf "$TARBALL" -C "$RESTORE_DIR"

    # Restore home directory
    if [ -d "$RESTORE_DIR/home" ]; then
        echo ""
        echo "${GREEN}🏠 Restoring home directory...${NC}"
        rsync -ah --info=progress2 "$RESTORE_DIR/home/" /home/
        echo "  ✓ Home directory restored"
    fi

    # Restore configs (carefully)
    if [ -d "$RESTORE_DIR/etc" ]; then
        echo ""
        echo "${GREEN}⚙️  Restoring configs...${NC}"
        echo "${YELLOW}⚠️  Review these changes carefully!${NC}"

        for config in "$RESTORE_DIR/etc"/*; do
            if [ -e "$config" ]; then
                basename=$(basename "$config")
                echo "  📝 Restore /etc/$basename? [y/N]"
                read -n 1 -r
                echo
                if [[ $REPLY =~ ^[Yy]$ ]]; then
                    cp -a "$config" "/etc/"
                    echo "    ✓ Restored"
                else
                    echo "    ⏭️  Skipped"
                fi
            fi
        done
    fi

    # Restore packages
    if [ -f "$RESTORE_DIR/packages.list" ]; then
        echo ""
        echo "${GREEN}📦 Restore installed packages? [y/N]${NC}"
        read -n 1 -r
        echo
        if [[ $REPLY =~ ^[Yy]$ ]]; then
            echo "  📥 Installing packages (this may take a while)..."
            dpkg --set-selections < "$RESTORE_DIR/packages.list"
            apt-get dselect-upgrade -y
            echo "  ✓ Packages restored"
        else
            echo "  ⏭️  Skipped package restoration"
            echo "  💡 Packages list saved to: $RESTORE_DIR/packages.list"
        fi
    fi

    # Fix permissions
    echo ""
    echo "🔧 Fixing permissions..."
    for homedir in /home/*; do
        if [ -d "$homedir" ]; then
            username=$(basename "$homedir")
            chown -R "$username:$username" "$homedir" 2>/dev/null || true
        fi
    done

    # Cleanup
    rm -rf "$RESTORE_DIR"

    echo ""
    echo "${GREEN}✅ Restore complete!${NC}"
    echo ""
    echo "🎉 Your persistent data has been restored!"
    echo "🔄 Reboot to apply all changes"
    echo ""
}

auto_migrate() {
    echo "${GREEN}[AUTO-MIGRATE MODE]${NC}"
    echo ""
    echo "This will backup persistent data and restore to current system"
    echo "${YELLOW}⚠️  Make sure you're running on your FULL INSTALL${NC}"
    echo ""
    read -p "Continue? [y/N]: " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Yy]$ ]]; then
        exit 0
    fi

    # Backup
    backup_persistent

    # Get the tarball that was just created
    LATEST_BACKUP=$(ls -t /tmp/furryos-backup-*.tar.gz 2>/dev/null | head -1)

    if [ -z "$LATEST_BACKUP" ]; then
        echo "${RED}❌ Backup failed${NC}"
        exit 1
    fi

    echo ""
    echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
    echo ""

    # Restore
    TARBALL="$LATEST_BACKUP"
    restore_to_install
}

main() {
    banner
    check_root
    mode_select

    case $mode in
        1)
            backup_persistent
            ;;
        2)
            restore_to_install
            ;;
        3)
            auto_migrate
            ;;
        *)
            echo "${RED}❌ Invalid choice${NC}"
            exit 1
            ;;
    esac

    echo ""
    echo "🐾 FurryOS Migration Tool - Done! 🌱"
    echo ""
}

main

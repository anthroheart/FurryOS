#!/bin/bash
#═══════════════════════════════════════════════════════════════════════════════
#                  🦊 FurryOS Gen2.1 Asset Installer & Builder
#                          Automated Setup Script
#═══════════════════════════════════════════════════════════════════════════════

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Asset download URL
ASSET_URL="https://furry-os.org/assets/FurryOS_Gen2.1_Payload_Assets.zip"
DOWNLOAD_DIR="$HOME/Downloads"
ASSET_ZIP="$DOWNLOAD_DIR/FurryOS_Gen2.1_Payload_Assets.zip"
FURRYOS_DIR="$HOME/FurryOS"
SOURCECODE_DIR="$FURRYOS_DIR/sourcecode"
PAYLOAD_DIR="$SOURCECODE_DIR/payload/assets"

#═══════════════════════════════════════════════════════════════════════════════
# Print Functions
#═══════════════════════════════════════════════════════════════════════════════

print_header() {
    echo -e "${PURPLE}"
    echo "╔═══════════════════════════════════════════════════════════════════════════════╗"
    echo "║               🦊 FurryOS Gen2.1 - Automated Asset Installer 🦊              ║"
    echo "╚═══════════════════════════════════════════════════════════════════════════════╝"
    echo -e "${NC}"
}

print_step() {
    echo -e "${CYAN}➜ $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ ERROR: $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️  $1${NC}"
}

print_info() {
    echo -e "${BLUE}ℹ️  $1${NC}"
}

#═══════════════════════════════════════════════════════════════════════════════
# Step 1: Download Assets
#═══════════════════════════════════════════════════════════════════════════════

download_assets() {
    print_header
    print_step "Step 1/6: Downloading FurryOS Assets..."
    echo ""

    if [ -f "$ASSET_ZIP" ]; then
        print_warning "Asset ZIP already exists in Downloads folder"
        read -p "   Do you want to re-download? (y/N): " -n 1 -r
        echo
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
            print_info "Using existing asset ZIP"
            return 0
        fi
        rm -f "$ASSET_ZIP"
    fi

    print_info "Downloading from: $ASSET_URL"
    print_info "Saving to: $ASSET_ZIP"
    echo ""

    if command -v wget &> /dev/null; then
        wget -O "$ASSET_ZIP" "$ASSET_URL" || {
            print_error "Download failed with wget"
            return 1
        }
    elif command -v curl &> /dev/null; then
        curl -L -o "$ASSET_ZIP" "$ASSET_URL" || {
            print_error "Download failed with curl"
            return 1
        }
    else
        print_error "Neither wget nor curl found. Please install one of them."
        return 1
    fi

    print_success "Assets downloaded successfully!"
    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# Step 2: Create Folder Structure
#═══════════════════════════════════════════════════════════════════════════════

create_folders() {
    print_step "Step 2/6: Creating FurryOS folder structure..."
    echo ""

    # Create main directories
    mkdir -p "$FURRYOS_DIR"
    mkdir -p "$SOURCECODE_DIR"
    mkdir -p "$PAYLOAD_DIR/wallpapers"
    mkdir -p "$PAYLOAD_DIR/splash"
    mkdir -p "$PAYLOAD_DIR/sounds/startup"
    mkdir -p "$PAYLOAD_DIR/sounds/shutdown"

    print_success "Created: $FURRYOS_DIR/"
    print_success "Created: $SOURCECODE_DIR/"
    print_success "Created: $PAYLOAD_DIR/wallpapers/"
    print_success "Created: $PAYLOAD_DIR/splash/"
    print_success "Created: $PAYLOAD_DIR/sounds/startup/"
    print_success "Created: $PAYLOAD_DIR/sounds/shutdown/"
    echo ""

    # Show folder structure
    print_info "Folder structure created:"
    echo ""
    tree -L 4 "$FURRYOS_DIR" 2>/dev/null || {
        find "$FURRYOS_DIR" -type d | sed 's|[^/]*/|  |g'
    }
    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# Step 3: Extract and Install Assets
#═══════════════════════════════════════════════════════════════════════════════

extract_assets() {
    print_step "Step 3/6: Extracting and installing assets..."
    echo ""

    if [ ! -f "$ASSET_ZIP" ]; then
        print_error "Asset ZIP not found: $ASSET_ZIP"
        return 1
    fi

    # Create temp extraction directory
    TEMP_EXTRACT="$DOWNLOAD_DIR/furryos_assets_temp"
    rm -rf "$TEMP_EXTRACT"
    mkdir -p "$TEMP_EXTRACT"

    print_info "Extracting ZIP to temporary location..."
    unzip -q "$ASSET_ZIP" -d "$TEMP_EXTRACT"

    # Expected structure in ZIP:
    # FurryOS_Gen2.1_Payload_Assets/
    #   ├── wallpapers/default.jpg
    #   ├── splash/splash.png
    #   ├── sounds/startup/startup.ogg
    #   └── sounds/shutdown/shutdown.ogg

    # Find the extracted folder (might have different name)
    EXTRACTED_BASE=$(find "$TEMP_EXTRACT" -maxdepth 1 -type d ! -path "$TEMP_EXTRACT" | head -n 1)

    if [ -z "$EXTRACTED_BASE" ]; then
        print_error "No folder found in extracted ZIP"
        return 1
    fi

    print_info "Installing assets to payload directory..."

    # Copy wallpaper
    if [ -f "$EXTRACTED_BASE/wallpapers/default.jpg" ]; then
        cp "$EXTRACTED_BASE/wallpapers/default.jpg" "$PAYLOAD_DIR/wallpapers/"
        print_success "Installed: wallpapers/default.jpg"
    else
        print_warning "Wallpaper not found in ZIP (looking for wallpapers/default.jpg)"
    fi

    # Copy splash
    if [ -f "$EXTRACTED_BASE/splash/splash.png" ]; then
        cp "$EXTRACTED_BASE/splash/splash.png" "$PAYLOAD_DIR/splash/"
        print_success "Installed: splash/splash.png"
    else
        print_warning "Splash screen not found in ZIP (looking for splash/splash.png)"
    fi

    # Copy startup sound
    if [ -f "$EXTRACTED_BASE/sounds/startup/startup.ogg" ]; then
        cp "$EXTRACTED_BASE/sounds/startup/startup.ogg" "$PAYLOAD_DIR/sounds/startup/"
        print_success "Installed: sounds/startup/startup.ogg"
    else
        print_warning "Startup sound not found in ZIP (looking for sounds/startup/startup.ogg)"
    fi

    # Copy shutdown sound (optional)
    if [ -f "$EXTRACTED_BASE/sounds/shutdown/shutdown.ogg" ]; then
        cp "$EXTRACTED_BASE/sounds/shutdown/shutdown.ogg" "$PAYLOAD_DIR/sounds/shutdown/"
        print_success "Installed: sounds/shutdown/shutdown.ogg"
    else
        print_info "Shutdown sound not included (optional)"
    fi

    # Cleanup temp directory
    rm -rf "$TEMP_EXTRACT"

    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# Step 4: Verify Assets
#═══════════════════════════════════════════════════════════════════════════════

verify_assets() {
    print_step "Step 4/6: Verifying installed assets..."
    echo ""

    VERIFICATION_PASSED=true

    # Check wallpaper
    if [ -f "$PAYLOAD_DIR/wallpapers/default.jpg" ]; then
        SIZE=$(identify -format "%wx%h" "$PAYLOAD_DIR/wallpapers/default.jpg" 2>/dev/null || echo "unknown")
        print_success "Wallpaper: default.jpg ($SIZE)"
    else
        print_error "Missing: wallpapers/default.jpg"
        VERIFICATION_PASSED=false
    fi

    # Check splash
    if [ -f "$PAYLOAD_DIR/splash/splash.png" ]; then
        SIZE=$(identify -format "%wx%h" "$PAYLOAD_DIR/splash/splash.png" 2>/dev/null || echo "unknown")
        print_success "Splash: splash.png ($SIZE)"
    else
        print_error "Missing: splash/splash.png"
        VERIFICATION_PASSED=false
    fi

    # Check startup sound
    if [ -f "$PAYLOAD_DIR/sounds/startup/startup.ogg" ]; then
        DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$PAYLOAD_DIR/sounds/startup/startup.ogg" 2>/dev/null | cut -d. -f1 || echo "unknown")
        print_success "Startup sound: startup.ogg (${DURATION}s)"
    else
        print_error "Missing: sounds/startup/startup.ogg"
        VERIFICATION_PASSED=false
    fi

    # Check shutdown sound (optional)
    if [ -f "$PAYLOAD_DIR/sounds/shutdown/shutdown.ogg" ]; then
        DURATION=$(ffprobe -v error -show_entries format=duration -of default=noprint_wrappers=1:nokey=1 "$PAYLOAD_DIR/sounds/shutdown/shutdown.ogg" 2>/dev/null | cut -d. -f1 || echo "unknown")
        print_success "Shutdown sound: shutdown.ogg (${DURATION}s)"
    else
        print_info "Shutdown sound: not installed (optional)"
    fi

    echo ""

    if [ "$VERIFICATION_PASSED" = false ]; then
        print_error "Some required assets are missing!"
        print_info "Please check your asset ZIP file structure"
        return 1
    fi

    print_success "All required assets verified!"
    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# Step 5: Install Desktop Shortcuts
#═══════════════════════════════════════════════════════════════════════════════

install_desktop_shortcuts() {
    print_step "Step 5/6: Installing desktop shortcuts..."
    echo ""

    DESKTOP_DIR="$HOME/.local/share/applications"
    mkdir -p "$DESKTOP_DIR"

    # Create Mode Switcher desktop file
    cat > "$DESKTOP_DIR/furryos-mode-switcher.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=FurryOS Mode Switcher
Comment=Switch between Granny, Normal, Gamer, Hacker, and Ghost modes
Icon=preferences-desktop-theme
Exec=zenity --list --title="FurryOS Mode Switcher" --text="Select a mode to activate:" --column="Mode" --column="Description" --height=400 --width=600 "👴 Granny Mode" "Large fonts, accessible, beginner-friendly" "🔧 Normal Mode" "Balanced interface for everyday use" "🎮 Gamer Mode" "Gaming optimized with Steam and media tools" "👨‍💻 Hacker Mode" "Development environment for coders and admins" "🕵️ Ghost Mode" "Privacy & security focused with Tor and VPN"
Terminal=false
Categories=System;Settings;
Keywords=mode;theme;switch;furryos;
StartupNotify=true
EOF
    print_success "Created: Mode Switcher"

    # Create Source Folder desktop file
    cat > "$DESKTOP_DIR/furryos-source-folder.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FurryOS Source & Assets
Comment=Open FurryOS source code and asset folders
Icon=folder-custom
Exec=xdg-open $FURRYOS_DIR/sourcecode
Terminal=false
Categories=System;Utility;FileManager;
Keywords=furryos;source;assets;wallpaper;splash;sounds;
StartupNotify=true
EOF
    print_success "Created: Source & Assets Folder"

    # Create Documentation desktop file
    cat > "$DESKTOP_DIR/furryos-documentation.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=FurryOS Documentation
Comment=Read the complete FurryOS guide and documentation
Icon=accessories-text-editor
Exec=xdg-open ~/Desktop/FurryOS_README.pdf
Terminal=false
Categories=Documentation;Education;
Keywords=furryos;documentation;help;guide;readme;
StartupNotify=true
EOF
    print_success "Created: Documentation"

    # Create Package Installer desktop file
    cat > "$DESKTOP_DIR/furryos-install-packages.desktop" << 'EOF'
[Desktop Entry]
Version=1.0
Type=Application
Name=Install Custom Packages
Comment=Install additional software packages
Icon=system-software-install
Exec=x-terminal-emulator -e "bash -c 'echo \"📦 FurryOS Package Installer\"; echo \"\"; echo \"Enter package name to install (or \'q\' to quit):\"; read PKG; if [ \"$PKG\" != \"q\" ]; then sudo apt update && sudo apt install -y $PKG; fi; echo \"\"; echo \"Press Enter to close..\"; read'"
Terminal=false
Categories=System;PackageManager;
Keywords=install;package;apt;software;
StartupNotify=true
EOF
    print_success "Created: Package Installer"

    # Create Asset Installer desktop file
    cat > "$DESKTOP_DIR/furryos-asset-installer.desktop" << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=FurryOS Asset Installer
Comment=Download and install FurryOS custom assets
Icon=emblem-downloads
Exec=x-terminal-emulator -e "$SOURCECODE_DIR/install_furryos_assets.sh"
Terminal=true
Categories=System;Settings;
Keywords=furryos;assets;installer;download;
StartupNotify=true
EOF
    print_success "Created: Asset Installer (this script)"

    # Make all desktop files executable
    chmod +x "$DESKTOP_DIR"/furryos-*.desktop

    echo ""
    print_info "Desktop shortcuts installed to: $DESKTOP_DIR/"
    print_info "They will appear in your Applications menu under 'System' or search for 'FurryOS'"
    echo ""

    # Optionally copy to Desktop
    read -p "   Do you want to copy shortcuts to Desktop for quick access? (Y/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Nn]$ ]]; then
        mkdir -p "$HOME/Desktop"
        cp "$DESKTOP_DIR"/furryos-*.desktop "$HOME/Desktop/"
        chmod +x "$HOME/Desktop"/furryos-*.desktop
        print_success "Desktop shortcuts also copied to ~/Desktop/"
    fi

    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# Step 6: Summary & Next Steps
#═══════════════════════════════════════════════════════════════════════════════

show_summary() {
    print_step "Step 6/6: Installation Summary"
    echo ""

    echo -e "${GREEN}╔═══════════════════════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║                    ✅ FURRYOS ASSETS INSTALLED SUCCESSFULLY! ✅              ║${NC}"
    echo -e "${GREEN}╚═══════════════════════════════════════════════════════════════════════════════╝${NC}"
    echo ""

    print_success "Assets Location:"
    echo "   • Wallpaper:     $PAYLOAD_DIR/wallpapers/default.jpg"
    echo "   • Splash:        $PAYLOAD_DIR/splash/splash.png"
    echo "   • Startup sound: $PAYLOAD_DIR/sounds/startup/startup.ogg"
    echo "   • Shutdown sound: $PAYLOAD_DIR/sounds/shutdown/shutdown.ogg"
    echo ""

    print_success "Desktop Shortcuts Created:"
    echo "   • FurryOS Mode Switcher (switch between 5 modes)"
    echo "   • FurryOS Source & Assets (browse assets folder)"
    echo "   • FurryOS Documentation (read guides)"
    echo "   • Install Custom Packages (add software)"
    echo "   • FurryOS Asset Installer (run this script again)"
    echo ""

    print_info "Next Steps:"
    echo ""
    echo -e "${YELLOW}   1. Copy your build scripts to: $SOURCECODE_DIR/${NC}"
    echo "      • GENOME_Gen2.1_Final.yaml"
    echo "      • build_furryos_gen2.1_enhanced.sh"
    echo "      • FurryOS_Live_Multimedia_Setup_Post_ISO_Gen2.1.sh"
    echo ""
    echo -e "${YELLOW}   2. Make build script executable:${NC}"
    echo "      chmod +x $SOURCECODE_DIR/*.sh"
    echo ""
    echo -e "${YELLOW}   3. Build your custom FurryOS:${NC}"
    echo "      cd $SOURCECODE_DIR"
    echo "      sudo ./build_furryos_gen2.1_enhanced.sh"
    echo ""
    echo -e "${YELLOW}   4. Find your ISO at:${NC}"
    echo "      $SOURCECODE_DIR/_generated/output/furryos-gen2.1-final-amd64.iso"
    echo ""

    print_success "🦊 FurryOS asset installation complete!"
    echo ""
}

#═══════════════════════════════════════════════════════════════════════════════
# Main Installation Flow
#═══════════════════════════════════════════════════════════════════════════════

main() {
    # Check if running as root
    if [ "$EUID" -eq 0 ]; then
        print_error "Do not run this script as root/sudo!"
        print_info "Run as regular user: ./install_furryos_assets.sh"
        exit 1
    fi

    # Run installation steps
    download_assets || exit 1
    create_folders || exit 1
    extract_assets || exit 1
    verify_assets || exit 1
    install_desktop_shortcuts || exit 1
    show_summary

    exit 0
}

# Run main function
main

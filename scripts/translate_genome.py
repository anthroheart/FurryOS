import yaml
import os
import sys

# --- SMART PATH FINDING ---
def find_project_root():
    """Hunts for the root directory by looking for 'build.sh' or 'config'."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk up 3 levels to find the root
    for _ in range(3):
        if os.path.exists(os.path.join(current_dir, 'build.sh')):
            return current_dir
        current_dir = os.path.dirname(current_dir)
    
    # Fallback: assume the script is in /scripts/ and root is one level up
    return os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))

ROOT_DIR = find_project_root()
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
YAML_FILE = os.path.join(CONFIG_DIR, 'GENOME.yaml')

print(f"📍 Project Root detected: {ROOT_DIR}")
print(f"📍 Config File target: {YAML_FILE}")

# --- TEMPLATES ---
ZRAM_HOOK = """#!/bin/sh
echo "🧠 Configuring ZRAM Swap (Genome Spec)..."
apt-get install -y zram-tools
echo "ALGO=zstd" >> /etc/default/zramswap
echo "PERCENT=50" >> /etc/default/zramswap
"""

TLP_HOOK = """#!/bin/sh
echo "🔋 Configuring TLP Power Management..."
apt-get install -y tlp tlp-rdw
systemctl enable tlp
"""

THEME_HOOK = """#!/bin/sh
echo "🎨 Applying FurryOS Branding to MATE..."
mkdir -p /usr/share/glib-2.0/schemas/
cat <<EOF > /usr/share/glib-2.0/schemas/99-furryos-mate.gschema.override
[org.mate.background]
picture-filename='/usr/share/backgrounds/furryos/wallpaper.jpg'

[org.mate.interface]
gtk-theme='Menta'
icon-theme='mate'
font-name='Noto Sans 10'
EOF
glib-compile-schemas /usr/share/glib-2.0/schemas/
"""

# --- MAIN LOGIC ---

def load_yaml():
    if not os.path.exists(YAML_FILE):
        print(f"❌ Error: Could not find GENOME.yaml at {YAML_FILE}")
        print("   Please ensure the file exists in the 'config' folder in your project root.")
        sys.exit(1)
    with open(YAML_FILE, 'r') as f:
        return yaml.safe_load(f)

def generate_packages(data):
    print("📦 Generating Package List from GENOME.yaml...")
    packages = set()

    # 1. Base Essentials
    packages.add("task-mate-desktop")
    packages.add("mate-utils")
    packages.add("plymouth")
    packages.add("plymouth-themes")
    packages.add("calamares")
    packages.add("calamares-settings-debian")
    
    # 2. Hardware/Kernel
    packages.add("linux-image-amd64")
    packages.add("firmware-linux")
    packages.add("firmware-iwlwifi")
    packages.add("firmware-misc-nonfree")

    # 3. Features from YAML
    try:
        # Audio
        if data.get('taxonomy', {}).get('family', {}).get('audio_server') == 'pipewire':
            packages.update(["pipewire", "pipewire-pulse", "wireplumber", "pavucontrol"])

        # Storage
        packages.add("btrfs-progs")
        packages.add("gparted")
        packages.add("dosfstools")

        # Performance
        packages.add("tlp")
        packages.add("zram-tools")

        # Bundles
        bundles = data.get('installer', {}).get('wizard', {}).get('step4_packages', {}).get('bundles', {})
        
        if bundles.get('gaming'):
            packages.update(["steam-installer", "lutris", "gamemode"])
        
        if bundles.get('development'):
            packages.update(["git", "python3", "build-essential"])

        if bundles.get('multimedia'):
            packages.update(["gimp", "obs-studio", "vlc"])

        if bundles.get('office'):
            packages.add("libreoffice")

    except KeyError as e:
        print(f"⚠️  Warning: Missing expected key in YAML: {e}. Skipping some packages.")

    # Write
    pkg_path = os.path.join(CONFIG_DIR, 'package-lists', 'genome_generated.list.chroot')
    if not os.path.exists(os.path.dirname(pkg_path)):
        os.makedirs(os.path.dirname(pkg_path))
        
    with open(pkg_path, 'w') as f:
        f.write("\n".join(sorted(packages)))
    print(f"   ✅ Added {len(packages)} packages to {pkg_path}")

def generate_hooks(data):
    print("🪝 Generating System Hooks...")
    hook_dir = os.path.join(CONFIG_DIR, 'hooks', 'live')
    if not os.path.exists(hook_dir):
        os.makedirs(hook_dir)

    with open(os.path.join(hook_dir, '01-setup-zram.hook.chroot'), 'w') as f: f.write(ZRAM_HOOK)
    with open(os.path.join(hook_dir, '02-setup-power.hook.chroot'), 'w') as f: f.write(TLP_HOOK)
    with open(os.path.join(hook_dir, '03-mate-theme.hook.chroot'), 'w') as f: f.write(THEME_HOOK)
    
    for filename in os.listdir(hook_dir):
        os.chmod(os.path.join(hook_dir, filename), 0o755)
    print("   ✅ Hooks generated.")

if __name__ == "__main__":
    data = load_yaml()
    generate_packages(data)
    generate_hooks(data)
    print("\n🚀 Translation Complete! Your ISO will now include the GENOME specs.")

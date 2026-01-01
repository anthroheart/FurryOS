#!/usr/bin/env python3
"""
===============================================================================
FURRYOS SIGNING KEY GENERATOR
===============================================================================
Location: /TOP/assets/generate_signing_keys.py
Generates Ed25519 keypair for self-signing all FurryOS binaries
Keys are saved in /TOP/signing_keys/
===============================================================================
"""

import os
import sys
from pathlib import Path
from datetime import datetime

def find_api_key():
    """
    Intelligently hunts for the API key by walking up the directory tree.
    Works regardless of where this script is run from.
    """
    import os, sys
    filename = 'Gemini_API.key.txt'
    current_search_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk up the tree (max 5 levels) to find the 'assets' folder
    for _ in range(5):
        potential_key = os.path.join(current_search_dir, 'assets', filename)
        if os.path.exists(potential_key):
            return potential_key
        
        # Move up one level
        parent_dir = os.path.dirname(current_search_dir)
        if parent_dir == current_search_dir: # We hit the root
            break
        current_search_dir = parent_dir
    
    # Fallback: Check Desktop
    desktop_fallback = os.path.expanduser('~/Desktop/Gemini_API.key.txt')
    if os.path.exists(desktop_fallback):
        return desktop_fallback

    print("❌ CRITICAL ERROR: Could not find 'Gemini_API.key.txt' anywhere.")
    sys.exit(1)


def banner():
    print("\n" + "="*80)
    print("   🔐 FURRYOS SIGNING KEY GENERATOR 🔐")
    print("="*80 + "\n")

def check_cryptography():
    """Check if cryptography is available"""
    try:
        import cryptography
        return True
    except ImportError:
        print("❌ cryptography package not found")
        print("")
        print("Please install it:")
        print("   Option 1 (venv): source activate_furryos.sh")
        print("   Option 2 (system): sudo pip3 install cryptography")
        print("   Option 3 (venv): ./setup_venv.sh")
        print("")
        return False

def generate_keypair():
    """Generate Ed25519 signing keypair"""
    from cryptography.hazmat.primitives.asymmetric import ed25519

    print("🔑 Generating Ed25519 keypair...")
    private_key = ed25519.Ed25519PrivateKey.generate()
    public_key = private_key.public_key()

    return private_key, public_key

def save_keys(private_key, public_key, key_dir):
    """Save keys to disk"""
    from cryptography.hazmat.primitives import serialization

    Path(key_dir).mkdir(parents=True, exist_ok=True)

    # Save private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    private_path = f"{key_dir}/furryos_signing.key"
    with open(private_path, 'wb') as f:
        f.write(private_pem)
    os.chmod(private_path, 0o600)
    print(f"✓ Private key: {private_path}")

    # Save public key
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    public_path = f"{key_dir}/furryos_signing.pub"
    with open(public_path, 'wb') as f:
        f.write(public_pem)
    os.chmod(public_path, 0o644)
    print(f"✓ Public key: {public_path}")

    # Save metadata
    metadata = f"""# FurryOS Signing Keys
Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
Algorithm: Ed25519
Purpose: Self-signing FurryOS binaries

## Private Key
File: furryos_signing.key
Permissions: 0600 (owner read/write only)
DO NOT SHARE THIS FILE!

## Public Key
File: furryos_signing.pub
Permissions: 0644 (world readable)
Distribute with binaries for verification

## Usage

### Sign a binary:
python3 assets/sign_binary.py furryos_build/bin/heartbeat_core

### Verify a signature:
python3 assets/verify_signature.py furryos_build/bin/heartbeat_core
"""

    with open(f"{key_dir}/README.txt", 'w') as f:
        f.write(metadata)

    print(f"✓ Metadata: {key_dir}/README.txt")

def main():
    banner()

    # Change to /TOP directory (parent of assets/)
    script_dir = os.path.dirname(os.path.abspath(__file__))
    if script_dir.endswith('/assets'):
        os.chdir(os.path.dirname(script_dir))

    # Check cryptography
    if not check_cryptography():
        sys.exit(1)

    KEY_DIR = "signing_keys"

    if os.path.exists(f"{KEY_DIR}/furryos_signing.key"):
        print(f"⚠️  Keys already exist in {KEY_DIR}/")
        response = input("Regenerate? [y/N]: ")
        if response.lower() != 'y':
            print("✓ Keeping existing keys")
            return

    private_key, public_key = generate_keypair()
    print(f"\n💾 Saving keys to {KEY_DIR}/")
    save_keys(private_key, public_key, KEY_DIR)

    print("\n" + "="*80)
    print("   🎉 SIGNING KEYS GENERATED! 🎉")
    print("="*80)
    print(f"\n📁 Location: {KEY_DIR}/")
    print("\n🔐 furryos_signing.key (PRIVATE - KEEP SECRET!)")
    print("🔓 furryos_signing.pub (PUBLIC - DISTRIBUTE)")
    print("📝 README.txt (usage instructions)")
    print("\n🔒 Security:")
    print("   • Private key permissions: 0600 (owner only)")
    print("   • Public key permissions: 0644 (world readable)")
    print("   • Algorithm: Ed25519 (256-bit security)")
    print("\n🐾 Keys ready for signing binaries! 🌱\n")

if __name__ == "__main__":
    main()
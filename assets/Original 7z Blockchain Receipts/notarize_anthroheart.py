#!/usr/bin/env python3
"""
===============================================================================
 The AnthroHeart Collection – Genesis Notarization (2025)
===============================================================================
Date:   December 25, 2025
Author: AnthroHeart Project
Organization: Anthro Entertainment LLC
Type:   Genesis Record (Sequence 0)
===============================================================================
"""

import os
import sys
import subprocess
import platform
import shutil
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 1. VENV BOOTSTRAP (Cross-Platform & Self-Healing)
# ---------------------------------------------------------------------------

VENV_DIR = ".venv"
REQUIRED_PACKAGES = ["pynacl", "opentimestamps-client"]

def in_venv():
    return sys.prefix != sys.base_prefix

def bootstrap_venv():
    # Detect Python executable for the venv
    if platform.system() == "Windows":
        venv_python = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        venv_python = os.path.join(VENV_DIR, "bin", "python")

    if not os.path.exists(VENV_DIR):
        print(f"🔧 Creating virtual environment in {VENV_DIR}...")
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

    # If we are not in the venv, install deps and relaunch
    if not in_venv():
        print("📦 Verifying dependencies...")
        subprocess.check_call([venv_python, "-m", "pip", "install", "--upgrade", "pip", "-q"])
        subprocess.check_call([venv_python, "-m", "pip", "install", *REQUIRED_PACKAGES, "-q"])
        
        print("🔁 Re-launching script inside venv...\n")
        subprocess.check_call([venv_python] + sys.argv)
        sys.exit(0)

if not in_venv():
    bootstrap_venv()

# ---------------------------------------------------------------------------
# 2. CORE LOGIC
# ---------------------------------------------------------------------------

import json
import hashlib
from nacl.signing import SigningKey
from nacl.encoding import HexEncoder

# CONFIGURATION
FILE_PATH = "The_AnthroHeart_Collection_Bundle.7z"
OUT_DIR = "anthroheart_chain"
KEY_FILE = "anthroheart_genesis.key"

METADATA = {
    "author": "AnthroHeart Project",
    "organization": "Anthro Entertainment LLC",
    "license": "CC0-1.0",
    "website": "https://anthroentertainment.com",
    "publication_date": "2025-12-25",
    "notes": "Genesis record. Hash-only notarization anchored via OpenTimestamps."
}

def get_hashes(filepath):
    print(f"⚙️  Hashing {filepath} (SHA256 & SHA512)...")
    sha256 = hashlib.sha256()
    sha512 = hashlib.sha512()
    
    total_size = os.path.getsize(filepath)
    processed = 0
    
    with open(filepath, "rb") as f:
        while chunk := f.read(4096 * 4096): # 16MB chunks
            sha256.update(chunk)
            sha512.update(chunk)
            processed += len(chunk)
            if total_size > 0:
                print(f"   Progress: {int((processed/total_size)*100)}%", end="\r")
            
    print("\n   Hashing complete.")
    return sha256.hexdigest(), sha512.hexdigest()

def load_or_generate_key(key_path):
    if os.path.exists(key_path):
        print(f"🔑 Loading existing identity from {key_path}...")
        with open(key_path, "r") as f:
            private_hex = f.read().strip()
        return SigningKey(private_hex, encoder=HexEncoder)
    else:
        print(f"✨ Generating NEW Genesis Identity...")
        signing_key = SigningKey.generate()
        private_hex = signing_key.encode(encoder=HexEncoder).decode()
        with open(key_path, "w") as f:
            f.write(private_hex)
        print(f"⚠️  WARNING: {key_path} created. BACK THIS UP. You need it to sign future updates.")
        return signing_key

def main():
    if not os.path.exists(FILE_PATH):
        print(f"❌ Error: Archive not found: {FILE_PATH}")
        sys.exit(1)

    os.makedirs(OUT_DIR, exist_ok=True)

    # 1. Manage Identity
    signing_key = load_or_generate_key(os.path.join(OUT_DIR, KEY_FILE))
    verify_key = signing_key.verify_key
    public_key_hex = verify_key.encode(encoder=HexEncoder).decode()

    # Save public key for verification
    with open(os.path.join(OUT_DIR, "anthro_public.key"), "w") as f:
        f.write(public_key_hex)

    # 2. Hash Content
    h256, h512 = get_hashes(FILE_PATH)

    # 3. Sign Hashes
    signature = signing_key.sign(h512.encode()).signature.hex()

    # 4. Construct Genesis Metadata
    record = {
        "manifest_version": "1.0",
        "sequence": 0,
        "previous_record": None,
        # Fixed the deprecated datetime warning
        "timestamp_claim": datetime.now(timezone.utc).isoformat(),
        
        "file_info": {
            "filename": FILE_PATH,
            "size_bytes": os.path.getsize(FILE_PATH),
            "hashes": {
                "sha256": h256,
                "sha512": h512
            }
        },
        "identity": {
            "public_key": public_key_hex,
            "signature_of_sha512": signature,
            "algorithm": "Ed25519"
        },
        "metadata": METADATA
    }

    # 5. Save Record
    record_filename = f"genesis_record_{METADATA['publication_date']}.json"
    record_path = os.path.join(OUT_DIR, record_filename)

    with open(record_path, "w") as f:
        json.dump(record, f, indent=2, sort_keys=True)

    # 6. Timestamp (FIXED)
    print(f"⏳ Submitting to Bitcoin blockchain via OpenTimestamps...")
    
    # Calculate path to the 'ots' executable inside the venv to avoid PATH errors
    if platform.system() == "Windows":
        ots_executable = os.path.join(sys.prefix, "Scripts", "ots.exe")
    else:
        ots_executable = os.path.join(sys.prefix, "bin", "ots")

    try:
        if not os.path.exists(ots_executable):
            # Fallback for some linux distros if they put it elsewhere in venv
            ots_executable = "ots" 
            
        subprocess.check_call([ots_executable, "stamp", record_path])
        print("✅ Timestamp proof created successfully.")
        
        # 7. Final Report
        print("\n" + "="*60)
        print(" ANTHROHEART COLLECTION - GENESIS COMPLETE")
        print("="*60)
        print(f"📂 Output Directory: {OUT_DIR}/")
        print(f"📄 Genesis Record:   {record_filename}")
        print(f"🛡️  Proof File:       {record_filename}.ots")
        print(f"🔑 Identity Key:     {KEY_FILE} (DO NOT SHARE/LOSE THIS)")
        print("-" * 60)
        print("Next Steps:")
        print("1. Keep the .ots file safe. It is your proof.")
        print("2. When you upgrade this collection, increment 'sequence' to 1")
        print("   and hash this genesis JSON as 'previous_record'.")
        print("="*60)
        
    except subprocess.CalledProcessError:
        print("❌ Error: OpenTimestamps server returned an error.")
        print("   Wait a moment and try running manually: 'ots stamp <file>'")
    except FileNotFoundError:
        print(f"❌ Error: Could not find 'ots' executable at {ots_executable}")
        print("   Please ensure the requirements installed correctly.")

if __name__ == "__main__":
    main()
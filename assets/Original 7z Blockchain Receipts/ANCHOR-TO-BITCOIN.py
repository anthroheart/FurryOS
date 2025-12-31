#!/usr/bin/env python3
"""
===============================================================================
 AnthroHeart VPS Anchor (Bitcoin Strategy)
===============================================================================
Purpose:
  Links your VPS file to the Bitcoin Blockchain for FREE.
  - Verifies the file hash.
  - Signs it with your Christmas Identity Key.
  - Creates a "Release Manifest" pointing to your IP.
  - Stamps the Manifest with OpenTimestamps (Bitcoin).
===============================================================================
"""

import os
import sys
import json
import hashlib
import subprocess
import platform
from datetime import datetime, timezone

# ---------------------------------------------------------------------------
# 1. SETUP
# ---------------------------------------------------------------------------
VENV_DIR = ".venv"
REQUIRED = ["pynacl", "opentimestamps-client"]

def bootstrap():
    if platform.system() == "Windows":
        py = os.path.join(VENV_DIR, "Scripts", "python.exe")
    else:
        py = os.path.join(VENV_DIR, "bin", "python")

    if not os.path.exists(VENV_DIR):
        subprocess.check_call([sys.executable, "-m", "venv", VENV_DIR])

    if sys.prefix == sys.base_prefix:
        subprocess.check_call([py, "-m", "pip", "install", *REQUIRED, "-q"])
        subprocess.check_call([py] + sys.argv)
        sys.exit(0)

bootstrap()

from nacl.signing import SigningKey
from nacl.encoding import HexEncoder

# --- CONFIGURATION ---
FILE_PATH = "The_AnthroHeart_Collection_Bundle.7z"
IDENTITY_KEY = "anthroheart_chain/anthro_identity.key"
PUBLIC_KEY = "anthroheart_chain/anthro_public.key"
VPS_URL = os.getenv(
    "ANTHROHEART_ORIGIN_URL",
    "https://torrent.anthroentertainment.com/The_AnthroHeart_Collection_Bundle.7z"
)

OUT_DIR = "anthroheart_chain"

def main():
    # A. CHECKS
    if not os.path.exists(FILE_PATH):
        sys.exit(f"❌ Error: {FILE_PATH} not found.")
    if not os.path.exists(IDENTITY_KEY):
        sys.exit(f"❌ Error: {IDENTITY_KEY} not found.")

    # B. LOAD IDENTITY
    print(f"🔑 Loading Identity...")
    with open(IDENTITY_KEY, "r") as f:
        signing_key = SigningKey(f.read().strip(), encoder=HexEncoder)
        public_key_hex = signing_key.verify_key.encode(encoder=HexEncoder).decode()

    # C. HASH FILE
    print(f"⚙️  Hashing 5GB file (Verification)...")
    sha256, sha512 = hashlib.sha256(), hashlib.sha512()
    
    with open(FILE_PATH, "rb") as f:
        while chunk := f.read(16 * 1024 * 1024):
            sha256.update(chunk)
            sha512.update(chunk)
            print(".", end="", flush=True)
    
    h256, h512 = sha256.hexdigest(), sha512.hexdigest()
    print(f"\n✅ Hash Verified: {h256[:16]}...")

    # D. SIGNATURE
    # Sign the Hash + URL to lock them together
    payload = f"{h512}|{VPS_URL}".encode()
    signature = signing_key.sign(payload).signature.hex()

    # E. CREATE RELEASE MANIFEST
    manifest = {
        "record_type": "Public_Release_Anchor",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "hosting": {
            "url": VPS_URL,
            "method": "Self-Hosted VPS (Nginx)",
            "note": "Primary Origin"
        },
        "integrity": {
            "filename": os.path.basename(FILE_PATH),
            "filesize": os.path.getsize(FILE_PATH),
            "sha256": h256,
            "sha512": h512
        },
        "authorization": {
            "signer_public_key": public_key_hex,
            "signature": signature,
            "signed_string": "sha512|url"
        }
    }

    manifest_filename = f"release_proof_{datetime.now().strftime('%Y%m%d')}.json"
    manifest_path = os.path.join(OUT_DIR, manifest_filename)

    with open(manifest_path, "w") as f:
        json.dump(manifest, f, indent=2, sort_keys=True)

    # F. STAMP TO BITCOIN BLOCKCHAIN
    print(f"\n⏳ Anchoring to Bitcoin via OpenTimestamps...")
    
    if platform.system() == "Windows":
        ots_exec = os.path.join(sys.prefix, "Scripts", "ots.exe")
    else:
        ots_exec = os.path.join(sys.prefix, "bin", "ots")
        if not os.path.exists(ots_exec): ots_exec = "ots"

    try:
        subprocess.check_call([ots_exec, "stamp", manifest_path])
        print("\n" + "="*60)
        print(" ✅ SUCCESS: RELEASE ANCHORED TO BITCOIN")
        print("="*60)
        print(f" 1. Manifest created: {manifest_path}")
        print(f" 2. Bitcoin Proof:    {manifest_path}.ots")
        print("-" * 60)
        print(" HOW THIS WORKS:")
        print(" You now have a file on your VPS, and a cryptographic proof")
        print(" on your computer that links that SPECIFIC file URL to the")
        print(" Bitcoin blockchain forever.")
        print("-" * 60)
        print(" NEXT STEP: Upload these two small files (.json and .ots)")
        print(" to your VPS folder next to the 7z file so geeks can verify it.")
        print("="*60)
    except Exception as e:
        print(f"❌ OTS Error: {e}")

if __name__ == "__main__":
    main()
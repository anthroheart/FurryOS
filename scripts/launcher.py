#!/usr/bin/env python3
"""
===============================================================================
FURRYOS MASTER LAUNCHER v8.2 "Madhatter"
===============================================================================
"""
import os
import sys
import subprocess
import shutil
from pathlib import Path

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


BUILD_DIR = Path("furryos_build")
BIN_DIR = BUILD_DIR / "bin"
ASSETS_DIR = Path("assets")
KEY_PATH = "signing_keys/furryos_signing.key"

# Replacing fragile API key loading with the robust function
API_KEY_FILE = find_api_key()

def run_cmd(cmd, desc):
    print(f"⚡ {desc}...")
    subprocess.run(cmd, shell=True, check=True)

def compile_heartbeat():
    print("\n[ Module: Heartbeat Core (C + ASM) ]")
    c_src = ASSETS_DIR / "heartbeat_core.c"
    asm_src = ASSETS_DIR / "heartbeat_core_asm.s"
    output_bin = BIN_DIR / "heartbeat_core"
    
    if shutil.which("nasm") and asm_src.exists():
        obj_asm = BUILD_DIR / "heartbeat_core_asm.o"
        run_cmd(f"nasm -f elf64 {asm_src} -o {obj_asm}", "Assembling x86_64 Core")
        # -no-pie is crucial for raw ASM integration
        run_cmd(f"gcc -O3 -march=native -pthread -no-pie {c_src} {obj_asm} -o {output_bin}", "Linking Core")
    else:
        print("⚠️  NASM missing or asm source missing.")

def compile_healer():
    print("\n[ Module: The Healer ]")
    healer_src = ASSETS_DIR / "healer_core.cpp"
    if not healer_src.exists():
        # Embed minimal healer just in case
        with open(healer_src, "w") as f:
            f.write(r'''#include <iostream>
#include <unistd.h>
#include <sys/wait.h>
#include <thread>
#include <chrono>
int main(int argc, char* argv[]) {
    if(argc<2)return 1;
    while(1){
        if(fork()==0) { execvp(argv[1],&argv[1]); exit(1); }
        int s; wait(&s); 
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }
}''')
    run_cmd(f"g++ -O3 {healer_src} -o {BIN_DIR}/healer", "Compiling Healer")

def sign_binaries():
    print("\n[ Security: Signing Binaries ]")
    if not os.path.exists(KEY_PATH): return
    try:
        from cryptography.hazmat.primitives.asymmetric import ed25519
        from cryptography.hazmat.primitives import serialization
        with open(KEY_PATH, 'rb') as f:
            private_key = serialization.load_pem_private_key(f.read(), password=None)
        for binary in BIN_DIR.glob('*'):
            if binary.is_file() and not binary.suffix == '.sig':
                with open(binary, 'rb') as f: data = f.read()
                with open(f"{binary}.sig", 'wb') as f: f.write(private_key.sign(data))
                print(f"   🔐 Signed: {binary.name}")
    except: pass

def main():
    if os.geteuid() != 0: sys.exit("❌ Run as root")
    for d in [BUILD_DIR, BIN_DIR]: d.mkdir(parents=True, exist_ok=True)
    compile_heartbeat()
    compile_healer()
    sign_binaries()
    print("\n✨ Binaries Ready.")

if __name__ == "__main__":
    main()
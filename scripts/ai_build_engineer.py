import os
import sys
import google.generativeai as genai
from pathlib import Path

# --- CONFIGURATION ---
ROOT_DIR = Path.cwd()
KEY_FILE = ROOT_DIR / 'Gemini_API.key.txt'
CONFIG_DIR = ROOT_DIR / 'config'
INCLUDES_DIR = CONFIG_DIR / 'includes.chroot'

# Define target paths for AI generation
SYSCTL_PATH = INCLUDES_DIR / 'etc' / 'sysctl.d' / '99-furryos-ai-tuned.conf'
MOTD_PATH = INCLUDES_DIR / 'etc' / 'motd'

def get_api_key():
    if not KEY_FILE.exists():
        print(f"❌ API Key not found at {KEY_FILE}")
        sys.exit(1)
    return KEY_FILE.read_text().strip()

def setup_directories():
    os.makedirs(SYSCTL_PATH.parent, exist_ok=True)
    os.makedirs(MOTD_PATH.parent, exist_ok=True)

def generate_optimizations(model):
    print("🧠 AI Engineer: Analyzing Kernel Parameters for Debian 13...")

    prompt = """
    You are a Senior Linux Kernel Architect building 'FurryOS' (Debian 13 Trixie base).
    Target: Modern Desktop/Workstation (2025/2026 Hardware).
    Goal: Maximize desktop responsiveness, reduce latency, and optimize NVMe/SSD IO.

    OUTPUT REQUIREMENTS:
    Generate a valid 'sysctl.conf' file content.
    Include settings for:
    1. Virtual Memory (swappiness, vfs_cache_pressure) - Optimized for desktop responsiveness.
    2. Network (TCP Fast Open, BBR congestion control).
    3. File System (max_user_watches for heavy dev work).
    4. Kernel panic behavior (reboot automatically).

    Output ONLY the raw file content. No markdown formatting.
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.replace("```", "").strip()

        with open(SYSCTL_PATH, 'w') as f:
            f.write(f"# FurryOS AI-Tuned Kernel Config\n# Generated: {os.environ.get('DATE', 'Unknown')}\n\n")
            f.write(content)
        print(f"   ✅ Generated Kernel Tuning: {SYSCTL_PATH}")
    except Exception as e:
        print(f"   ⚠️ AI Generation failed: {e}")
        # Fallback safe defaults
        with open(SYSCTL_PATH, 'w') as f:
            f.write("vm.swappiness=10\nfs.inotify.max_user_watches=524288\n")

def generate_motd(model):
    print("🧠 AI Engineer: Writing System Welcome Message...")

    prompt = """
    Write a short, inspiring Message of the Day (/etc/motd) for FurryOS users.
    Theme: "A New Paradigm of Joy and Technology."
    Mention: Debian 13 Base, Privacy Focused, Community Driven.
    Style: Professional but warm. ASCII art of a small fox face is optional but welcome.
    Output ONLY the raw text.
    """

    try:
        response = model.generate_content(prompt)
        content = response.text.replace("```", "").strip()

        with open(MOTD_PATH, 'w') as f:
            f.write(content)
        print(f"   ✅ Generated MOTD: {MOTD_PATH}")
    except Exception as e:
        print(f"   ⚠️ AI Generation failed: {e}")

def main():
    setup_directories()

    try:
        key = get_api_key()
        genai.configure(api_key=key)
        # Use a model likely to exist in 2025/2026 context or fallback
        model = genai.GenerativeModel('gemini-1.5-flash')

        generate_optimizations(model)
        generate_motd(model)

    except Exception as e:
        print(f"❌ Critical AI Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()

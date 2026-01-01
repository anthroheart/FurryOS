import os
import time
import google.generativeai as genai
import sys

# --- SMART CONFIGURATION ---

def find_api_key():
    """
    Intelligently hunts for the API key by walking up the directory tree.
    Works regardless of where this script is run from.
    """
    filename = 'Gemini_API.key.txt'
    
    # Start where the script lives
    current_search_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Walk up the tree (max 5 levels) to find the 'assets' folder
    for _ in range(5):
        potential_key = os.path.join(current_search_dir, 'assets', filename)
        
        if os.path.exists(potential_key):
            print(f"🔑 Found API Key at: {potential_key}")
            return potential_key
        
        # Move up one level
        parent_dir = os.path.dirname(current_search_dir)
        if parent_dir == current_search_dir: # We hit the root of the drive
            break
        current_search_dir = parent_dir
        
    # Emergency fallback: Check the specific Desktop path seen in your screenshots
    desktop_fallback = '/home/anthro/Desktop/Gemini_API.key.txt'
    if os.path.exists(desktop_fallback):
        print(f"🔑 Found API Key on Desktop: {desktop_fallback}")
        return desktop_fallback

    print("❌ CRITICAL ERROR: Could not find 'Gemini_API.key.txt' anywhere.")
    print("   Please ensure it is in an 'assets' folder inside your project.")
    sys.exit(1)

def find_config_dir():
    """Finds the config directory relative to the found key or script."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try generic relative path first
    relative_config = os.path.abspath(os.path.join(script_dir, '..', 'config'))
    if os.path.exists(relative_config):
        return relative_config
        
    # If that fails, look in current dir
    if os.path.exists('config'):
        return os.path.abspath('config')
        
    print("⚠️  Warning: Could not locate 'config' folder.")
    return None

# --- AI LOGIC ---

SYSTEM_PROMPT = """
You are a Senior Linux Distro Engineer.
Your Goal: READ the user's config file (YAML/JSON) and SUPERCHARGE it.
1. ANALYZE: Look for missing modern features (Btrfs, ZRAM, Wayland, Theming).
2. EXPAND: Add these features directly to the file.
3. OUTPUT: Return ONLY the valid, upgraded file content.
"""

def get_api_key_content(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        print(f"❌ Error reading key file: {e}")
        sys.exit(1)

def enhance_file(model, file_path):
    print(f"🧠 Enhancing: {os.path.basename(file_path)}...")
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Skip empty or tiny files
    if len(content) < 10: 
        return

    try:
        response = model.generate_content(f"{SYSTEM_PROMPT}\n\nFILE CONTENT:\n{content}")
        if response.text:
            new_content = response.text.replace("```yaml", "").replace("```json", "").replace("```", "").strip()
            
            # Save backup
            os.rename(file_path, file_path + ".original")
            
            # Write new
            with open(file_path, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f"   ✅ Upgraded!")
    except Exception as e:
        print(f"   ⚠️ Failed: {e}")

if __name__ == "__main__":
    # 1. Locate Resources
    key_path = find_api_key()
    config_dir = find_config_dir()
    
    if not config_dir:
        print("Nothing to enhance (Config folder missing). Exiting.")
        sys.exit(0)

    # 2. Setup AI
    key = get_api_key_content(key_path)
    genai.configure(api_key=key)
    
    # Try to find the best model (fallback logic included)
    model = genai.GenerativeModel('gemini-2.5-flash')
    
    # 3. Execute
    print(f"📂 Scanning for configs in: {config_dir}")
    count = 0
    for root, dirs, files in os.walk(config_dir):
        for file in files:
            if file.endswith(('.yaml', '.yml', '.json', '.conf')):
                enhance_file(model, os.path.join(root, file))
                count += 1
                time.sleep(1) # Polite rate limiting
    
    if count == 0:
        print("   No .yaml/.json/.conf files found to enhance.")
    else:
        print(f"\n✨ Processed {count} configuration files.")

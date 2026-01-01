import os
import datetime
import markdown
from xhtml2pdf import pisa
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


# ==============================================================================
# CONFIGURATION
# ==============================================================================
OUTPUT_FILENAME = "FurryOS_Complete_Documentation.pdf"
VERSION = "8.0.0-origin"
TIMESTAMP = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
BRANDING = "Anthro Entertainment LLC"

SOURCE_DIRS = [".", "guides"]
EXTENSIONS = [".md", ".txt", ".yaml", ".json"]

EXCLUDE_FILES = [
    "requirements.txt", "MANIFEST.txt", "Gemini_API.key.txt",
    "compile_docs.py", "patch_furryos_optimized.py", "LICENSE",
    "create_partitions.py", "deploy_iso.py", "launcher.py"
]

# ==============================================================================
# LOGICAL BOOK STRUCTURE
# ==============================================================================
BOOK_STRUCTURE = {
    "1. Overview": [
        "README.md",
        "ISO_README.txt",
        "VERSION_REFERENCE.md",
    ],
    "2. Configuration": [
        "GENOME.yaml",
        "USER_CONFIG.yaml",
    ],
    "3. Build System": [
        "FRESH_BUILD_GUIDE.md",
        "BUILD_OPTIONS.md",
        "BUILD_SUMMARY.md",
        "PROGRESS_FEATURES.md",
        "VENV_GUIDE.md",
    ],
    "4. Features & Usage": [
        "ANTHROHEART_INCLUSION_GUIDE.md",
        "PERSISTENCE_GUIDE.md",
        "SMART_PARTITION_GUIDE.md",
        "ETCHER_INCLUSION_GUIDE.md",
        "SIGNING_GUIDE.md",
    ],
    "5. Technical Reference": [
        "C_ASSEMBLY_OPTIMIZATION.md",
        "ASSEMBLY_OPTIMIZATION_PLAN.md",
        "FILE_ORGANIZATION.md",
        "PACKAGE_LIST.md",
    ],
    "6. Troubleshooting": [
        "UPDATE_INSTRUCTIONS.md",
        "USB_WRITING_GUIDE.md",
        "FIX_SUMMARY.md",
        "PEP668_FIX_GUIDE.md",
    ]
}

# ==============================================================================
# TEXT SANITIZER
# ==============================================================================
def sanitize_text(text):
    replacements = {
        "├──": "|--", "└──": "`--", "│": "|  ", "──": "--",
        "✅": "[OK] ", "❌": "[X] ", "⚠️": "[!] ", "🚀": ">> ",
        "🐾": "", "🌱": "", "✨": "* ", "🔒": "[SEC] ",
        "🔐": "[KEY] ", "📦": "[PKG] ", "📁": "[DIR] ",
        "📄": "[FILE] ", "🔧": "[TOOL] ", "🐛": "[BUG] ",
        "💡": "[TIP] ", "🎨": "[ART] ", "💾": "[DISK] ",
        "📊": "[STATS] ", "📝": "[NOTE] ", "👉": "-> ",
        "🎉": "!",
    }
    for char, replacement in replacements.items():
        text = text.replace(char, replacement)
    return text

# ==============================================================================
# CSS STYLING
# ==============================================================================
CSS = """
    @page {
        size: letter;
        margin: 0.75in;
        margin-bottom: 1.2in;
        @frame footer_frame {
            -pdf-frame-content: footerContent;
            bottom: 0.5in;
            margin-left: 0.75in;
            margin-right: 0.75in;
            height: 0.5in;
        }
    }
    body {
        font-family: Helvetica, sans-serif;
        font-size: 10pt;
        line-height: 1.4;
        color: #222;
    }

    /* Footer */
    #footerContent {
        text-align: center;
        font-size: 8pt;
        color: #888;
        border-top: 1px solid #ccc;
        padding-top: 5px;
    }

    /* Headers */
    h1 { color: #E85D04; border-bottom: 2px solid #333; padding-bottom: 5px; margin-top: 0px; font-size: 18pt; }
    h2 { color: #333; margin-top: 20px; font-size: 14pt; border-bottom: 1px solid #ddd; }
    h3 { color: #555; font-size: 12pt; margin-top: 15px; font-weight: bold; }

    /* Document Title Headers */
    h1.doc-title {
        background-color: #333;
        color: #fff;
        padding: 5px 10px;
        font-family: Courier, monospace;
        font-size: 11pt;
        margin-bottom: 20px;
        border-radius: 3px;
        page-break-after: avoid;
    }

    h1.section-title {
        color: #E85D04;
        font-size: 24pt;
        text-align: center;
        margin-top: 200px;
        page-break-after: always;
    }

    /* Code Blocks */
    pre {
        font-family: 'Courier New', Courier, monospace;
        background-color: #f4f4f4;
        color: #000;
        padding: 8px;
        border: 1px solid #ccc;
        border-radius: 4px;
        font-size: 7pt;
        line-height: 1.2;
        white-space: pre;
        overflow: hidden;
        display: block;
        margin-bottom: 15px;
    }
    code { font-family: 'Courier New', Courier, monospace; background-color: #eee; padding: 2px 4px; font-size: 9pt; }

    /* Page Breaks */
    .file-break { page-break-before: always; }

    /* Cover Page */
    .cover-page { text-align: center; margin-top: 100px; page-break-after: always; }
    .cover-title { font-size: 36pt; font-weight: bold; color: #E85D04; margin-top: 20px; }

    /* Doc Control Table */
    .doc-control { margin-top: 50px; width: 100%; border-collapse: collapse; }
    .doc-control td { border: 1px solid #ddd; padding: 8px; font-size: 9pt; }
    .doc-control th { background-color: #eee; border: 1px solid #ddd; padding: 8px; font-size: 9pt; text-align: left; }
"""

def get_file_content(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            text = f.read()
    except Exception:
        return ""

    text = sanitize_text(text)
    ext = os.path.splitext(filepath)[1].lower()
    filename = os.path.basename(filepath)

    html = f"<div class='file-break'><h1 class='doc-title'>{filename}</h1>"

    if ext == ".md":
        try:
            html += markdown.markdown(text, extensions=['extra', 'codehilite'])
        except Exception:
            html += f"<pre>{text}</pre>"
    else:
        html += f"<pre>{text}</pre>"

    html += "</div>"
    return html

def find_file_path(filename):
    for d in SOURCE_DIRS:
        possible_path = os.path.join(d, filename)
        if os.path.exists(possible_path) and os.path.isfile(possible_path):
            return possible_path
    return None

def collect_appendix_files(processed_files):
    appendix = []
    for d in SOURCE_DIRS:
        if not os.path.exists(d): continue
        if d == ".":
            candidates = [f for f in os.listdir(d) if os.path.isfile(f)]
        else:
            candidates = []
            for root, _, files in os.walk(d):
                for f in files: candidates.append(os.path.join(root, f))

        for f_path in candidates:
            fname = os.path.basename(f_path)
            if fname in processed_files or fname in EXCLUDE_FILES or fname.startswith('.'):
                continue
            if os.path.splitext(fname)[1].lower() in EXTENSIONS:
                full_path = f_path if d == "." else f_path
                appendix.append(full_path)
    appendix.sort()
    return appendix

def get_logo_html():
    """Finds logo.png or icon.png and returns HTML image tag."""
    possible_logos = ["images/logo.png", "images/icon.png"]
    logo_path = None

    for rel_path in possible_logos:
        full_path = os.path.abspath(rel_path)
        if os.path.exists(full_path):
            logo_path = full_path
            print(f"🖼️  Found branding image: {rel_path}")
            break

    if logo_path:
        # 250px width ensures it fits nicely on the page
        return f'<img src="{logo_path}" style="width: 250px; height: auto; margin-bottom: 20px;" />'
    return ""

def generate_pdf():
    print("🐾 FurryOS Docs Compiler (Branded) 🐾")

    content_html = ""
    processed_filenames = set()

    # --- Process Sections ---
    for section_name, files in BOOK_STRUCTURE.items():
        print(f"📘 Processing Section: {section_name}")
        for filename in files:
            full_path = find_file_path(filename)
            if full_path:
                print(f"   + {filename}")
                content_html += get_file_content(full_path)
                processed_filenames.add(filename)
            else:
                print(f"   ⚠️  Missing: {filename}")

    # --- Process Appendix ---
    appendix_files = collect_appendix_files(processed_filenames)
    if appendix_files:
        print("📎 Processing Appendix...")
        content_html += "<div class='file-break'><h1 class='doc-title'>Appendix</h1></div>"
        for full_path in appendix_files:
            filename = os.path.basename(full_path)
            print(f"   + {filename}")
            content_html += get_file_content(full_path)

    # --- Build Final HTML ---
    logo_html = get_logo_html()

    full_html = f"""
    <html>
    <head><style>{CSS}</style></head>
    <body>
        <div id="footerContent">FurryOS {VERSION} — <pdf:pagenumber></div>

        <!-- COVER PAGE -->
        <div class="cover-page">
            {logo_html}
            <div class="cover-title">FurryOS</div>
            <div style="font-size: 24pt; color: #555;">Complete Documentation</div>

            <div style="margin-top: 50px; color: #888;">Generated: {TIMESTAMP}</div>
            <div style="margin-top: 20px; font-size: 14pt; color: #333; font-weight: bold;">{BRANDING}</div>

            <!-- Document Control Table -->
            <br><br><br>
            <table class="doc-control" align="center" style="width: 80%;">
                <tr><th>Version</th><td>{VERSION}</td></tr>
                <tr><th>Status</th><td>Origin Release</td></tr>
                <tr><th>Codename</th><td>Sovereign Universe</td></tr>
                <tr><th>License</th><td>MIT License (Public)</td></tr>
            </table>
        </div>

        <!-- INDEX -->
        <div class="file-break">
            <h1 style="color: #333; border: none;">Table of Contents</h1>
            <pdf:toc />
        </div>

        <!-- CONTENT -->
        {content_html}
    </body></html>
    """

    print(f"✍️  Writing PDF to {OUTPUT_FILENAME}...")
    try:
        with open(OUTPUT_FILENAME, "wb") as output_file:
            pisa_status = pisa.CreatePDF(src=full_html, dest=output_file)
        if not pisa_status.err:
            print(f"✅ Success! PDF saved to: {os.path.abspath(OUTPUT_FILENAME)}")
        else:
            print("❌ Error generating PDF")
    except Exception as e:
        print(f"❌ Critical Error: {e}")

if __name__ == "__main__":
    generate_pdf()
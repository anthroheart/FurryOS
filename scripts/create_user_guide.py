import os
import datetime
import sys
import io
import textwrap

try:
    from reportlab.lib.pagesizes import letter
    from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image, PageBreak, Table, TableStyle, KeepTogether
    from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
    from reportlab.lib import colors
    from reportlab.lib.units import inch
    from PIL import Image as PILImage
except ImportError:
    print("❌ Error: Missing libraries.")
    print("   Please run: pip install reportlab pillow")
    sys.exit(1)

# --- CONFIGURATION ---
ROOT_DIR = os.getcwd()
ASSETS_DIR = os.path.join(ROOT_DIR, 'assets')
LORE_DIR = os.path.join(ROOT_DIR, 'lore')
CONFIG_DIR = os.path.join(ROOT_DIR, 'config')
OUTPUT_PDF = "FurryOS_Official_Handbook.pdf"

# Theme Colors
COLOR_PRIMARY = colors.HexColor("#003366")
COLOR_ACCENT = colors.HexColor("#FF6600")
COLOR_TEXT = colors.HexColor("#333333")
COLOR_CODE_BG = colors.HexColor("#F5F5F5")

def header_footer(canvas, doc):
    canvas.saveState()
    canvas.setFont('Helvetica', 9)
    canvas.setFillColor(colors.grey)
    # Fixed: Draw footer LOWER (0.4 inch) so it's below the text margin (0.9 inch)
    canvas.drawString(inch, 0.4 * inch, "FurryOS Golden Master Handbook")
    canvas.drawRightString(7.5 * inch, 0.4 * inch, f"Page {doc.page}")
    canvas.restoreState()

def get_optimized_image(filename, display_width=6*inch, max_display_height=8*inch):
    """Finds, Resizes, and Compresses images."""
    search_paths = [
        os.path.join(ASSETS_DIR, 'wallpapers'),
        os.path.join(ASSETS_DIR, 'images', 'AnthroHeart Saga'),
        os.path.join(ASSETS_DIR, 'images'),
        ASSETS_DIR
    ]

    best_path = None
    for folder in search_paths:
        if not os.path.exists(folder): continue
        for root, dirs, files in os.walk(folder):
            if filename in files:
                best_path = os.path.join(root, filename)
                break
        if best_path: break

    if not best_path: return None

    try:
        with PILImage.open(best_path) as pil_img:
            img_w, img_h = pil_img.size
            aspect = img_h / float(img_w)
            final_display_h = display_width * aspect

            if final_display_h > max_display_height:
                final_display_h = max_display_height
                display_width = final_display_h / aspect

            # Downsample for PDF (150 DPI target)
            target_px_w = int(display_width / inch * 150)
            target_px_h = int(final_display_h / inch * 150)
            pil_img = pil_img.resize((target_px_w, target_px_h), PILImage.Resampling.LANCZOS)

            img_buffer = io.BytesIO()
            if pil_img.mode in ('RGBA', 'LA') or (pil_img.mode == 'P' and 'transparency' in pil_img.info):
                pil_img.save(img_buffer, format='PNG', optimize=True)
            else:
                if pil_img.mode != 'RGB': pil_img = pil_img.convert('RGB')
                pil_img.save(img_buffer, format='JPEG', quality=85)

            img_buffer.seek(0)
            rl_img = Image(img_buffer)
            rl_img.drawWidth = display_width
            rl_img.drawHeight = final_display_h
            return rl_img
    except: return None

def read_file(filepath):
    if not os.path.exists(filepath): return None
    try:
        with open(filepath, 'r', encoding='utf-8', errors='replace') as f:
            return f.read()
    except: return None

def process_yaml_for_pdf(text, style):
    """Splits YAML content into individual Paragraph lines for safe pagination."""
    flowables = []
    lines = text.split('\n')

    for line in lines:
        formatted_line = line.replace(" ", "&nbsp;")
        # Wrap long lines to prevent overflow
        if len(line) > 85:
            wrapped = textwrap.wrap(line, width=85)
            for w in wrapped:
                flowables.append(Paragraph(w.replace(" ", "&nbsp;"), style))
        else:
            flowables.append(Paragraph(formatted_line, style))

    return flowables

def generate_handbook():
    print(f"📘 Compiling Final Handbook ({OUTPUT_PDF})...")

    # Fixed: Increased bottomMargin to 0.9 inch to leave room for the footer
    doc = SimpleDocTemplate(OUTPUT_PDF, pagesize=letter,
                            rightMargin=36, leftMargin=36,
                            topMargin=50, bottomMargin=0.9*inch)

    story = []
    styles = getSampleStyleSheet()

    # Styles
    style_title = ParagraphStyle('Title', parent=styles['Title'], fontSize=32, textColor=COLOR_PRIMARY, spaceAfter=20)
    style_h1 = ParagraphStyle('H1', parent=styles['Heading1'], fontSize=20, textColor=COLOR_ACCENT, spaceBefore=20, spaceAfter=10, borderPadding=0, borderBottomWidth=1, borderColor=colors.grey)
    style_h2 = ParagraphStyle('H2', parent=styles['Heading2'], fontSize=16, textColor=COLOR_PRIMARY, spaceBefore=15)
    style_body = ParagraphStyle('Body', parent=styles['Normal'], fontSize=11, leading=15, spaceAfter=10)
    style_code = ParagraphStyle('Code', parent=styles['Code'], fontSize=9, leading=11, fontName='Courier', backColor=COLOR_CODE_BG, spaceAfter=0)

    style_table_header = ParagraphStyle('TableHeader', parent=styles['Normal'], fontSize=11, leading=13, textColor=colors.white, fontName='Helvetica-Bold')
    style_table_body = ParagraphStyle('TableBody', parent=styles['Normal'], fontSize=10, leading=12, textColor=colors.black)

    # --- COVER PAGE ---
    logo = get_optimized_image("icon.png", display_width=3*inch)
    if logo: story.append(logo)

    story.append(Spacer(1, 30))
    story.append(Paragraph("FurryOS", style_title))
    story.append(Paragraph("The Golden Master Handbook", style_h1))
    story.append(Paragraph(f"<b>Edition: {datetime.datetime.now().strftime('%Y-%m-%d')}</b>", style_body))
    story.append(Spacer(1, 20))

    collage = get_optimized_image("anthroheart_collage.png", display_width=7*inch, max_display_height=5*inch)
    if collage: story.append(collage)

    story.append(PageBreak())

    # --- CHAPTER 1: WELCOME ---
    story.append(Paragraph("Chapter 1: Welcome to the New Paradigm", style_h1))
    intro = """
    FurryOS is a philosophy given digital form. Built on the rock-solid foundation of Debian 13 "Trixie",
    it strips away corporate bloat and replaces it with specific, user-centric profiles.
    It adapts to you—whether you are a gamer seeking frames, a grandparent seeking simplicity, or a hacker seeking control.
    """
    story.append(Paragraph(intro, style_body))

    # Profiles Table
    story.append(Paragraph("The Four Modes", style_h2))

    raw_data = [
        ["Mode", "Target User", "Technical Impact"],
        ["🎮 Gamer", "Speed Demons", "Disables CUPS/Cron. Forces CPU to 'performance'. Max FPS."],
        ["👵 Granny", "Stability", "Locks Panel layout. Increases font size (DPI). Auto-updates."],
        ["🤖 Hacker", "Creators", "Installs build-essential, git, vim. Unlocks write access."],
        ["🕵️ Paranoid", "Privacy", "Deny-all Firewall. MAC Spoofing. RAM wipe on shutdown."]
    ]

    table_data = []
    table_data.append([Paragraph(cell, style_table_header) for cell in raw_data[0]])
    for row in raw_data[1:]:
        table_data.append([Paragraph(cell, style_table_body) for cell in row])

    t = Table(table_data, colWidths=[1.2*inch, 1.2*inch, 4.6*inch])
    t.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), COLOR_PRIMARY),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.grey),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('TOPPADDING', (0,0), (-1,-1), 6),
    ]))
    story.append(t)
    story.append(PageBreak())

    # --- CHAPTER 2: UNDER THE HOOD ---
    story.append(Paragraph("Chapter 2: Technical Specifications", style_h1))
    story.append(Paragraph("FurryOS is driven by a 'Genome' configuration file.", style_body))

    genome_content = read_file(os.path.join(CONFIG_DIR, 'GENOME.yaml'))
    if genome_content:
        story.append(Paragraph("System Genome (config/GENOME.yaml)", style_h2))
        code_blocks = process_yaml_for_pdf(genome_content, style_code)
        for block in code_blocks:
            story.append(block)

    story.append(PageBreak())

    # --- CHAPTER 3: THE SAGA ---
    story.append(Paragraph("Chapter 3: The AnthroHeart Saga", style_h1))
    story.append(Paragraph("The spirit behind the code.", style_body))

    trinity_img = get_optimized_image("AnthroHeart_Trinity.png", display_width=6*inch, max_display_height=5*inch)
    if trinity_img:
        story.append(trinity_img)
        story.append(Spacer(1, 15))

    saga_path = os.path.join(LORE_DIR, "Cio's AnthroHeart Saga FINAL.txt")
    saga_text = read_file(saga_path)

    if saga_text:
        paragraphs = saga_text.split('\n\n')
        count = 0
        for para in paragraphs:
            clean_para = para.replace("\n", " ").strip()
            if clean_para:
                story.append(Paragraph(clean_para, style_body))
                story.append(Spacer(1, 6))
                count += 1
                if count > 200:
                    story.append(Paragraph("<i>[...Full Saga text continues in /lore folder on the ISO...]</i>", style_body))
                    break

    story.append(PageBreak())

    # --- CHAPTER 4: THE WARLOCK NAME ---
    story.append(Paragraph("Chapter 4: The Warlock Name", style_h1))

    warlock_img = get_optimized_image("Warlock Cover Front.jpg", display_width=4*inch)
    if warlock_img:
        story.append(warlock_img)
        story.append(Spacer(1, 15))

    warlock_path = os.path.join(LORE_DIR, "The Warlock Name.txt")
    warlock_text = read_file(warlock_path)

    if warlock_text:
         story.append(Paragraph("A Legend of Power (Excerpt)", style_h2))
         story.append(Paragraph(warlock_text[:4000] + "...", style_body))
         story.append(Paragraph("<i>[Read the full novel in the /lore folder]</i>", style_body))

    story.append(PageBreak())

    # --- APPENDIX: GALLERY ---
    story.append(Paragraph("Appendix: Asset Gallery", style_h1))

    wall_dir = os.path.join(ASSETS_DIR, 'wallpapers')
    if os.path.exists(wall_dir):
        images = []
        for img_file in sorted(os.listdir(wall_dir))[:6]:
            if img_file.lower().endswith(('.png', '.jpg', '.jpeg')):
                img_obj = get_optimized_image(img_file, display_width=3*inch, max_display_height=2.5*inch)
                if img_obj: images.append(img_obj)

        if images:
            data = [images[i:i+2] for i in range(0, len(images), 2)]
            t = Table(data)
            story.append(t)

    doc.build(story, onFirstPage=header_footer, onLaterPages=header_footer)
    print(f"✅ Success! Handbook Created: {OUTPUT_PDF}")

if __name__ == "__main__":
    generate_handbook()

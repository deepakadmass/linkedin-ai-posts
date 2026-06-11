from PIL import Image, ImageDraw, ImageFont
import os
import random
from datetime import datetime

# ========== NO NEED TO EDIT ANYTHING HERE ==========
TEMPLATE_DIR = "templates"
DATA_DIR = "data"
OUTPUT_DIR = "outputs"

def load_commands(category):
    """Load commands from data file"""
    file_path = os.path.join(DATA_DIR, f"{category}.txt")
    if not os.path.exists(file_path):
        print(f"❌ Data file not found: {file_path}")
        return []
    
    with open(file_path, 'r') as f:
        lines = [x.strip() for x in f.readlines() if x.strip()]
    
    commands = []
    for line in lines[:5]:  # Max 5 commands
        if '|' in line:
            cmd, desc = line.split('|', 1)
            commands.append((cmd, desc))
    
    return commands

def generate_banner():
    """Auto generate banner for today's topic"""
    
    # Available categories (your templates)
    categories = ["linux", "aws", "security", "windows", "networking", "devops"]
    
    # Auto select based on day of week (Monday=linux, Tuesday=aws, etc)
    day_index = datetime.now().weekday()
    category = categories[day_index % len(categories)]
    
    # Load template
    template_path = os.path.join(TEMPLATE_DIR, f"{category}.png")
    if not os.path.exists(template_path):
        print(f"❌ Template not found: {template_path}")
        return None
    
    # Load commands for this category
    commands = load_commands(category)
    if not commands:
        print(f"❌ No commands found for {category}")
        return None
    
    # Open template
    img = Image.open(template_path)
    draw = ImageDraw.Draw(img)
    
    # Load font
    try:
        font_cmd = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 28)
        font_desc = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 22)
    except:
        font_cmd = ImageFont.load_default()
        font_desc = ImageFont.load_default()
    
    # ADJUST THESE COORDINATES FOR YOUR TEMPLATE
    # Y positions for each command (row 1 to 5)
    cmd_y_positions = [380, 470, 560, 650, 740]  # Adjust these numbers
    desc_y_positions = [415, 505, 595, 685, 775]  # Adjust these numbers
    
    # X position (left margin)
    cmd_x = 320   # Adjust this
    desc_x = 320  # Adjust this
    
    # Draw commands and descriptions
    for i, (cmd, desc) in enumerate(commands):
        # Draw command
        draw.text((cmd_x, cmd_y_positions[i]), cmd, fill=(0, 255, 0), font=font_cmd)
        # Draw description
        draw.text((desc_x, desc_y_positions[i]), desc, fill=(200, 200, 200), font=font_desc)
    
    # Save output
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d")
    output_path = os.path.join(OUTPUT_DIR, f"{category}_banner_{timestamp}.png")
    img.save(output_path)
    
    print(f"✅ Generated: {output_path}")
    print(f"📌 Category: {category.upper()}")
    return output_path

if __name__ == "__main__":
    generate_banner()

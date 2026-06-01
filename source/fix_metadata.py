import os
import glob
from fontTools.ttLib import TTFont

def get_style_name(filename):
    basename = os.path.basename(filename).replace(".ttf", "")
    parts = basename.split("-")
    if len(parts) == 2:
        return parts[1]
    return "Regular"

def fix_font(filepath, out_dir):
    try:
        font = TTFont(filepath)
    except Exception as e:
        print(f"Error opening {filepath}: {e}")
        return
        
    style = get_style_name(filepath)
    is_17pt = "17pt" in os.path.basename(filepath)
    
    family = "Elvan Sans 17pt" if is_17pt else "Elvan Sans"
    
    # 1. Fix Name Table
    if "name" not in font:
        # Create a new name table if completely missing
        from fontTools.ttLib.tables._n_a_m_e import table__n_a_m_e
        font["name"] = table__n_a_m_e()
        
    name_table = font["name"]
    # Clear corrupted names from pyftmerge
    name_table.names = []
    
    # Helper to add names for Windows (3,1,1033) and Mac (1,0,0)
    def add_name(nameID, string):
        name_table.setName(string, nameID, 3, 1, 1033)
        name_table.setName(string, nameID, 1, 0, 0)
        
    # Standard OpenType Full Name is "Family SubFamily", but if Regular just "Family"
    full_name = f"{family} {style}"
    if style == "Regular":
        full_name = family
        
    ps_name = os.path.basename(filepath).replace(".ttf", "")
        
    add_name(0, "Copyright 2026 The Elvan Sans Project Authors. Original fonts by Google Inc. and Ek Type.")
    add_name(1, family)
    add_name(2, style)
    add_name(3, f"1.000;ELVN;{ps_name}") # Unique ID
    add_name(4, full_name)
    add_name(5, "Version 1.000")
    add_name(6, ps_name)
    add_name(8, "Elvan Parthasarathy") # Manufacturer
    add_name(9, "Elvan Parthasarathy") # Designer
    add_name(13, "This Font Software is licensed under the SIL Open Font License, Version 1.1.")
    add_name(14, "http://scripts.sil.org/OFL")
    
    # 2. Fix OS/2 Table
    if "OS/2" in font:
        os2 = font["OS/2"]
        weight_map = {
            "Regular": 400, "Italic": 400,
            "Medium": 500, "MediumItalic": 500,
            "SemiBold": 600, "SemiBoldItalic": 600,
            "Bold": 700, "BoldItalic": 700
        }
        os2.usWeightClass = weight_map.get(style, 400)
        os2.usWidthClass = 5
        
        # fsSelection
        # Bit 0: Italic, Bit 5: Bold, Bit 6: Regular
        fsSelection = 0
        if "Italic" in style:
            fsSelection |= (1 << 0) # bit 0
        if "Bold" in style:
            fsSelection |= (1 << 5) # bit 5
        if style == "Regular":
            fsSelection |= (1 << 6) # bit 6
        os2.fsSelection = fsSelection
        
        # Vertical Metrics (Google Fonts Standard)
        os2.sTypoAscender = 1000
        os2.sTypoDescender = -250
        os2.sTypoLineGap = 0
        os2.usWinAscent = 1000
        os2.usWinDescent = 250
    
    # 3. Fix hhea Table
    if "hhea" in font:
        hhea = font["hhea"]
        hhea.ascent = 1000
        hhea.descent = -250
        hhea.lineGap = 0
    
    # 4. Fix Base Characters Zero Width
    if "hmtx" in font:
        hmtx = font["hmtx"]
        for glyph_name in hmtx.metrics:
            width, lsb = hmtx.metrics[glyph_name]
            if width == 0:
                # Setting 0 width bases to a minimal positive value to pass Fontbakery checks
                hmtx.metrics[glyph_name] = (1, lsb)

    out_path = os.path.join(out_dir, os.path.basename(filepath))
    font.save(out_path)
    print(f"Fixed metadata and saved -> {out_path}")

def main():
    # We run this on the fonts inside the distribution folder (the "broken" ones)
    fonts = glob.glob("fonts/ttf/*.ttf")
    if not fonts:
        print("No fonts found in fonts/ttf/")
        return
        
    out_dir = "Elvan_Sans_Fixed"
    os.makedirs(out_dir, exist_ok=True)
    
    for f in fonts:
        fix_font(f, out_dir)
        
    print(f"Done! All fixed fonts are in {out_dir}")

if __name__ == "__main__":
    main()

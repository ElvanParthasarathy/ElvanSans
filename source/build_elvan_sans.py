import os
import sys
import subprocess
from fontTools.ttLib import TTFont
import math
import fontTools.ttLib.tables._g_l_y_f

def run_cmd(cmd):
    print(f"Running: {' '.join(cmd)}")
    subprocess.run(cmd, check=True)

def skew_font(font_path, output_path, angle_degrees=10):
    font = TTFont(font_path)
    shear = math.tan(math.radians(angle_degrees))
    glyf = font['glyf']
    
    for glyph_name in glyf.keys():
        glyph = glyf[glyph_name]
        if glyph.isComposite():
            for component in glyph.components:
                if hasattr(component, 'x') and hasattr(component, 'y'):
                    component.x = int(round(component.x + component.y * shear))
        else:
            if hasattr(glyph, 'coordinates'):
                new_coords = []
                for x, y in glyph.coordinates:
                    new_x = int(round(x + y * shear))
                    new_coords.append((new_x, y))
                glyph.coordinates = fontTools.ttLib.tables._g_l_y_f.GlyphCoordinates(new_coords)
        glyph.recalcBounds(glyf)
        
    if 'post' in font:
        font['post'].italicAngle = -angle_degrees
    if 'hhea' in font:
        font['hhea'].caretSlopeRun = int(round(font['hhea'].caretSlopeRise * shear))
    if 'OS/2' in font:
        font['OS/2'].fsSelection |= (1 << 0) # set italic
        font['OS/2'].fsSelection &= ~(1 << 6) # unset regular
    font.save(output_path)

def finalize_font(font_path, new_family_name, style_name):
    print(f"Finalizing {font_path} to {new_family_name} {style_name}")
    font = TTFont(font_path)
    
    # 1. Rename
    name_table = font['name']
    full_name = f"{new_family_name} {style_name}"
    postscript_name = f"{new_family_name.replace(' ', '')}-{style_name.replace(' ', '')}"
    
    # Determine RBIZ base family and style for MS Word grouping
    rbiz_styles = ["Regular", "Italic", "Bold", "BoldItalic", "Bold Italic"]
    if style_name in rbiz_styles:
        nameID_1 = new_family_name
        nameID_2 = style_name.replace("BoldItalic", "Bold Italic")
    else:
        # It's an extended weight like Medium or SemiBold
        if "Italic" in style_name:
            weight_part = style_name.replace("Italic", "").strip()
            nameID_1 = f"{new_family_name} {weight_part}"
            nameID_2 = "Italic"
        else:
            nameID_1 = f"{new_family_name} {style_name}"
            nameID_2 = "Regular"
            
    nameID_16 = new_family_name
    nameID_17 = style_name
    
    for record in name_table.names:
        if record.nameID == 0:
            record.string = "Copyright 2026 Elvan Parthasarathy. Based on Google Sans and Mukta Malar (SIL Open Font License).".encode(record.getEncoding())
        elif record.nameID == 1:
            record.string = nameID_1.encode(record.getEncoding())
        elif record.nameID == 2:
            record.string = nameID_2.encode(record.getEncoding())
        elif record.nameID == 3 or record.nameID == 4:
            record.string = full_name.encode(record.getEncoding())
        elif record.nameID == 6:
            record.string = postscript_name.encode(record.getEncoding())
        elif record.nameID == 7:
            record.string = "".encode(record.getEncoding())
        elif record.nameID == 8 or record.nameID == 9:
            record.string = "Elvan Parthasarathy".encode(record.getEncoding())
        elif record.nameID == 10:
            record.string = "Elvan Sans is a composite font created by Elvan Parthasarathy, combining Google Sans and Mukta Malar under the SIL Open Font License.".encode(record.getEncoding())
        elif record.nameID == 11 or record.nameID == 12:
            record.string = "https://github.com/ElvanParthasarathy".encode(record.getEncoding())
        elif record.nameID == 13:
            record.string = "This Font Software is licensed under the SIL Open Font License, Version 1.1. This font is a composite of Google Sans and Mukta Malar.".encode(record.getEncoding())
        elif record.nameID == 16:
            record.string = nameID_16.encode(record.getEncoding())
        elif record.nameID == 17:
            record.string = nameID_17.encode(record.getEncoding())
            
    is_italic = "Italic" in style_name
    is_bold = "Bold" in style_name
    if 'head' in font:
        if is_italic:
            font['head'].macStyle |= (1 << 1)
        else:
            font['head'].macStyle &= ~(1 << 1)
        if is_bold:
            font['head'].macStyle |= (1 << 0)
        else:
            font['head'].macStyle &= ~(1 << 0)
            
    # 2. Fix Metrics (Mukta Malar: Ascent 1130, Descent 532)
    if 'OS/2' in font:
        os2 = font['OS/2']
        os2.usWinAscent = 1130
        os2.usWinDescent = 532
        
        # Enforce OS/2 selection bits
        os2.fsSelection &= ~((1 << 0) | (1 << 5) | (1 << 6))
        if is_italic: os2.fsSelection |= (1 << 0)
        if is_bold: os2.fsSelection |= (1 << 5)
        if not is_italic and not is_bold: os2.fsSelection |= (1 << 6)
        
        # 3. Fix Unicode Ranges for MS Word
        # Bit 15: Devanagari, 16: Bengali, 17: Gurmukhi, 18: Gujarati, 19: Oriya, 20: Tamil, 21: Telugu, 22: Kannada, 23: Malayalam
        os2.ulUnicodeRange1 |= (1 << 15) | (1 << 16) | (1 << 17) | (1 << 18) | (1 << 19) | (1 << 20) | (1 << 21) | (1 << 22) | (1 << 23)
            
    font.save(font_path)

def main():
    out_dir = "Elvan_Sans_Output"
    os.makedirs(out_dir, exist_ok=True)
    temp_dir = "temp_fonts"
    os.makedirs(temp_dir, exist_ok=True)
    
    non_tamil_range = "U+0000-0B7F,U+0C00-11FBF,U+12000-10FFFF"
    tamil_only_range = "U+0B80-0BFF,U+200C,U+200D,U+25CC"
    
    google_fonts_dir = "Google_Sans/static"
    for filename in os.listdir(google_fonts_dir):
        if not filename.endswith(".ttf"):
            continue
            
        name_part = filename.replace(".ttf", "")
        if "-" in name_part:
            family_prefix, style = name_part.split("-", 1)
        else:
            family_prefix = "GoogleSans"
            style = "Regular"
            
        # Map style to Mukta Malar weight
        mukta_weight = "Regular"
        if "ExtraBold" in style:
            mukta_weight = "ExtraBold"
        elif "SemiBold" in style:
            mukta_weight = "SemiBold"
        elif "Bold" in style:
            mukta_weight = "Bold"
        elif "Medium" in style:
            mukta_weight = "Medium"
        elif "ExtraLight" in style:
            mukta_weight = "ExtraLight"
        elif "Light" in style:
            mukta_weight = "Light"
            
        is_italic = "Italic" in style
        if style == "Italic":
            mukta_weight = "Regular"
            
        is_17pt = "17pt" in family_prefix
        new_family = "Elvan Sans 17pt" if is_17pt else "Elvan Sans"
        new_filename = f"ElvanSans{'17pt' if is_17pt else ''}-{style}.ttf"
        
        print(f"\n--- Processing {filename} ({new_family} {style}) ---")
        
        google_font = os.path.join(google_fonts_dir, filename)
        mukta_font = f"Mukta_Malar/MuktaMalar-{mukta_weight}.ttf"
        
        if not os.path.exists(mukta_font):
            print(f"Missing {mukta_font}, using Regular instead.")
            mukta_font = "Mukta_Malar/MuktaMalar-Regular.ttf"
            
        # Process Mukta - Skew if italic, otherwise use untouched
        mukta_processed = mukta_font
        if is_italic:
            mukta_processed = os.path.join(temp_dir, f"MuktaMalar-{mukta_weight}-Italic.ttf")
            if not os.path.exists(mukta_processed):
                skew_font(mukta_font, mukta_processed, 10.0)
                
        google_subset = os.path.join(temp_dir, f"{name_part}.subset.ttf")
        mukta_subset = os.path.join(temp_dir, f"MuktaMalar-{mukta_weight}-subset.ttf")
        merged_font = os.path.join(out_dir, new_filename)
        
        # 1. Isolate Google Sans: Strip Tamil unicodes and EXCLUDE Tamil layout scripts
        run_cmd([
            sys.executable, "-m", "fontTools.subset", google_font,
            f"--unicodes={non_tamil_range}",
            "--layout-features=*",
            "--layout-scripts=*,-taml,-tml2",
            "--glyph-names", "--symbol-cmap", "--legacy-cmap",
            "--notdef-glyph", "--notdef-outline", "--recommended-glyphs",
            "--name-IDs=*", "--name-legacy", "--name-languages=*",
            f"--output-file={google_subset}"
        ])
        
        # 2. Isolate Mukta Malar: Keep ONLY Tamil unicodes and ONLY Tamil layout scripts
        run_cmd([
            sys.executable, "-m", "fontTools.subset", mukta_processed,
            f"--unicodes={tamil_only_range}",
            "--layout-features=*",
            "--layout-scripts=taml,tml2",
            "--glyph-names", "--symbol-cmap", "--legacy-cmap",
            "--notdef-glyph", "--notdef-outline", "--recommended-glyphs",
            "--name-IDs=*", "--name-legacy", "--name-languages=*",
            f"--output-file={mukta_subset}"
        ])
        
        # 3. Merge clean subsets
        run_cmd([
            sys.executable, "-m", "fontTools.merge",
            google_subset,
            mukta_subset,
            f"--output-file={merged_font}"
        ])
        
        # 4. Finalize naming and metadata
        finalize_font(merged_font, new_family, style)
        
    print("\nDone! All variations processed.")

if __name__ == "__main__":
    main()

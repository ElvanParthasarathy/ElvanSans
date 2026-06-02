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

def rename_font(font_path, new_family_name, style_name):
    print(f"Renaming {font_path} to {new_family_name} {style_name}")
    font = TTFont(font_path)
    name_table = font['name']
    
    full_name = f"{new_family_name} {style_name}"
    postscript_name = f"{new_family_name.replace(' ', '')}-{style_name.replace(' ', '')}"
    
    for record in name_table.names:
        if record.nameID == 1 or record.nameID == 16:
            record.string = new_family_name.encode(record.getEncoding())
        elif record.nameID == 2 or record.nameID == 17:
            record.string = style_name.encode(record.getEncoding())
        elif record.nameID == 3 or record.nameID == 4:
            record.string = full_name.encode(record.getEncoding())
        elif record.nameID == 6:
            record.string = postscript_name.encode(record.getEncoding())
            
    font.save(font_path)

def main():
    out_dir = "Elvan_Sans_Output"
    os.makedirs(out_dir, exist_ok=True)
    temp_dir = "temp_fonts"
    os.makedirs(temp_dir, exist_ok=True)
    
    non_tamil_range = "U+0000-0B7F,U+0C00-11FBF,U+12000-10FFFF"
    
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
        if "Bold" in style:
            mukta_weight = "Bold"
        elif "SemiBold" in style:
            mukta_weight = "SemiBold"
        elif "Medium" in style:
            mukta_weight = "Medium"
        elif "ExtraLight" in style:
            mukta_weight = "ExtraLight"
        elif "Light" in style:
            mukta_weight = "Light"
        elif "ExtraBold" in style:
            mukta_weight = "ExtraBold"
            
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
        merged_font = os.path.join(out_dir, new_filename)
        
        # Strip Tamil rules from Google Sans
        run_cmd([
            sys.executable, "-m", "fontTools.subset", google_font,
            f"--unicodes={non_tamil_range}",
            "--layout-features=*",
            "--layout-scripts=*",
            "--glyph-names", "--symbol-cmap", "--legacy-cmap",
            "--notdef-glyph", "--notdef-outline", "--recommended-glyphs",
            "--name-IDs=*", "--name-legacy", "--name-languages=*",
            f"--output-file={google_subset}"
        ])
        
        # Merge subsetted Google Sans with UN-SUBSETTED Mukta Malar
        run_cmd([
            sys.executable, "-m", "fontTools.merge",
            google_subset,
            mukta_processed,
            f"--output-file={merged_font}"
        ])
        
        rename_font(merged_font, new_family, style)
        
    print("\nDone! All variations processed.")

if __name__ == "__main__":
    main()

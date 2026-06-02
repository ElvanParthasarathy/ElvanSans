import os
import glob
import shutil
from fontTools.ttLib import TTFont

def main():
    root_dir = r"d:\Projects\Elvan Sans"
    fonts_dir = os.path.join(root_dir, "fonts", "ttf")
    backup_dir = os.path.join(root_dir, "fonts", "ttf_backup")
    
    print(f"Backing up current fonts to {backup_dir}...")
    os.makedirs(backup_dir, exist_ok=True)
    
    ttf_files = glob.glob(os.path.join(fonts_dir, "*.ttf"))
    
    for font_path in ttf_files:
        filename = os.path.basename(font_path)
        backup_path = os.path.join(backup_dir, filename)
        
        # Backup the file first
        shutil.copy2(font_path, backup_path)
        print(f"Backed up {filename}")
        
    print("\nFixing Android metrics...")
    for font_path in ttf_files:
        filename = os.path.basename(font_path)
        print(f"Processing {filename}...")
        
        font = TTFont(font_path)
        
        # 1. Recalculate Bounding Boxes (head table xMin, xMax, yMin, yMax)
        xMin = 32767
        yMin = 32767
        xMax = -32768
        yMax = -32768
        
        if 'glyf' in font:
            glyf = font['glyf']
            for glyph_name in glyf.keys():
                glyph = glyf[glyph_name]
                # Safely get bounds
                try:
                    glyph.recalcBounds(glyf)
                    if hasattr(glyph, 'xMin'):
                        xMin = min(xMin, glyph.xMin)
                        yMin = min(yMin, glyph.yMin)
                        xMax = max(xMax, glyph.xMax)
                        yMax = max(yMax, glyph.yMax)
                except Exception as e:
                    pass
                
        if 'head' in font and xMin != 32767:
            font['head'].xMin = xMin
            font['head'].yMin = yMin
            font['head'].xMax = xMax
            font['head'].yMax = yMax
            
        # 2. Recalculate advanceWidthMax (hhea table)
        if 'hmtx' in font and 'hhea' in font:
            hmtx = font['hmtx']
            max_aw = max([metrics[0] for metrics in hmtx.metrics.values()])
            font['hhea'].advanceWidthMax = max_aw
            
            # 3. Sync Vertical Metrics for Android / Apple
            font['hhea'].ascent = yMax
            font['hhea'].descent = yMin
            font['hhea'].lineGap = 0
            
        # 4. Sync OS/2 Typo Metrics for universal agreement
        if 'OS/2' in font:
            os2 = font['OS/2']
            os2.sTypoAscender = yMax
            os2.sTypoDescender = yMin
            os2.sTypoLineGap = 0
            os2.usWinAscent = yMax
            os2.usWinDescent = abs(yMin)
            
        font.save(font_path)
        print(f"  Fixed metrics for {filename}: xMax={xMax}, advanceWidthMax={font['hhea'].advanceWidthMax}")

    print("\nAll fonts have been successfully updated with proper Android bounds!")

if __name__ == "__main__":
    main()

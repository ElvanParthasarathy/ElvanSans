import glob
from fontTools.ttLib import TTFont
from fontTools.ttLib.tables._c_m_a_p import cmap_format_4

def main():
    fonts = glob.glob("fonts/ttf/*.ttf")
    for f in fonts:
        print(f"Fixing cmap for {f}...")
        font = TTFont(f)
        
        # Check if 0 3 already exists
        has_0_3 = any(t.platformID == 0 and t.platEncID == 3 for t in font['cmap'].tables)
        if not has_0_3:
            # Find 3 1
            cmap_3_1 = None
            for t in font['cmap'].tables:
                if t.platformID == 3 and t.platEncID == 1:
                    cmap_3_1 = t
                    break
                    
            if cmap_3_1:
                new_table = cmap_format_4(4)
                new_table.platformID = 0
                new_table.platEncID = 3
                new_table.language = 0
                new_table.cmap = cmap_3_1.cmap
                font['cmap'].tables.append(new_table)
                font.save(f)
                
    print("Done! Added cmap 0 3 to all fonts.")

if __name__ == "__main__":
    main()

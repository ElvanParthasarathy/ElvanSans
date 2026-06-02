import glob
from fontTools.ttLib import TTFont

def main():
    fonts = glob.glob("fonts/ttf/*.ttf")
    for f in fonts:
        print(f"Fixing GSUB in {f}...")
        font = TTFont(f)
        
        if 'GSUB' not in font:
            continue
            
        gsub = font['GSUB'].table
        modified = False
        
        for lookup in gsub.LookupList.Lookup:
            for st in lookup.SubTable:
                if hasattr(st, 'mapping'):
                    # It's a SingleSubst table
                    keys_to_delete = []
                    for in_glyph, out_glyph in st.mapping.items():
                        if isinstance(out_glyph, str) and out_glyph.endswith('.1'):
                            keys_to_delete.append(in_glyph)
                        elif isinstance(out_glyph, list) and any(g.endswith('.1') for g in out_glyph):
                            st.mapping[in_glyph] = [g for g in out_glyph if not g.endswith('.1')]
                            if len(st.mapping[in_glyph]) == 0:
                                keys_to_delete.append(in_glyph)
                            modified = True
                    
                    for k in keys_to_delete:
                        del st.mapping[k]
                        modified = True
                        
                elif hasattr(st, 'alternates'):
                    # It's an AlternateSubst table
                    keys_to_delete = []
                    for in_glyph, out_glyphs in st.alternates.items():
                        # If any alternate is a .1 glyph, filter it out
                        filtered = [g for g in out_glyphs if not g.endswith('.1')]
                        if len(filtered) == 0:
                            keys_to_delete.append(in_glyph)
                        elif len(filtered) != len(out_glyphs):
                            st.alternates[in_glyph] = filtered
                            modified = True
                            
                    for k in keys_to_delete:
                        del st.alternates[k]
                        modified = True
        
        if modified:
            font.save(f)
            
    print("Done stripping broken .1 GSUB rules!")

if __name__ == "__main__":
    main()

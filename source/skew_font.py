import math
from fontTools.ttLib import TTFont

def skew_font(font_path, output_path, angle_degrees=10):
    print(f"Skewing {font_path} by {angle_degrees} degrees")
    font = TTFont(font_path)
    
    # Calculate shear factor
    # A right-leaning italic has a positive shear factor
    shear = math.tan(math.radians(angle_degrees))
    
    glyf = font['glyf']
    
    for glyph_name in glyf.keys():
        glyph = glyf[glyph_name]
        
        # If it's a simple glyph
        if glyph.isComposite():
            # For composite glyphs, we need to shear the offset
            # the components themselves will be sheared because they reference simple glyphs
            for component in glyph.components:
                if hasattr(component, 'x') and hasattr(component, 'y'):
                    component.x = int(round(component.x + component.y * shear))
        else:
            # Simple glyph
            if hasattr(glyph, 'coordinates'):
                new_coords = []
                for x, y in glyph.coordinates:
                    new_x = int(round(x + y * shear))
                    new_coords.append((new_x, y))
                glyph.coordinates = fontTools.ttLib.tables._g_l_y_f.GlyphCoordinates(new_coords)
                
        # Recalculate bounds
        glyph.recalcBounds(glyf)
        
    # Update post table
    if 'post' in font:
        font['post'].italicAngle = -angle_degrees
        
    # Update hhea table caret slope
    if 'hhea' in font:
        font['hhea'].caretSlopeRun = int(round(font['hhea'].caretSlopeRise * shear))
        
    # Update OS/2 table to mark as italic
    if 'OS/2' in font:
        font['OS/2'].fsSelection |= (1 << 0) # set italic bit
        
    font.save(output_path)
    print(f"Saved skewed font to {output_path}")

if __name__ == "__main__":
    import sys
    import fontTools
    skew_font(sys.argv[1], sys.argv[2], float(sys.argv[3]))

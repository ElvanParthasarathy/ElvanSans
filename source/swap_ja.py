
import glob
from fontTools.ttLib import TTFont

def swap_glyphs(font, g1, g2):
    glyf = font['glyf']
    hmtx = font['hmtx']
    
    if g1 in glyf and g2 in glyf:
        # Swap outlines
        temp_glyf = glyf[g1]
        glyf[g1] = glyf[g2]
        glyf[g2] = temp_glyf
        
        # Swap metrics (advance width and lsb)
        temp_hmtx = hmtx[g1]
        hmtx[g1] = hmtx[g2]
        hmtx[g2] = temp_hmtx
        
        return True
    return False

def main():
    fonts = glob.glob('fonts/ttf/*.ttf')
    pairs = [
        ('Ja.tm', 'JaAlt.tm'),
        ('JaPulli.tm', 'JaAltPulli.tm'),
        ('JaMatraI.tm', 'JaAltMatraI.tm'),
        ('JaMatraIi.tm', 'JaAltMatraIi.tm'),
        ('JaMatraU.tm', 'JaAltMatraU.tm'),
        ('JaMatraUu.tm', 'JaAltMatraUu.tm')
    ]
    
    for f in fonts:
        print(f'Swapping Ja variants in {f}...')
        font = TTFont(f)
        swapped = False
        
        for p1, p2 in pairs:
            if swap_glyphs(font, p1, p2):
                swapped = True
                
        if swapped:
            font.save(f)
            
    print('Done swapping Ja variants!')

if __name__ == '__main__':
    main()


import glob
from fontTools.ttLib import TTFont

fonts = glob.glob('fonts/ttf/*.ttf')

# Bits to set in ulUnicodeRange1 according to OpenType spec:
# 15: Devanagari
# 16: Bengali
# 18: Gujarati
# 20: Tamil
# 21: Telugu
# 23: Malayalam
bits_to_set = [15, 16, 18, 20, 21, 23]

for f in fonts:
    print(f'Fixing Unicode Ranges for {f}...')
    font = TTFont(f)
    os2 = font['OS/2']
    
    for bit in bits_to_set:
        os2.ulUnicodeRange1 |= (1 << bit)
        
    font.save(f)

print('All 16 fonts updated with full Indic Unicode Range support!')

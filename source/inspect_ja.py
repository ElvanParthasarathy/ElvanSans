
from fontTools.ttLib import TTFont

font_elvan = TTFont('fonts/ttf/ElvanSans-Regular.ttf')
font_google = TTFont('source/Google_Sans/static/GoogleSans-Regular.ttf')

cmap_g = font_google.getBestCmap()
ja_m = cmap_g.get(0x0D1C)
print('Malayalam Ja glyph in Google Sans:', ja_m)

for g in ['Ja.tm', 'JaAlt.tm', 'JaMatraI.tm', 'JaAltMatraI.tm', 'JaPulli.tm']:
    if g in font_elvan['glyf']:
        glyf = font_elvan['glyf'][g]
        print(f'{g} is composite:', glyf.isComposite())
        if glyf.isComposite():
            print(f'  Components: {[c.glyphName for c in glyf.components]}')

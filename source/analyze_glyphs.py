
from fontTools.ttLib import TTFont

f1 = TTFont('source/Google_Sans/static/GoogleSans-Regular.ttf')
f2 = TTFont('fonts/ttf/ElvanSans-Regular.ttf')

print(f'Google Sans glyphs: {len(f1.getGlyphOrder())}')
print(f'Elvan Sans glyphs: {len(f2.getGlyphOrder())}')

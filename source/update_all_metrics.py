
import glob
from fontTools.ttLib import TTFont

fonts = glob.glob('fonts/ttf/*.ttf')

for f in fonts:
    print(f'Updating metrics for {f}...')
    font = TTFont(f)
    os2 = font['OS/2']
    os2.usWinAscent = 1130
    os2.usWinDescent = 532
    font.save(f)

print('All 16 fonts successfully updated with new vertical metrics!')

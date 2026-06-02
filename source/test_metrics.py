
from fontTools.ttLib import TTFont

print('Loading fonts...')
elvan = TTFont('fonts/ttf/ElvanSans-Regular.ttf')
mukta = TTFont('source/Mukta_Malar/MuktaMalar-Regular.ttf')

# Get Mukta Malar metrics
mukta_os2 = mukta['OS/2']
mukta_hhea = mukta['hhea']
win_ascent = mukta_os2.usWinAscent
win_descent = mukta_os2.usWinDescent

print(f'Mukta Malar WinAscent: {win_ascent}, WinDescent: {win_descent}')

# Apply to Elvan Sans
elvan_os2 = elvan['OS/2']
print(f'Old Elvan WinAscent: {elvan_os2.usWinAscent}, WinDescent: {elvan_os2.usWinDescent}')
elvan_os2.usWinAscent = win_ascent
elvan_os2.usWinDescent = win_descent

# Save test font
import os
os.makedirs('tests', exist_ok=True)
elvan.save('tests/test_metrics.ttf')
print('Saved test font to tests/test_metrics.ttf')

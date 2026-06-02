
from fontTools.ttLib import TTFont

def analyze_os2(font_path):
    print(f'\\n--- Analyzing OS/2 in {font_path} ---')
    font = TTFont(font_path)
    os2 = font['OS/2']
    print(f'ulUnicodeRange1: {bin(os2.ulUnicodeRange1)}')
    print(f'ulCodePageRange1: {bin(os2.ulCodePageRange1)}')
    print(f'ulCodePageRange2: {bin(os2.ulCodePageRange2)}')
    
analyze_os2('source/Google_Sans/static/GoogleSans-Regular.ttf')
analyze_os2('source/Mukta_Malar/MuktaMalar-Regular.ttf')
analyze_os2('fonts/ttf/ElvanSans-Regular.ttf')

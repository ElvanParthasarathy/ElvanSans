
from fontTools.ttLib import TTFont

def analyze_gdef(font_path):
    print(f'\\n--- GDEF in {font_path} ---')
    font = TTFont(font_path)
    if 'GDEF' not in font:
        print('NO GDEF TABLE!')
        return
        
    gdef = font['GDEF'].table
    if hasattr(gdef, 'GlyphClassDef') and gdef.GlyphClassDef:
        print(f'GlyphClassDef classes: {len(gdef.GlyphClassDef.classDefs)}')
    else:
        print('No GlyphClassDef')
        
    if hasattr(gdef, 'MarkAttachClassDef') and gdef.MarkAttachClassDef:
        print(f'MarkAttachClassDef classes: {len(gdef.MarkAttachClassDef.classDefs)}')
    else:
        print('No MarkAttachClassDef')

analyze_gdef('source/Google_Sans/static/GoogleSans-Regular.ttf')
analyze_gdef('temp_fonts/GoogleSans-Regular.subset.ttf')
analyze_gdef('source/Mukta_Malar/MuktaMalar-Regular.ttf')
analyze_gdef('fonts/ttf/ElvanSans-Regular.ttf')

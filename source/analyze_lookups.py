
from fontTools.ttLib import TTFont

def analyze_font(font_path):
    print(f'\\n--- {font_path} ---')
    font = TTFont(font_path)
    if 'GSUB' not in font:
        print('No GSUB')
        return
    gsub = font['GSUB'].table
    print(f'Total Lookups: {len(gsub.LookupList.Lookup)}')
    
    # Check features for a script like mlym (Malayalam)
    found_mlym = False
    for script_rec in gsub.ScriptList.ScriptRecord:
        if script_rec.ScriptTag in ('mlym', 'mlm2'):
            found_mlym = True
            script = script_rec.Script
            if script.DefaultLangSys:
                features = script.DefaultLangSys.FeatureIndex
                print(f'{script_rec.ScriptTag} has {len(features)} features')
    if not found_mlym:
        print('No Malayalam script found!')

analyze_font('source/Google_Sans/static/GoogleSans-Regular.ttf')
analyze_font('fonts/ttf/ElvanSans-Regular.ttf')

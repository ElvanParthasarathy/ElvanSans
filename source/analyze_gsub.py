
from fontTools.ttLib import TTFont

def analyze(font_path):
    print(f'\\n--- Analyzing {font_path} ---')
    font = TTFont(font_path)
    if 'GSUB' not in font:
        print('No GSUB table!')
        return
        
    gsub = font['GSUB'].table
    if not hasattr(gsub, 'ScriptList') or not gsub.ScriptList:
        print('No ScriptList!')
        return
        
    for script_rec in gsub.ScriptList.ScriptRecord:
        script_tag = script_rec.ScriptTag
        print(f'Script: {script_tag}')
        if script_tag in ('taml', 'tml2', 'mlym', 'mlm2'):
            script = script_rec.Script
            if script.DefaultLangSys:
                feature_indices = script.DefaultLangSys.FeatureIndex
                print(f'  DefaultLangSys has {len(feature_indices)} features')
            if script.LangSysRecord:
                for lang_rec in script.LangSysRecord:
                    print(f'  LangSys {lang_rec.LangSysTag} has {len(lang_rec.LangSys.FeatureIndex)} features')

analyze('source/Google_Sans/static/GoogleSans-Regular.ttf')
analyze('source/Mukta_Malar/MuktaMalar-Regular.ttf')
analyze('fonts/ttf/ElvanSans-Regular.ttf')

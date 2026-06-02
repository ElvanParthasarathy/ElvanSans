
import os
from fontTools.ttLib import TTFont

subset_path = 'temp_fonts/GoogleSans-Regular.subset.ttf'
if os.path.exists(subset_path):
    print('Found subsetted Google Sans!')
    font = TTFont(subset_path)
    gsub = font['GSUB'].table
    for script_rec in gsub.ScriptList.ScriptRecord:
        if script_rec.ScriptTag in ('taml', 'tml2'):
            print(f'Subsetted Google Sans still has {script_rec.ScriptTag} script!')
            script = script_rec.Script
            if script.DefaultLangSys:
                print(f'  Features: {len(script.DefaultLangSys.FeatureIndex)}')
else:
    print('Subsetted font not found.')

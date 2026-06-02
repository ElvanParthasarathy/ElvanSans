
from fontTools.ttLib import TTFont

font = TTFont('source/Google_Sans/static/GoogleSans-Regular.ttf')
gsub = font['GSUB'].table

dot1_count = 0
for lookup in gsub.LookupList.Lookup:
    for st in lookup.SubTable:
        if hasattr(st, 'mapping'):
            for in_g, out_g in st.mapping.items():
                if isinstance(out_g, str) and out_g.endswith('.1'):
                    dot1_count += 1
        elif hasattr(st, 'alternates'):
            for in_g, out_glyphs in st.alternates.items():
                if any(g.endswith('.1') for g in out_glyphs):
                    dot1_count += 1

print(f'Google Sans GSUB uses .1 glyphs in {dot1_count} substitution rules!')

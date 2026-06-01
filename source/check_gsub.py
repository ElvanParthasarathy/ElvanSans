from fontTools.ttLib import TTFont

font = TTFont('fonts/ttf/ElvanSans-Regular.ttf')
gsub = font['GSUB'].table

for i, feature in enumerate(gsub.FeatureList.FeatureRecord):
    tag = feature.FeatureTag
    feature_table = feature.Feature
    
    for lookup_index in feature_table.LookupListIndex:
        lookup = gsub.LookupList.Lookup[lookup_index]
        for st in lookup.SubTable:
            if hasattr(st, 'mapping') and 'a' in st.mapping:
                if st.mapping['a'] == 'a.1':
                    print(f"Feature '{tag}' replaces 'a' with 'a.1'")

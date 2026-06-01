import os
import shutil

def main():
    base_dir = r"d:\Projects\Elvan Sans"
    src_dir = os.path.join(base_dir, "Elvan_Sans_Output")
    dist_dir = os.path.join(base_dir, "Elvan_Sans_Distribution")
    
    ttf_dir = os.path.join(dist_dir, "fonts", "ttf")
    os.makedirs(ttf_dir, exist_ok=True)
    
    # 1. Move fonts
    for filename in os.listdir(src_dir):
        if filename.endswith(".ttf"):
            src_file = os.path.join(src_dir, filename)
            dst_file = os.path.join(ttf_dir, filename)
            shutil.copy2(src_file, dst_file)
            
    # 2. Move OFL.txt
    ofl_src = os.path.join(src_dir, "OFL.txt")
    ofl_dst = os.path.join(dist_dir, "OFL.txt")
    if os.path.exists(ofl_src):
        shutil.copy2(ofl_src, ofl_dst)
        
    # 3. Create README.md
    readme_path = os.path.join(dist_dir, "README.md")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write("""# Elvan Sans

Elvan Sans is a modern, versatile typeface designed for seamless typography and excellent readability across digital platforms. It provides extensive support for both English (Latin) and Tamil scripts.

## History and Motivation
Elvan Sans was created by Elvan Parthasarathy as a derivative work to solve Tamil rendering and shaping issues found in existing open-source fonts. It seamlessly integrates the highly legible Tamil character set from **Mukta Malar** with the clean, geometric Latin design of **Google Sans**, producing a unified, professional typeface where both scripts match perfectly in weight and style.

## Styles
The Elvan Sans family includes 16 styles:
* Regular, Italic
* Medium, Medium Italic
* SemiBold, SemiBold Italic
* Bold, Bold Italic
(Along with 17pt optical size variants for each)

## License
Elvan Sans is licensed under the SIL Open Font License v1.1 (http://scripts.sil.org/OFL).
See `OFL.txt` for details.
""")

    # 4. Create DESCRIPTION.en_us.html for Google Fonts
    desc_path = os.path.join(dist_dir, "DESCRIPTION.en_us.html")
    with open(desc_path, "w", encoding="utf-8") as f:
        f.write("""<p>
  Elvan Sans is a modern typeface designed by Elvan Parthasarathy. It was created to provide a seamless, highly readable typographic experience for both English and Tamil readers.
</p>
<p>
  By combining geometric Latin proportions with expertly crafted Tamil letterforms, Elvan Sans ensures that multi-lingual text looks unified and professional. It features perfect weight-matching across both scripts, resolving common shaping and layout issues in digital typography.
</p>
""")

    # 5. Create basic METADATA.pb
    meta_path = os.path.join(dist_dir, "METADATA.pb")
    with open(meta_path, "w", encoding="utf-8") as f:
        f.write("""name: "Elvan Sans"
designer: "Elvan Parthasarathy"
license: "OFL"
category: "SANS_SERIF"
date_added: "2026-06-01"
fonts {
  name: "Elvan Sans"
  style: "normal"
  weight: 400
  filename: "fonts/ttf/ElvanSans-Regular.ttf"
  post_script_name: "ElvanSans-Regular"
  full_name: "Elvan Sans Regular"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "italic"
  weight: 400
  filename: "fonts/ttf/ElvanSans-Italic.ttf"
  post_script_name: "ElvanSans-Italic"
  full_name: "Elvan Sans Italic"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "normal"
  weight: 500
  filename: "fonts/ttf/ElvanSans-Medium.ttf"
  post_script_name: "ElvanSans-Medium"
  full_name: "Elvan Sans Medium"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "italic"
  weight: 500
  filename: "fonts/ttf/ElvanSans-MediumItalic.ttf"
  post_script_name: "ElvanSans-MediumItalic"
  full_name: "Elvan Sans Medium Italic"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "normal"
  weight: 600
  filename: "fonts/ttf/ElvanSans-SemiBold.ttf"
  post_script_name: "ElvanSans-SemiBold"
  full_name: "Elvan Sans SemiBold"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "italic"
  weight: 600
  filename: "fonts/ttf/ElvanSans-SemiBoldItalic.ttf"
  post_script_name: "ElvanSans-SemiBoldItalic"
  full_name: "Elvan Sans SemiBold Italic"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "normal"
  weight: 700
  filename: "fonts/ttf/ElvanSans-Bold.ttf"
  post_script_name: "ElvanSans-Bold"
  full_name: "Elvan Sans Bold"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
fonts {
  name: "Elvan Sans"
  style: "italic"
  weight: 700
  filename: "fonts/ttf/ElvanSans-BoldItalic.ttf"
  post_script_name: "ElvanSans-BoldItalic"
  full_name: "Elvan Sans Bold Italic"
  copyright: "Copyright 2026 The Elvan Sans Project Authors"
}
subsets: "latin"
subsets: "latin-ext"
subsets: "tamil"
subsets: "menu"
""")

    print(f"Successfully organized Elvan Sans distribution files in: {dist_dir}")

if __name__ == "__main__":
    main()

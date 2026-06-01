import subprocess
import sys

def run(cmd):
    print("Running:", " ".join(cmd))
    subprocess.run(cmd, check=True)

# 1. Subset Google Sans
run([
    sys.executable, "-m", "fontTools.subset", 
    "Google_Sans/static/GoogleSans-Regular.ttf",
    "--unicodes=U+0000-0B7F,U+0C00-11FBF,U+12000-10FFFF",
    "--layout-features='*'",
    "--layout-scripts-=taml,tml2",
    "--glyph-names", "--symbol-cmap", "--legacy-cmap",
    "--notdef-glyph", "--notdef-outline", "--recommended-glyphs",
    "--name-IDs='*'", "--name-legacy", "--name-languages='*'",
    "--output-file=temp_fonts/GoogleSans-Regular-NoTamil.ttf"
])

# 2. Merge with Original Mukta Malar
run([
    sys.executable, "-m", "fontTools.merge",
    "temp_fonts/GoogleSans-Regular-NoTamil.ttf",
    "Mukta_Malar/MuktaMalar-Regular.ttf",
    "--output-file=temp_fonts/TestMerge-Regular.ttf"
])

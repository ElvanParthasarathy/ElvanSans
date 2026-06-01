import glob
from fontTools.ttLib import TTFont

def main():
    fonts = glob.glob("fonts/ttf/*.ttf")
    for f in fonts:
        print(f"Fixing PANOSE for {f}...")
        font = TTFont(f)
        if "OS/2" in font:
            p = font["OS/2"].panose
            p.bFamilyType = 2
            p.bSerifStyle = 11
            p.bWeight = 0
            p.bProportion = 0
            p.bContrast = 0
            p.bStrokeVariation = 0
            p.bArmStyle = 0
            p.bLetterForm = 0
            p.bMidline = 0
            p.bXHeight = 0
            font.save(f)
            
    print("Done! PANOSE codes updated.")

if __name__ == "__main__":
    main()

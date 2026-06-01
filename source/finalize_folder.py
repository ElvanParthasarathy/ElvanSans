import os
import shutil
import glob

def main():
    root = r"d:\Projects\Elvan Sans"
    fixed_dir = os.path.join(root, "Elvan_Sans_Fixed")
    fonts_dir = os.path.join(root, "fonts", "ttf")
    source_dir = os.path.join(root, "source")
    
    # 1. Delete old fonts
    for f in glob.glob(os.path.join(fonts_dir, "*.ttf")):
        os.remove(f)
        
    # 2. Move fixed fonts to fonts/ttf
    for f in glob.glob(os.path.join(fixed_dir, "*.ttf")):
        shutil.move(f, os.path.join(fonts_dir, os.path.basename(f)))
        
    # 3. Remove fixed directory
    if os.path.exists(fixed_dir):
        os.rmdir(fixed_dir)
        
    # 4. Move fontbakery report to source
    report = os.path.join(root, "fontbakery-report.md")
    if os.path.exists(report):
        shutil.move(report, os.path.join(source_dir, "fontbakery-report.md"))
        
    print("Files restructured successfully.")
    
if __name__ == "__main__":
    main()

import os
import shutil
import glob

def main():
    root = r"d:\Projects\Elvan Sans"
    upload_dir = os.path.join(root, "elvansans")
    
    # Create the folder
    os.makedirs(upload_dir, exist_ok=True)
    
    # Copy the fonts
    fonts_dir = os.path.join(root, "fonts", "ttf")
    for f in glob.glob(os.path.join(fonts_dir, "*.ttf")):
        shutil.copy(f, os.path.join(upload_dir, os.path.basename(f)))
        
    # Copy metadata files
    for f in ["OFL.txt", "METADATA.pb", "DESCRIPTION.en_us.html"]:
        src = os.path.join(root, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(upload_dir, f))
            
    print(f"Created ready-to-upload folder at: {upload_dir}")

if __name__ == "__main__":
    main()

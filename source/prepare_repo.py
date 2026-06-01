import os
import shutil

def main():
    root_dir = r"d:\Projects\Elvan Sans"
    source_dir = os.path.join(root_dir, "source")
    dist_dir = os.path.join(root_dir, "Elvan_Sans_Distribution")
    
    # 1. Create source folder
    os.makedirs(source_dir, exist_ok=True)
    
    # 2. List of things to move to source
    to_move = [
        "Google_Sans",
        "Mukta_Malar",
        "temp_fonts",
        "Elvan_Sans_Output",
        "build_elvan_sans.py",
        "try_var.py",
        "skew_font.py",
        "test_merge.py",
        "organize_distribution.py",
        "preview.html",
        "test_subset.html",
        "test_merge.html",
    ]
    
    for item in to_move:
        src_path = os.path.join(root_dir, item)
        dst_path = os.path.join(source_dir, item)
        if os.path.exists(src_path):
            try:
                shutil.move(src_path, dst_path)
                print(f"Moved {item} to source/")
            except Exception as e:
                print(f"Could not move {item}: {e}")
                
    # Move self as well
    self_path = os.path.join(root_dir, "prepare_repo.py")
    if os.path.exists(self_path):
        shutil.move(self_path, os.path.join(source_dir, "prepare_repo.py"))
                
    # 3. Move Distribution contents to Root
    if os.path.exists(dist_dir):
        for item in os.listdir(dist_dir):
            src_path = os.path.join(dist_dir, item)
            dst_path = os.path.join(root_dir, item)
            if os.path.exists(dst_path):
                if os.path.isdir(dst_path):
                    shutil.rmtree(dst_path)
                else:
                    os.remove(dst_path)
            shutil.move(src_path, dst_path)
            print(f"Moved {item} to root")
            
        os.rmdir(dist_dir)
        
    # 4. Create .gitignore
    gitignore_path = os.path.join(root_dir, ".gitignore")
    with open(gitignore_path, "w", encoding="utf-8") as f:
        f.write("""# Ignore temporary font build directories
source/temp_fonts/
source/Elvan_Sans_Output/

# Ignore Python caches
__pycache__/
*.pyc
""")
    print("Created .gitignore")
    
if __name__ == "__main__":
    main()

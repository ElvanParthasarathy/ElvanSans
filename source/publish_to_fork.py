import os
import shutil
import subprocess

def run_cmd(cmd, cwd=None):
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, cwd=cwd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
    else:
        print(result.stdout)
    return result.returncode == 0

def main():
    root = r"d:\Projects\Elvan Sans"
    clone_dir = os.path.join(root, "fonts_fork")
    
    # 1. Clone the fork (shallow clone to save time since it's huge)
    if not os.path.exists(clone_dir):
        success = run_cmd("git clone --depth 1 https://github.com/ElvanParthasarathy/fonts.git fonts_fork", cwd=root)
        if not success:
            return
            
    # 2. Create the target folder in the fork
    target_dir = os.path.join(clone_dir, "ofl", "elvansans")
    os.makedirs(target_dir, exist_ok=True)
    
    # 3. Copy files to the target folder
    # Copy TTF files
    fonts_dir = os.path.join(root, "fonts", "ttf")
    for f in os.listdir(fonts_dir):
        if f.endswith(".ttf"):
            shutil.copy(os.path.join(fonts_dir, f), os.path.join(target_dir, f))
            
    # Copy metadata files
    for f in ["OFL.txt", "METADATA.pb", "DESCRIPTION.en_us.html"]:
        src = os.path.join(root, f)
        if os.path.exists(src):
            shutil.copy(src, os.path.join(target_dir, f))
            
    # 4. Git add, commit, push in the fork
    run_cmd("git add ofl/elvansans", cwd=clone_dir)
    run_cmd('git commit -m "Add Elvan Sans to ofl/elvansans"', cwd=clone_dir)
    run_cmd("git push origin main", cwd=clone_dir)
    
    print("Successfully pushed to ElvanParthasarathy/fonts fork!")

if __name__ == "__main__":
    main()

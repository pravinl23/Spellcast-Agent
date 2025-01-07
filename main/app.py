import subprocess
import os

def main():
    # define the paths to the scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    setup_region_path = os.path.join(base_dir, "setup_region.py")
    screenshot_path = os.path.join(base_dir, "screenshot.py")

    # run setup_region.py to define the region
    subprocess.run(["python", setup_region_path], check=True)

    # run screenshot.py to take a screenshot of the defined region
    subprocess.run(["python", screenshot_path], check=True)

if __name__ == "__main__":
    main()

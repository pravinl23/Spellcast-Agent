import subprocess
import os

def main():
    # Define the paths to the scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    setup_region_path = os.path.join(base_dir, "setup_region.py")
    screenshot_path = os.path.join(base_dir, "screenshot.py")
    export_grid_path = os.path.join(base_dir, "export_grid.py")
    # Define the region to ss
    subprocess.run(["python", setup_region_path], check=True)

    # Take a screenshot of the defined region
    subprocess.run(["python", screenshot_path], check=True)

    # Extract the grid from the screenshot
    grid = subprocess.run(["python", export_grid_path], check=True)

    for row in grid:
        print(row)

if __name__ == "__main__":
    main()

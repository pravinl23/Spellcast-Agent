import subprocess
import os
from export_grid import export_grid
from word_finder import solve_grid
def main():

    # Define the paths to the scripts
    base_dir = os.path.dirname(os.path.abspath(__file__))
    setup_region_path = os.path.join(base_dir, "setup_region.py")
    screenshot_path = os.path.join(base_dir, "screenshot.py")


    # 1st Define the region to ss
    subprocess.run(["python", setup_region_path], check=True)

    # 2nd Take a screenshot of the defined region
    subprocess.run(["python", screenshot_path], check=True)

    # Extract the grid from the screenshot
    grid = export_grid()

    for row in grid:
        print(row)

    # 4th Solve the grid
    results = solve_grid(grid)

    print(f"\nBest word found: {results['word']} (Score: {results['score']})")
    print("\nPath to follow:")
    print(results['path_instructions'])
    print("\nGrid with path:")
    print(results['grid_display'])
        

if __name__ == "__main__":
    main()
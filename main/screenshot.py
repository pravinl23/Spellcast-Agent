import tkinter as tk
import os
from PIL import ImageGrab

# Load region from the file region_data.txt which is collected by the program on setup_region.py
def load_region():
    # Get the parent directory (spellcast-solver) to read the file from there
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    region_file_path = os.path.join(parent_dir, 'region_data.txt')
    with open(region_file_path, 'r') as f:
        region_data = f.read().split(',')

        return tuple(map(int, region_data))

def take_screenshot():
    # Take a screenshot of the specified region
    region = load_region();
    # Get the parent directory (spellcast-solver) to save the file there
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    screenshot_path = os.path.join(parent_dir, "grid.png")
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)  # Delete the previous screenshot if it exists already
    
    left, top, width, height = region
    right = left + width
    bottom = top + height
    
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot.save(screenshot_path)


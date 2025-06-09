import os
import time
from PIL import ImageGrab
from export_grid import export_grid
from word_finder import solve_grid
import pyautogui
from auto_solver import get_grid_coordinates, perform_drag_sequence

# Global flag to control agentic mode
agentic_mode_active = False

def take_agentic_screenshot():
    # take screenshot of the grid
    left, top, width, height = 703, 300, 324, 318
    right = left + width
    bottom = top + height
    
    # save file in the parent directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    parent_dir = os.path.dirname(script_dir)
    screenshot_path = os.path.join(parent_dir, "grid.png")
    
    if os.path.exists(screenshot_path):
        # delete the previous screenshot if it exists
        os.remove(screenshot_path)  
    
    screenshot = ImageGrab.grab(bbox=(left, top, right, bottom))
    screenshot.save(screenshot_path)
    return True

def agentic_solve():
    # Continuously solve Spellcast puzzles until an error occurs or stopped
    global agentic_mode_active
    
    agentic_mode_active = True
    print("Starting agentic solver - will continuously solve puzzles...")
    print("Press ⌘+K to stop at any time")
    print("Using agentic coordinates: 703,300,324,318")
    
    cycle_count = 0
    
    try:
        while agentic_mode_active:
            cycle_count += 1
            print(f"\n=== Cycle {cycle_count} ===")
            
            # Take screenshot using agentic coordinates
            print("Taking screenshot...")
            screenshot_success = take_agentic_screenshot()
            if not screenshot_success:
                print("Failed to take screenshot - stopping agentic mode")
                break
            
            # Export grid (this processes the screenshot)
            try:
                grid = export_grid()
                if not grid:
                    print("Failed to export grid - stopping agentic mode")
                    break
                
                print("Grid detected successfully")
                
                # Solve the grid
                results = solve_grid(grid)
                if 'error' in results:
                    print(f"Solver error: {results['error']} - stopping agentic mode")
                    break
                
                print(f"Solution found: {results['word']} (Score: {results['score']})")
                
                # Get coordinates and perform drag
                grid_coordinates = get_grid_coordinates()
                success = perform_drag_sequence(results['path'], grid_coordinates)
                
                if not success:
                    print("Failed to execute drag sequence - stopping agentic mode")
                    break
                
                print(f"Successfully executed: {results['word']}")
                
                # Wait before next cycle (can be interrupted by stop command)
                print("Waiting 12 seconds before next cycle...")
                for i in range(12):
                    print("waiting")
                    if not agentic_mode_active:
                        break
                    time.sleep(1)
                
            except Exception as e:
                print(f"Error during processing (Cycle {cycle_count}): {e}")
                break
                
    except KeyboardInterrupt:
        print(f"\nAgentic mode stopped by user after {cycle_count} cycles")
    
    agentic_mode_active = False
    print("Returning to manual mode...")
    return True

def stop_agentic_mode():
    # Stop the agentic mode
    global agentic_mode_active
    agentic_mode_active = False
    print("Stopping agentic mode...")

if __name__ == "__main__":
    agentic_solve() 
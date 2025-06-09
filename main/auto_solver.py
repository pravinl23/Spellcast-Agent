import time
from export_grid import export_grid
from word_finder import solve_grid

import pyautogui

def get_grid_coordinates():
    coordinates = {
        (0, 0): (749, 343),
        (0, 1): (805, 342),
        (0, 2): (868, 342),
        (0, 3): (929, 340),
        (0, 4): (991, 343),
        (1, 0): (748, 405),
        (1, 1): (808, 403),
        (1, 2): (866, 404),
        (1, 3): (934, 402),
        (1, 4): (987, 398),
        (2, 0): (748, 463),
        (2, 1): (816, 462),
        (2, 2): (867, 463),
        (2, 3): (925, 464),
        (2, 4): (983, 463),
        (3, 0): (754, 513),
        (3, 1): (812, 522),
        (3, 2): (866, 522),
        (3, 3): (923, 521),
        (3, 4): (988, 527),
        (4, 0): (746, 574),
        (4, 1): (800, 577),
        (4, 2): (874, 580),
        (4, 3): (932, 582),
        (4, 4): (989, 580)
    }
    return coordinates


def perform_drag_sequence(path_coords, grid_coordinates, drag_duration=0.4, pause_between=0.1):
    # Disable pyautogui failsafe temporarily
    pyautogui.FAILSAFE = False

    # Convert grid coordinates to screen coordinates
    screen_path = [grid_coordinates[(row, col)] for row, col in path_coords]

    # Start at the first tile
    start_x, start_y = screen_path[0]
    pyautogui.moveTo(start_x, start_y, duration=0.2)
    time.sleep(pause_between)

    # Press and hold mouse
    pyautogui.mouseDown()
    time.sleep(0.05)

    # Drag through path
    for x, y in screen_path[1:]:
        pyautogui.moveTo(x, y, duration=drag_duration)
        time.sleep(pause_between)

    # Release mouse
    pyautogui.mouseUp()

    # Re-enable failsafe
    pyautogui.FAILSAFE = True


def auto_solve():
    grid = export_grid()
    results = solve_grid(grid)
    
    # get screen coordinates for each cell
    grid_coordinates = get_grid_coordinates()
    # perform drag
    perform_drag_sequence(results['path'], grid_coordinates)    
    return True

if __name__ == "__main__":
    auto_solve() 
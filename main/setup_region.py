import tkinter as tk
from PIL import Image, ImageTk, ImageGrab
from screeninfo import get_monitors
import os

# global variables
region = None
click_count = 0
top_left = None
bottom_right = None
dot_canvas = None
region_window = None
background_image = None
dot_coords = []  # keep track of drawn dots for clarity

# Handles mouse clicks on the canvas
def on_canvas_click(event):
    global click_count, top_left, bottom_right, region, region_window

    x, y = event.x, event.y
    dot_canvas.create_oval(x - 5, y - 5, x + 5, y + 5, fill="red", outline="red")
    dot_canvas.update()  # ensure dot renders immediately

    if click_count == 0:
        top_left = (x, y)
    elif click_count == 1:
        bottom_right = (x, y)
        region = (
            top_left[0],
            top_left[1],
            bottom_right[0] - top_left[0],
            bottom_right[1] - top_left[1]
        )

        # Save region to file
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        region_file_path = os.path.join(parent_dir, 'region_data.txt')

        with open(region_file_path, 'w') as f:
            f.write(f"{region[0]},{region[1]},{region[2]},{region[3]}")

        region_window.destroy()

    click_count += 1

def define_region():
    global dot_canvas, region_window, background_image

    background_ss = "background.png"
    if os.path.exists(background_ss):
        os.remove(background_ss)

    # Capture full screen
    bg_ss = ImageGrab.grab()
    bg_ss.save(background_ss)

    monitor = get_monitors()[0]
    screen_width, screen_height = monitor.width, monitor.height

    screenshot = Image.open(background_ss)
    screenshot = screenshot.resize((screen_width, screen_height), Image.Resampling.LANCZOS)

    region_window = tk.Toplevel()
    region_window.title("Define Region")
    region_window.configure(bg="black")
    region_window.geometry(f"{screen_width}x{screen_height}+0+0")
    region_window.attributes("-topmost", True)

    # Store the image to prevent garbage collection
    background_image = ImageTk.PhotoImage(screenshot)
    region_window.background_image_ref = background_image

    dot_canvas = tk.Canvas(region_window, bg="black", highlightthickness=0, width=screen_width, height=screen_height)
    dot_canvas.pack(fill=tk.BOTH, expand=True)
    dot_canvas.create_image(0, 0, anchor="nw", image=background_image)
    dot_canvas.bind("<Button-1>", on_canvas_click)

    if os.path.exists(background_ss):
        os.remove(background_ss)

    print("Starting region GUI...")
    region_window.mainloop()

import tkinter as tk
from PIL import Image, ImageTk
import os
import pyautogui

# global variables
region = None
click_count = 0
top_left = None
bottom_right = None
dot_canvas = None
region_window = None
background_image = None

# handles mouse clicks on the canvas, marks clicked position with red dot, and captures coords
def on_canvas_click(event):
    global click_count, top_left, bottom_right, region

    # get the clicked position (x, y) on the canvas
    x, y = event.x, event.y

    # put a small red dot on the canvas at the clicked position
    dot_canvas.create_oval(x-5, y-5, x+5, y+5, fill="red", outline="red")

    # this saves the positions for the top left and bottom right corners
    if click_count == 0:
        # first click sets the top left corner
        top_left = (x, y)

    elif click_count == 1:
        # second click sets the bottom right corner
        bottom_right = (x, y)

        # create the region based on the two selected corners
        region = (top_left[0], top_left[1], bottom_right[0] - top_left[0], bottom_right[1] - top_left[1])
        
        # save the region data to a file for later use
        with open('region_data.txt', 'w') as f:
            # write the region in the format x, y, width, height
            f.write(f"{region[0]},{region[1]},{region[2]},{region[3]}")

        # close the region selection window
        region_window.quit()

    # increment the click counter
    click_count += 1

# creates define region area by first taking a screenshot of the screen, then using that as the background for a 
# defining region popup where users can manually click what area of the screen they want to take screenshots of
def define_region():
    global dot_canvas, region_window, background_image

    # file name for screenshot
    background_ss = "background.png"
    # remove any previous screenshot to ensure a fresh capture
    if os.path.exists(background_ss):
        os.remove(background_ss)
    # capture the entire screen using pyautogui and save it as a file
    bg_ss = pyautogui.screenshot()
    bg_ss.save(background_ss)
    # get the screen dimensions (width and height) using pyautogui
    screen_width, screen_height = pyautogui.size()
    # open the saved screenshot and resize it to match the screen dimensions
    screenshot = Image.open(background_ss)
    screenshot = screenshot.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
    # convert the resized image to a PhotoImage format for tkinter
    background_image = ImageTk.PhotoImage(screenshot)

    # create a new tkinter window for region selection
    region_window = tk.Toplevel()
    region_window.title("Define Region")

    # set window background colour and make it fullscreen
    region_window.configure(bg="black")
    region_window.attributes("-fullscreen", True)

    # create a canvas that display the screenshot and detect mouse clicks
    dot_canvas = tk.Canvas(region_window, bg="black", highlightthickness=0, width=screen_width, height=screen_height)
    dot_canvas.pack(fill=tk.BOTH, expand=True)
    dot_canvas.create_image(0, 0, anchor="nw", image=background_image)

    # button-1 is left mouse button, when clicked it calls on_canvas_click function
    dot_canvas.bind("<Button-1>", on_canvas_click)

    # delete the screenshot because it is uncessary after this
    os.remove(background_ss)


if __name__ == "__main__":
    # create the popup window for defining region
    root = tk.Tk()
    # this is for the actual window not button
    root.title("Region Setup")
    root.geometry("300x100")
    root.configure(bg="azure2")

    # this is for the button on the popup window
    button = tk.Button(
        root,
        text="Define Region",
        font='Helvetica 18 bold',
        command=define_region # calls the define_region function on click
    )

    button.pack(pady=20)

    # start the tkinter event loop to display the popup window
    root.mainloop()

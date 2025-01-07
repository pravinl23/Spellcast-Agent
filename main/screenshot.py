import tkinter as tk
import os
import pyautogui

# load region from the file region_data.txt which is collected by the program on setup_region.py
def load_region():
    with open('region_data.txt', 'r') as f:
        region_data = f.read().split(',')
        # after region data is extracted remove the region_data.txt file
        os.remove('region_data.txt')
        return tuple(map(int, region_data))

region = load_region()

def take_screenshot():
    # take a screenshot of the specified region
    screenshot_path = "grid.png"
    if os.path.exists(screenshot_path):
        os.remove(screenshot_path)  # delete the previous screenshot if it exists already
    screenshot = pyautogui.screenshot(region=region)
    screenshot.save(screenshot_path)


if __name__ == "__main__":
    # create the popup window for defining region
    root = tk.Tk()
    # this is for the actual window not button
    root.title("Spellcast AI")
    root.geometry("300x100")
    root.configure(bg="azure2")

    # this is for the button on the popup window
    button = tk.Button(
        root,
        text="Define Region",
        font='Helvetica 18 bold',
        command=take_screenshot # calls the define_region function on click
    )

    button.pack(pady=20)

    # start the tkinter event loop to display the popup window
    root.mainloop()

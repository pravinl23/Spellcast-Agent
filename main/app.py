import os
from export_grid import export_grid
from word_finder import solve_grid
from pynput import keyboard
from screenshot import take_screenshot
import tkinter as tk
import queue
import threading
import subprocess
import sys

gui_queue = queue.Queue()
overlay_proc = None

# Queue GUI task instead of calling directly
def run_setup_region():
    script = os.path.join(os.path.dirname(__file__), "setup_region.py")
    python_exe = sys.executable
    subprocess.Popen([python_exe, script])

def run_screenshot():
    global overlay_proc
    # Kill any existing overlay 
    if overlay_proc is not None:
        try:
            overlay_proc.terminate()
        except Exception:
            pass
        overlay_proc = None

    take_screenshot()

def get_output():
    global overlay_proc
    script = os.path.join(os.path.dirname(__file__), "overlay.py")
    # kill any existing overlay before spawning a new one
    if overlay_proc is not None:
        try:
            overlay_proc.terminate()
        except Exception:
            pass

    overlay_proc = subprocess.Popen([sys.executable, script])

# Track pressed keys for Command shortcuts
current_keys = set()

def on_press(key):
    try:
        current_keys.add(key)
        if keyboard.Key.cmd in current_keys and hasattr(key, 'char'):
            if key.char == '1':
                print("Setting up region...")
                run_setup_region()
            elif key.char == '2':
                print("Taking screenshot...")
                run_screenshot()
            elif key.char == '3':
                print("Processing output...")
                get_output()
    except AttributeError:
        pass


def on_release(key):
    try:
        current_keys.remove(key)
    except KeyError:
        pass

# Main entry point: starts listener and runs Tk loop on main thread
def main():
    global root
    print("Spellcast Solver is running in the background.")
    print("Use the following keyboard shortcuts:")
    print("⌘+1: Setup Region")
    print("⌘+2: Take Screenshot")
    print("⌘+3: Process and Get Output")
    print("Press Ctrl+C to exit")

    listener = keyboard.Listener(on_press=on_press, on_release=on_release)
    listener_thread = threading.Thread(target=listener.start, daemon=True)
    listener_thread.start()

    # Initialize main Tk root for GUI tasks
    root = tk.Tk()
    root.withdraw()

    # Periodically poll for queued GUI tasks
    def poll_gui_tasks():
        while not gui_queue.empty():
            task = gui_queue.get()
            try:
                task()
            except Exception as e:
                print(f"Error running GUI task: {e}")
        root.after(100, poll_gui_tasks)

    poll_gui_tasks()
    root.mainloop()

if __name__ == "__main__":
    main()

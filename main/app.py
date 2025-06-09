import os
import sys
import subprocess
import queue
import threading
import tkinter as tk
from pynput import keyboard
from screenshot import take_screenshot
from auto_solver import auto_solve
from agentic import agentic_solve, stop_agentic_mode


gui_queue = queue.Queue()
overlay_proc = None
agentic_mode_active = False

def export_grid_dimensions():
    # Setup grid region by running setup_region.py
    print("Launching region setup tool...")
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
                print("Exporting grid dimensions...")
                export_grid_dimensions()
            elif key.char == '2':
                print("Taking screenshot...")
                run_screenshot()
            elif key.char == '3':
                print("Extracting grid and showing overlay...")
                get_output()
            elif key.char == '4':
                print("Auto solving puzzle...")
                auto_solve()
            elif key.char == '5':
                print("Starting agentic mode...")
                agentic_solve()
            elif key.char == 'k':
                stop_agentic_mode()
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
    print("⌘+1: Export Grid Dimensions")
    print("⌘+2: Take Screenshot")
    print("⌘+3: Extract Grid and Show Overlay")
    print("⌘+4: Auto Drag and Solve")
    print("⌘+5: Agentic Mode (continuous solving)")
    print("⌘+K: Stop Agentic Mode")
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

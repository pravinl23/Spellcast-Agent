import tkinter as tk
from export_grid import export_grid
from word_finder import solve_grid


def pop_grid_overlay(grid, path_coords=None, window_size=250):
    rows = len(grid)
    cols = len(grid[0]) if rows else 0
    if rows == 0 or cols == 0:
        return

    # Size of each grid cell
    cell = window_size // max(rows, cols)
    # Center the grid
    offset_x = (window_size - cols * cell) // 2
    offset_y = (window_size - rows * cell) // 2

    # Keep the window up
    root = tk.Tk()
    root.overrideredirect(True)
    root.attributes('-topmost', True)

    sw = root.winfo_screenwidth()
    sh = root.winfo_screenheight()
    init_x = sw - window_size - 10
    init_y = sh // 8
    root.geometry(f"{window_size}x{window_size}+{init_x}+{init_y}")

    canvas = tk.Canvas(root, width=window_size, height=window_size, highlightthickness=0, bg='black')
    canvas.pack()

    # Draw the grid
    for r in range(rows):
        for c in range(cols):
            x0 = offset_x + c * cell
            y0 = offset_y + r * cell
            x1 = x0 + cell
            y1 = y0 + cell
            canvas.create_rectangle(x0, y0, x1, y1, outline='white', width=0.5)
            canvas.create_text(
                x0 + cell/2, y0 + cell/2,
                text=grid[r][c],
                font=('Helvetica', int(cell * 0.4)),
                fill='white'
            )

    # Overlay the path
    if path_coords:
        # Compute center points for each cell in path
        centers = []
        for r, c in path_coords:
            cx = offset_x + c * cell + cell/2
            cy = offset_y + r * cell + cell/2
            centers.append((cx, cy))
        # Draw circles and connecting lines
        radius = cell * 0.25
        for i, (cx, cy) in enumerate(centers):
            canvas.create_oval(
                cx - radius, cy - radius,
                cx + radius, cy + radius,
                outline='blue', width=1
            )
            if i > 0:
                x1, y1 = centers[i-1]
                canvas.create_line(x1, y1, cx, cy, fill='blue', width=2)

    # Make window draggable
    def start_move(e):
        root._x = e.x
        root._y = e.y
    def on_motion(e):
        x = e.x_root - root._x
        y = e.y_root - root._y
        root.geometry(f"{window_size}x{window_size}+{x}+{y}")
    root.bind('<ButtonPress-1>', start_move)
    root.bind('<B1-Motion>', on_motion)

    # Keep window on top at all times
    def keep_lifting():
        root.lift()
        root.after(500, keep_lifting)
    keep_lifting()

    root.mainloop()


if __name__ == "__main__":
    grid = export_grid()
    results = solve_grid(grid)

    for row in grid:
        print(row)

    print(f"\nBest word found: {results['word']} (Score: {results['score']})")
    print("\nPath to follow:")
    print(results['path_instructions'])
    print("\nGrid with path:")
    print(results['grid_display'])


    path_coords = results.get('path', [])

    pop_grid_overlay(grid, path_coords=path_coords)

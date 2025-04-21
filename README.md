## Project Overview

**Spellcast Solver** is a lightweight desktop helper that automates the repetitive steps of the SpellCast mini‑game:
1. **Select** the on‑screen grid region.  
2. **Snap** a screenshot of that region.  
3. **Detect** each letter with a custom YOLO/PyTorch model.  
4. **Evalulate** the best‑scoring word path.  
5. **Overlay** the solution back on your screen in a floating, always‑on‑top window.

All you need to do is press:
- ⌘+1 to pick the board area  
- ⌘+2 to capture the latest grid  
- ⌘+3 to see the solver’s answer pop up

Under the hood we combine:
- **`screeninfo`** + **`Pillow`** for grabbing your grid  
- **PyTorch/YOLOv5** for robust letter detection  
- A simple **DFS** path‑finding to maximize score  
- **Tkinter** to draw a draggable, semi‑transparent overlay you can move out of the way

## Getting Started

1. **Clone & install**  
   ```bash
   git clone https://github.com/pravinl23/SpellcastSolver.git
   cd SpellcastSolver
   pip install -r requirements.txt

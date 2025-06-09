# Spellcast AI Solver

An AI-powered desktop app that automatically solves Spellcast word puzzles for you.

## What it does

This app can:
- 📸 Take screenshots of your Spellcast game
- 🤖 Use AI to read the letters in the grid
- 🎯 Find the highest-scoring word automatically  
- 🖱️ Control your mouse to trace the solution
- 🔄 Run continuously to solve puzzle after puzzle

## How to use

1. **Install and run**
   ```bash
   git clone https://github.com/pravinl23/SpellcastSolver.git
   cd SpellcastSolver
   pip install -r requirements.txt
   python main/app.py
   ```

2. **Use keyboard shortcuts while playing Spellcast:**
   - `⌘+1` - Set up screen region (first time only)
   - `⌘+2` - Take screenshot
   - `⌘+3` - Show solution overlay
   - `⌘+4` - Auto-solve (moves mouse automatically)
   - `⌘+5` - Auto-solve continuously 
   - `⌘+K` - Stop auto-solving

## How it works

The app combines several technologies:
- **Computer Vision**: Custom AI model trained to recognize letters
- **Word Finding**: Smart algorithm to find the best scoring words
- **Automation**: Controls your mouse to execute the solution

## Requirements

- macOS, Windows, or Linux
- Python 3.8+
- Webcam/screen access permissions


import os
import sys
import cv2
import numpy as np
from PIL import Image
import pytesseract
import argparse

def extract_with_tesseract(image_path, rows=5, cols=5):
    """
    Extract text from the grid image using pytesseract
    """
    # Read the image
    img = cv2.imread(image_path)
    if img is None:
        print(f"Could not read image from {image_path}")
        return None
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to make text clearer
    _, thresh = cv2.threshold(gray, 150, 255, cv2.THRESH_BINARY_INV)
    
    # Calculate cell size
    height, width = thresh.shape
    cell_height = height // rows
    cell_width = width // cols
    
    # Create empty grid for tesseract output
    tesseract_grid = []
    
    # Process each cell
    for row in range(rows):
        tesseract_row = []
        for col in range(cols):
            # Calculate cell coordinates
            y1 = row * cell_height
            y2 = (row + 1) * cell_height
            x1 = col * cell_width
            x2 = (col + 1) * cell_width
            
            # Extract cell
            cell = thresh[y1:y2, x1:x2]
            
            # Add padding around the cell
            cell_padded = cv2.copyMakeBorder(cell, 10, 10, 10, 10, cv2.BORDER_CONSTANT, value=0)
            
            # Convert to PIL image for tesseract
            pil_img = Image.fromarray(cell_padded)
            
            # Extract text with tesseract (configure for single character)
            text = pytesseract.image_to_string(
                pil_img, 
                config='--psm 10 --oem 3 -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZ'
            ).strip()
            
            # If tesseract finds a character, add it, otherwise add '?'
            if len(text) == 1 and text.isalpha():
                tesseract_row.append(text.upper())
            else:
                tesseract_row.append('?')
        
        tesseract_grid.append(tesseract_row)
    
    return tesseract_grid

def compare_grids(model_grid, tesseract_grid):
    """
    Compare two grids and calculate accuracy metrics
    """
    if not model_grid or not tesseract_grid:
        return None
    
    total_cells = len(model_grid) * len(model_grid[0])
    matching_cells = 0
    model_valid_chars = 0
    tesseract_valid_chars = 0
    
    for i in range(len(model_grid)):
        for j in range(len(model_grid[i])):
            model_char = model_grid[i][j]
            tesseract_char = tesseract_grid[i][j]
            
            # Count cells where both methods agree
            if model_char == tesseract_char and model_char != '?':
                matching_cells += 1
            
            # Count valid characters detected by each method
            if model_char != '?':
                model_valid_chars += 1
            if tesseract_char != '?':
                tesseract_valid_chars += 1
                
            # Print comparison for debugging
            print(f"Position [{i}][{j}]: Model: {model_char}, Tesseract: {tesseract_char}")
    
    # Calculate statistics
    agreement_percentage = (matching_cells / total_cells) * 100 if total_cells > 0 else 0
    model_detection_rate = (model_valid_chars / total_cells) * 100 if total_cells > 0 else 0
    tesseract_detection_rate = (tesseract_valid_chars / total_cells) * 100 if total_cells > 0 else 0
    
    return {
        'agreement': agreement_percentage,
        'model_detection_rate': model_detection_rate,
        'tesseract_detection_rate': tesseract_detection_rate,
        'model_valid_chars': model_valid_chars,
        'tesseract_valid_chars': tesseract_valid_chars,
        'total_cells': total_cells
    }

def parse_input_grid(input_str):
    """
    Parse a string representation of a grid into a 2D list
    Format: "ABCDE,FGHIJ,KLMNO,PQRST,UVWXY"
    """
    try:
        rows = input_str.strip().split(',')
        grid = []
        for row in rows:
            grid_row = [char.upper() for char in row.strip()]
            grid.append(grid_row)
        return grid
    except Exception as e:
        print(f"Error parsing grid input: {e}")
        return None

def main():
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='Compare PyTorch model output with Tesseract OCR')
    parser.add_argument('--grid', type=str, help='Custom grid string in format "ABCDE,FGHIJ,KLMNO,PQRST,UVWXY"')
    parser.add_argument('--image', type=str, default="grid.png", help='Path to the grid image (default: grid.png)')
    args = parser.parse_args()
    
    # Default model grid (update with your actual model output if known)
    model_grid = [
        ['L', 'V', 'O', 'L', 'E'],
        ['O', 'A', 'D', 'K', 'E'],
        ['V', 'O', 'V', 'S', 'O'],
        ['R', 'F', 'T', 'N', 'E'],
        ['I', 'A', 'N', 'D', 'I']
    ]
    
    # If custom grid is provided, parse it
    if args.grid:
        custom_grid = parse_input_grid(args.grid)
        if custom_grid:
            model_grid = custom_grid
            print("Using custom grid input.")
    
    # Path to the image
    image_path = args.image
    
    # Check if image exists
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return
    
    # Extract using pytesseract
    print("Extracting text using Tesseract...")
    tesseract_grid = extract_with_tesseract(image_path)
    
    if tesseract_grid:
        # Print grids for comparison
        print("\nModel output:")
        for row in model_grid:
            print(' '.join(row))
        
        print("\nTesseract output:")
        for row in tesseract_grid:
            print(' '.join(row))
        
        # Calculate and print comparison metrics
        print("\nCalculating comparison metrics...")
        metrics = compare_grids(model_grid, tesseract_grid)
        
        if metrics:
            print(f"\nAgreement between models: {metrics['agreement']:.2f}%")
            print(f"Model character detection rate: {metrics['model_detection_rate']:.2f}% ({metrics['model_valid_chars']} of {metrics['total_cells']} cells)")
            print(f"Tesseract character detection rate: {metrics['tesseract_detection_rate']:.2f}% ({metrics['tesseract_valid_chars']} of {metrics['total_cells']} cells)")
            
            if metrics['model_detection_rate'] > metrics['tesseract_detection_rate']:
                improvement = metrics['model_detection_rate'] - metrics['tesseract_detection_rate']
                print(f"\nYour model performs {improvement:.2f}% better than Tesseract for character detection!")
            else:
                difference = metrics['tesseract_detection_rate'] - metrics['model_detection_rate']
                print(f"\nTesseract performs {difference:.2f}% better than your model for character detection.")
    else:
        print("Tesseract extraction failed. Make sure all dependencies are installed and the image exists.")

if __name__ == "__main__":
    main() 
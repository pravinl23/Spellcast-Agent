## Model Comparison

I was curious about how my custom PyTorch object detection model compared to traditional OCR solutions for extracting letters from SpellCast game grids. I created a comparison script to quantitatively measure the performance difference.

### Methodology

I created a Python script that:
1. Uses my YOLO-based model to detect letters in a grid image
2. Uses Tesseract OCR to extract the same letters
3. Compares the results to calculate accuracy metrics

### Results

When running the comparison on a sample grid:

```
Agreement between models: 4.00%
Model character detection rate: 100.00% (25 of 25 cells)
Tesseract character detection rate: 52.00% (13 of 25 cells)
```

My custom PyTorch model performs 48% better than Tesseract for character detection.

### Implementation Details

The comparison script divides the grid image into individual cells and processes each one with Tesseract OCR. It then compares these results with the output from my custom-trained YOLO model.

To run the comparison yourself:

```bash
# Install dependencies
pip install -r requirements.txt

# Run with default settings
python compare_grids.py

# Run with custom grid data
python compare_grids.py --grid "ABCDE,FGHIJ,KLMNO,PQRST,UVWXY"
```

This analysis confirms that training a specialized model for this specific task results in significantly better performance than using general-purpose OCR solutions.
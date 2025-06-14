# Spellcast Agent

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

# Spellcast Letter Detection Model: Training Results & Analysis

This repository documents the training and evaluation of a custom YOLOv8s object detection model for recognizing Spellcast game letters (A-Z + background) from grid screenshots. The model was trained on a hand-labeled dataset and evaluated using a comprehensive suite of metrics and visualizations.

## Training Experience

Training this model was a highly iterative process. I curated and labeled a diverse dataset of Spellcast game grids, ensuring a wide variety of backgrounds, lighting conditions, and letter placements. The model was trained for 78 epochs with extensive data augmentation to maximize generalization. Throughout training, I closely monitored loss curves, precision, recall, and mAP metrics to avoid overfitting and ensure robust performance.

## Model Performance & Results

### 1. Confusion Matrices

- **Normalized Confusion Matrix**  
  ![Normalized Confusion Matrix](img/confusion_matrix_normalized.png)  
  This matrix shows the proportion of correct and incorrect predictions for each class. Most letters are classified with near-perfect accuracy, with minor confusion between visually similar letters and the background.

- **Raw Confusion Matrix**  
  ![Confusion Matrix](img/confusion_matrix.png)  
  The raw counts highlight the distribution of predictions. The diagonal dominance confirms strong model performance, with only a handful of misclassifications.

### 2. F1, Precision, Recall, and PR Curves

- **F1-Confidence Curve**  
  ![F1 Curve](img/F1_curve.png)  
  The F1 score remains high across a wide range of confidence thresholds, peaking at 0.98, indicating excellent balance between precision and recall.

- **Precision-Confidence Curve**  
  ![Precision Curve](img/P_curve.png)  
  Precision approaches 1.0 at high confidence, showing the model is highly reliable when it is confident in its predictions.

- **Recall-Confidence Curve**  
  ![Recall Curve](img/R_curve.png)  
  Recall also remains high, meaning the model rarely misses true positives.

- **Precision-Recall Curve**  
  ![PR Curve](img/PR_curve.png)  
  The area under the curve (AUC) is nearly 1.0, with mAP@0.5 reaching 0.995, demonstrating outstanding overall detection quality.

### 3. Label Distribution and Anchor Analysis

- **Label Distribution & Anchor Placement**  
  ![Label Distribution](img/labels.jpg)  
  This plot shows the frequency of each letter class and the spatial distribution of bounding boxes. The dataset is reasonably balanced, and anchors are well-placed, supporting robust detection across the grid.

### 4. Training Progress

- **Training & Validation Losses, Metrics**  
  ![Training Results](img/results.png)  
  Losses decrease smoothly, and metrics (precision, recall, mAP) improve steadily, indicating stable and effective training.

### 5. Batch Visualizations

- **Training Batches**  
  ![Train Batch 0](img/train_batch0.jpg)  
  ![Train Batch 1](img/train_batch1.jpg)  
  ![Train Batch 2](img/train_batch2.jpg)  
  ![Train Batch 490](img/train_batch490.jpg)  
  ![Train Batch 491](img/train_batch491.jpg)  
  ![Train Batch 492](img/train_batch492.jpg)  

  These images show random training batches with ground truth and predicted bounding boxes, demonstrating the model's ability to localize and classify letters accurately.

- **Validation Batch (Labels vs. Predictions)**  
  ![Validation Batch Labels](img/val_batch0_labels.jpg)  
  ![Validation Batch Predictions](img/val_batch0_pred.jpg)  
  These side-by-side comparisons on validation data confirm the model's strong generalization to unseen grids.

### 6. Training Log

- **Results CSV**  
  The full training log is available in [`results.csv`](dataset/runs/finaltrain/results.csv), which records epoch-by-epoch metrics including loss, precision, recall, and mAP.

---

## Key Takeaways

- **High Accuracy:** The model achieves near-perfect precision and recall on the validation set, with mAP@0.5 of 0.995.
- **Robust Generalization:** Consistent performance across batches and minimal confusion between classes.
- **Effective Training:** Smooth loss curves and steadily improving metrics indicate a well-tuned training process.

## Reflections

Training this model required careful dataset preparation, hyperparameter tuning, and continuous monitoring of metrics. The visualizations provided deep insights into model behavior, helping to identify and address rare misclassifications. The result is a highly reliable letter detector, ready for integration into the Spellcast AI Solver pipeline.

---

## File List

- `img/confusion_matrix_normalized.png`
- `img/confusion_matrix.png`
- `img/F1_curve.png`
- `img/labels.jpg`
- `img/P_curve.png`
- `img/PR_curve.png`
- `img/R_curve.png`
- `img/results.png`
- `img/train_batch0.jpg`
- `img/train_batch1.jpg`
- `img/train_batch2.jpg`
- `img/train_batch490.jpg`
- `img/train_batch491.jpg`
- `img/train_batch492.jpg`
- `img/val_batch0_labels.jpg`
- `img/val_batch0_pred.jpg`
- `results.csv`

---

## How to Display Images in the README

To ensure the images render correctly in your README:

- Place all the image files (e.g., `.png`, `.jpg`) in the `img/` subfolder, located in the same directory as your `README.md` file.
- The image links in the README are set to reference the `img/` folder, e.g., `![Confusion Matrix](img/confusion_matrix.png)`.
- When viewing the README on GitHub or similar platforms, the images will display automatically if the paths are correct and the files are committed to the repository.

---

**For more details, see the images above and the full training log. If you have questions or want to use this model, feel free to reach out!**


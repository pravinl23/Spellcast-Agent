import os
import httpx
from dotenv import load_dotenv

load_dotenv()
REMOTE_URL = os.environ.get("REMOTE_URL", "http://localhost:8000/predict")

CLASS_MAP = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 
    5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O',
    15: 'P', 16: 'Q', 17: 'R', 18: 'S', 19: 'T',
    20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z'
}

# Converts YOLO detections into a rows x cols 2D array
def to_2d_array(detections, rows, cols):

    # First calculate center coordinates for each bounding box
    for det in detections:
        det['cx'] = (det['x1'] + det['x2']) / 2.0
        det['cy'] = (det['y1'] + det['y2']) / 2.0

    # Sort all detections by their center_y
    detections_sorted = sorted(detections, key=lambda d: d['cy'])

    grid = []
    
    # Now chunk into rows
    for row_idx in range(rows):
        # Get the slice of detections for this row
        start_idx = row_idx * cols
        end_idx = start_idx + cols
        row_dets = detections_sorted[start_idx:end_idx]

        # Sort each row chunk by center_x
        row_dets_sorted = sorted(row_dets, key=lambda d: d['cx'])

        # Convert to characters
        row_chars = [CLASS_MAP.get(det['class'], '?') for det in row_dets_sorted]

        grid.append(row_chars)

    return grid


def export_grid():
    script_dir = os.path.dirname(os.path.abspath(__file__))
    image_path = os.path.join(script_dir, "../grid.png")

    with open(image_path, "rb") as img_file:
        files = {"file": ("../grid.png", img_file, "image/png")}
        response = httpx.post(REMOTE_URL, files=files)
        response.raise_for_status()
        data = response.json()

    # Validate expected keys exist
    if not all(k in data for k in ("boxes", "confidences", "class_ids")):
        raise ValueError(f"Unexpected response structure: {data}")

    detections = []
    for i, box in enumerate(data["boxes"]):
        x1, y1, x2, y2 = box
        detections.append({
            'x1': x1,
            'y1': y1,
            'x2': x2,
            'y2': y2,
            'class': int(data["class_ids"][i]),
            'conf': data["confidences"][i]
        })

    return to_2d_array(detections, rows=5, cols=5)


def main():
    try:
        print("Exporting grid from image...")
        grid = export_grid()

        print("\nExtracted Grid:")
        for row in grid:
            print(" ".join(row))
    except Exception as e:
        print(f"\n[ERROR] Failed to extract grid: {e}")

if __name__ == "__main__":
    main()

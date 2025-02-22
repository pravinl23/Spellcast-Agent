from ultralytics import YOLO

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
        row_chars = []
        for det in row_dets_sorted:
            char = CLASS_MAP.get(det['class'], '?')
            row_chars.append(char)

        grid.append(row_chars)

    return grid


def export_grid():
    # Temporary model, trained by CHY4E
    model_path = "best.pt"
    model = YOLO(model_path)

    # Retrieve results from the grid
    image_path = "grid.png"
    results = model(image_path)

    detections = []

     # Iterate over each result returned by the model
    for result in results:
        # Loop over each detected bounding box in the current result.
        for det in result.boxes:
            # Extract the coordinates for the bounding box in the format [x1, y1, x2, y2]
            # https://github.com/ultralytics/ultralytics/issues/10988
            xyxy = det.xyxy[0]
            x1, y1, x2, y2 = xyxy

            # Extract the confidence score of the detection which indicates the model's certainty
            conf = det.conf
            
            # Extract the class ID (as a float) and convert it to an integer which indicates what letter it is
            cls = int(det.cls)
            
            # Append a dictionary containing all the detection details to the 'detections' list.
            detections.append({
                'x1': x1,
                'y1': y1,
                'x2': x2,
                'y2': y2,
                'class': cls,
                'conf': conf
            })

    grid = to_2d_array(detections, rows=5, cols=5)
    
    return grid
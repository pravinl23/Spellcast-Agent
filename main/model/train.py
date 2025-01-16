from ultralytics import YOLO

# Load a YOLOv8 model (Nano version here; you can use Small, Medium, etc.)
model = YOLO('yolov8n.pt')

# Train the model
model.train(
    data='spellcast.ai/main/model/data.yaml',  # Path to data.yaml
    epochs=50,                 # Number of epochs
    imgsz=640,                 # Image size
    batch=16                   # Batch size
)

# Evaluate the model on the validation set
metrics = model.val()
print(metrics)

# Export the trained model to other formats if needed
model.export(format='onnx')  # Options include ONNX, TensorFlow, etc.

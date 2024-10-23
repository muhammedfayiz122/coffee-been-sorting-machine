from ultralytics import YOLO

# Load your trained model
model = YOLO('../models/best.pt')

# Define path to your validation dataset and other configs
data_yaml = '../data.yaml'

# Evaluate the model
results = val.run(
    data=data_yaml,             # Path to data.yaml
    weights='path/to/your/best_model.pt',  # Path to your trained weights
    imgsz=640,                  # Image size for validation (e.g., 640x640)
    conf_thres=0.001,           # Confidence threshold (default is usually 0.001)
    iou_thres=0.6,              # Intersection-over-union threshold
    device='0',                 # GPU/CPU (use '0' for GPU or 'cpu' for CPU)
    save_json=False,            # Set to True if you want to save COCO results in JSON
)

# Access the evaluation metrics
print(f"mAP (mean Average Precision): {results['mAP_0.5']}")
print(f"Precision: {results['precision']}")
print(f"Recall: {results['recall']}")
print(f"F1 Score: {results['f1']}")

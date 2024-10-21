from datasets import load_dataset
import os
import pandas as pd
from ultralytics import YOLO

# Path for the dataset
image_dir = 'datasets/data/images'
label_dir = 'datasets/data/labels'

if not os.path.exists(image_dir):
    print("Dataset not found locally, downloading from Hugging Face...")

    # Loading dataset
    ds = load_dataset("SriPrasanna/coffee-beans")

    # making folder for images and labels
    os.makedirs('datasets/data/images', exist_ok=True)
    os.makedirs('datasets/data/labels', exist_ok=True)

    # Iterate over the dataset from hugging face library and save images and labels in local
    for i, item in enumerate(ds['train']):
        image = item['image']
        image.save(f'datasets/data/images/{i}.jpg')  # Save the image

        # Assuming you have bounding box annotations (you'll need to modify this part if your dataset has different annotations)
        with open(f'datasets/data/labels/{i}.txt', 'w') as f:
            # You can adjust the following lines based on your dataset's label format
            class_id = item['label']  # Using 'label' as class id for now
            # In YOLO format, annotations need to be in [class_id, x_center, y_center, width, height] normalized format.
            # You'll need to generate these values if available.
            f.write(f'{class_id} 0.5 0.5 1.0 1.0\n')  # Placeholder annotation

#loading model
model = YOLO("yolo11n.pt")

# Train the model
model.train(data='data.yaml', epochs=50, imgsz=640, batch=16)
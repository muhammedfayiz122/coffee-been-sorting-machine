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
        image_path = f'{image_dir}/{i}.jpg'
        label_path = f'{label_dir}/{i}.txt'

        # Save the image if it doesn't already exist
        if not os.path.exists(image_path):
            image.save(image_path)  # Save the image
        else:
            print(f"Image {i}.jpg already exists, skipping download.")

        # Save the label if it doesn't already exist
        if not os.path.exists(label_path):
            with open(label_path, 'w') as f:
                class_id = item['label']  # Using 'label' as class id for now
                # Placeholder annotation in YOLO format
                f.write(f'{class_id} 0.5 0.5 1.0 1.0\n')
        else:
            print(f"Label {i}.txt already exists, skipping label creation.")
else:
    print("Dataset already exists locally. Skipping download and file creation.")

#loading model
model = YOLO("yolo11n.pt")

# Train the model
model.train(data='data.yaml', epochs=50, imgsz=640, batch=16)
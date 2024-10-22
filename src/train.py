from ultralytics import YOLO

#loading model
model = YOLO("yolo11n.pt")

# Train the model
model.train(data='../data.yaml', epochs=50, imgsz=640, batch=16)
from ultralytics import YOLO

model = YOLO("runs/detect/train7/weights/best.pt")

results=model.predict("datasets/data/images/890.jpg",imgsz=640)

for result in results:
    boxes=result.boxes
    labels=result.names
    result.show()

# print(results)



# results.save("")
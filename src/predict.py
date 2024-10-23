from ultralytics import YOLO

def predict_coffee(model_path, test_file):
    # Load the trained model
    model = YOLO(model_path)

    # Predict on a new image
    results = model.predict(test_file, imgsz=640)

    # # Visualize the result
    # results.show()

    # # Save the predicted image with bounding boxes
    # results.save("output/")
    return results

def main():
    model_path = "../models/best.pt"
    test_file = "../test/1397.jpg"
    try:
        output = predict_coffee(model_path, test_file)
    except Exception as e:
        print(f"an error occured : {e}")
    output.show()
    print(output)

if __name__ == "__main__":
    main()
import kagglehub

# Download latest version
path = kagglehub.dataset_download("gpiosenka/coffee-bean-dataset-resized-224-x-224")

print("Path to dataset files:", path)
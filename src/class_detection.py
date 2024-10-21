import os

label_folder = '../datasets/data/labels'  # Replace with your label folder path
classes = set()

# Loop through all label files in the folder
for label_file in os.listdir(label_folder):
    if label_file.endswith('.txt'):  # Check if the file is a label file
        with open(os.path.join(label_folder, label_file), 'r') as file:
            for line in file:
                class_id = int(line.split()[0])  # Get the class ID
                classes.add(class_id)  # Add class ID to the set

# Print the number of classes and the unique class IDs found
print(f'Number of classes: {len(classes)}')
print(f'Classes found: {sorted(classes)}')

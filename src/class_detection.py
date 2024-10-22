import os

def get_unique_classes(label_folder):
    """
    Reads all label files in the given folder, extracts unique class IDs, 
    and returns the number of classes and the sorted list of unique class IDs.
    
    Parameters:
    - label_folder (str): Path to the folder containing label files (.txt format)
    
    Returns:
    - int: The number of unique classes found
    - list: A sorted list of unique class IDs
    """
    classes = set()

    # Loop through all label files in the folder
    for label_file in os.listdir(label_folder):
        if label_file.endswith('.txt'):  # Check if the file is a label file
            file_path = os.path.join(label_folder, label_file)
            try:
                with open(file_path, 'r') as file:
                    for line in file:
                        # Assume the first number on each line is the class ID
                        class_id = int(line.split()[0])  
                        classes.add(class_id)
            except Exception as e:
                print(f"Error reading file {file_path}: {e}")

    return len(classes), sorted(classes)

def main():
    # Example usage with a predefined path (can be replaced with an argument)
    label_folder = '../datasets/data/labels'  # Replace with the actual path
    
    try:
        num_classes, class_ids = get_unique_classes(label_folder)
        print(f'Number of classes: {num_classes}')
        print(f'Classes found: {class_ids}')
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == '__main__':
    main()
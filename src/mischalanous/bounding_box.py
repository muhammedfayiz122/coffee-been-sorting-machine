import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Load the image
image_path = '0.jpg'
img = Image.open(image_path)
width, height = img.size

# Normalized bounding box (center_x, center_y, width, height)
bbox = [963.8926, 515.6296, 110.1707,  76.6236]  # (center_x, center_y, width, height)

# Denormalize bounding box (convert to pixel values)
center_x = bbox[0] * width
center_y = bbox[1] * height
box_width = bbox[2] * width
box_height = bbox[3] * height

# Calculate top-left corner
x_min = center_x - (box_width / 2)
y_min = center_y - (box_height / 2)

# Plot the image
fig, ax = plt.subplots(1)
ax.imshow(img)

# Create a Rectangle patch
rect = patches.Rectangle((x_min, y_min), box_width, box_height, linewidth=2, edgecolor='r', facecolor='none')

# Add the rectangle to the plot
ax.add_patch(rect)

plt.show()

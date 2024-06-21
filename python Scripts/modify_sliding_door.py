import matplotlib.pyplot as plt
import matplotlib.patches as patches
from PIL import Image

# Load image
image_path = 'SlidingDoor.png'
image = Image.open(image_path)

# Create figure and axes
fig, ax = plt.subplots()
ax.imshow(image)

# Add annotations for the automatic sliding door
rect = patches.Rectangle((200, 100), 150, 50, linewidth=2, edgecolor='r', facecolor='none')
ax.add_patch(rect)
ax.text(200, 90, 'Automatic Sliding Door', color='red', fontsize=12)

# Add annotations for the RFID receiver
circle = patches.Circle((350, 125), 10, color='blue')
ax.add_patch(circle)
ax.text(360, 120, 'RFID Receiver', color='blue', fontsize=12)

# Add arrow pointing to the microcontroller
ax.arrow(350, 130, 20, 20, head_width=5, head_length=5, fc='blue', ec='blue')
ax.text(370, 150, 'Microcontroller', color='blue', fontsize=12)

# Display the modified image
plt.axis('off')
plt.show()
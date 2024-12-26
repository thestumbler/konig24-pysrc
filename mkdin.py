
import numpy as np
import matplotlib.pyplot as plt

from PIL import Image
from matplotlib.offsetbox import AnnotationBbox, OffsetImage



# Parameters for the DIN meter scale
#k = 2.5  # Compression parameter
#p = 1.7  # Power factor
#A = 100  # Angular span in degrees
k = 1.4  # Compression parameter
p = 2.3  # Power factor
A = 100  # Angular span in degrees

# Scale values in dB
db_values = np.array([-50, -40, -30, -20, -10, -5, 0, 5])

# Function to calculate angular positions based on dB values
def db_to_angle(db, k, p, A):
    normalized = (db - db_values.min()) / (db_values.max() - db_values.min())  # Normalize dB range
    return -A / 2 + A * (1 - np.exp(-k * normalized**p)) / (1 - np.exp(-k))  # Apply compression formula

# Calculate angles for each dB value
angles = db_to_angle(db_values, k, p, A)

print(angles)

# Start plotting
# fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
fig, ax = plt.subplots(figsize=(12, 8))

# Don't mess with the limits!
plt.xlim(-75, 75)
plt.ylim(0, 2)
plt.autoscale(False)
#ax.set_aspect('equal', 'box')
ax.axis('off')

# Load logo image
w, h = 3777, 393
zoom = 0.16
xyruler = (0.10, 0.35)

image_path = "din-sample.png"
image_data = Image.open(image_path).convert('RGBA')
zoom_factor = min(w / image_data.width, h / image_data.height) * zoom
image_box = OffsetImage(image_data, zoom=zoom_factor)
anno_box = AnnotationBbox(image_box, 
                          xy=xyruler, xycoords='axes fraction', 
                          box_alignment=(0.0, 0.5), frameon=False)

# Convert angles to radians for polar plot
# angles_rad = np.deg2rad(angles)
angles_rad = angles

# Plot the scale markings
for angle, db in zip(angles_rad, db_values):
    ax.plot([angle, angle], [0.8, 1.0], color='black', lw=1)  # Tick marks
    ax.text(
        angle, 1.1, f"{db} dB", horizontalalignment='center', 
        verticalalignment='center', fontsize=10,
        rotation = 90
    )  # Label

# Add colored ranges for visual emphasis
ax.fill_between(np.linspace(angles_rad[0], angles_rad[-1], 500), 0.8, 1.0, color='yellow', alpha=0.3)
ax.fill_between(np.linspace(angles_rad[-2], angles_rad[-1], 500), 0.8, 1.0, color='red', alpha=0.5)


ax.add_artist(anno_box)

plt.show()

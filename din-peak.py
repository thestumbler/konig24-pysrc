import numpy as np
import matplotlib.pyplot as plt

# Parameters for the DIN meter scale
k = 2.5  # Compression parameter
p = 1.7  # Power factor
A = 100  # Angular span in degrees

# Scale values in dB
db_values = np.array([-50, -40, -30, -20, -10, -5, 0, 5])

# Function to calculate angular positions based on dB values
def db_to_angle(db, k, p, A):
    normalized = (db - db_values.min()) / (db_values.max() - db_values.min())  # Normalize dB range
    return -A / 2 + A * (1 - np.exp(-k * normalized**p)) / (1 - np.exp(-k))  # Apply compression formula

# Calculate angles for each dB value
angles = db_to_angle(db_values, k, p, A)

# Start plotting
# fig, ax = plt.subplots(figsize=(8, 8), subplot_kw={'projection': 'polar'})
fig, ax = plt.subplots(figsize=(12, 8))

# Convert angles to radians for polar plot
# angles_rad = np.deg2rad(angles)
angles_rad = angles

# Plot the scale markings
for angle, db in zip(angles_rad, db_values):
    ax.plot([angle, angle], [0.8, 1.0], color='black', lw=1)  # Tick marks
    ax.text(
        angle, 1.1, f"{db} dB", horizontalalignment='center', verticalalignment='center', fontsize=10
    )  # Label

# Add colored ranges for visual emphasis
ax.fill_between(np.linspace(angles_rad[0], angles_rad[-1], 500), 0.8, 1.0, color='yellow', alpha=0.3)
ax.fill_between(np.linspace(angles_rad[-2], angles_rad[-1], 500), 0.8, 1.0, color='red', alpha=0.5)

# Add center circle for the needle pivot
ax.scatter(0, 0, s=50, color='black')

# Adjust plot appearance
ax.set_ylim(0, 1.2)
ax.axis('off')  # Turn off polar grid
ax.set_title("DIN 60268-10 Type I Meter Face", va='bottom', fontsize=14)

plt.show()

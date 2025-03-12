import time
from huskylib import HuskyLensLibrary
import numpy as np

# Initialize HuskyLens (adjust port as needed)
hl = HuskyLensLibrary("SERIAL", "/dev/tty.usbserial-11420", 3000000)

width_physical = 43 # width of the square for calibration, cm
height_physical = 43 # height of the square for calibration, cm

cm_per_pixel_x_all = []
cm_per_pixel_y_all = []

def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)

def calculate_width_height(corners):
    distances = []
    for i in range(4):
        for j in range(i + 1, 4):
            dist = euclidean_distance(corners[i], corners[j])
            distances.append((dist, (i, j)))  # Store the distance and point indices

    # Sort distances in descending order
    distances.sort(reverse=True, key=lambda x: x[0])

    width = (distances[2][0]+ distances[3][0]) / 2
    height = (distances[4][0]+ distances[5][0]) / 2

    return width, height

print("Calibrating camera resolution with April Tag... Press Ctrl+C to stop.")

try:
    while True:
        tag = hl.requestAll()
        if tag and isinstance(tag, list):
            if len(tag) == 4:
                corners = []
                print("Detected 4 tags")
                for obj in tag:
                    if obj.type == "BLOCK":  # Ensure we're tracking a block/tag
                        print(f"Tag Position -> X: {obj.x:d}, Y: {obj.y:d}")
                        corners.append((obj.x, obj.y))

                width, height = calculate_width_height(corners)
                print(f"Detected length in pixel -> width: {width:.2f}, height: {height:.2f}")

                cm_per_pixel_x = width_physical / width
                cm_per_pixel_y = height_physical / height
                cm_per_pixel_x_all.append(cm_per_pixel_x)
                cm_per_pixel_y_all.append(cm_per_pixel_y)
                print(f"cm_per_pixel_x: {cm_per_pixel_x:.3f}, cm_per_pixel_y: {cm_per_pixel_y:.3f}")

        time.sleep(0.1)  # Reduce CPU usage
except KeyboardInterrupt:
    print("\nCalibration stopped.")
    print("Camera spatial resolution:")
    cm_per_pixel_x_mean = sum(cm_per_pixel_x_all)/len(cm_per_pixel_x_all)
    cm_per_pixel_y_mean = sum(cm_per_pixel_y_all)/len(cm_per_pixel_y_all)
    print(f"cm_per_pixel_x: {cm_per_pixel_x_mean:.3f}, cm_per_pixel_y: {cm_per_pixel_y_mean:.3f}")

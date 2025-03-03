import time
from huskylib import HuskyLensLibrary

# Initialize HuskyLens (adjust port as needed)
hl = HuskyLensLibrary("SERIAL", "/dev/cu.usbserial-110", 3000000)

# Calibration values: You must measure these for your setup
frame_width_cm = 30  # Physical width of the tracked area in cm
frame_height_cm = 20  # Physical height of the tracked area in cm
husky_width_pixels = 320  # HuskyLens resolution (default 320x240)
husky_height_pixels = 240

# Compute conversion factors
cm_per_pixel_x = frame_width_cm / husky_width_pixels
cm_per_pixel_y = frame_height_cm / husky_height_pixels

print("Tracking tag position in cm... Press Ctrl+C to stop.")

try:
    while True:
        tag = hl.requestAll()
        if tag and isinstance(tag, list):
            for obj in tag:
                if obj.type == "BLOCK":  # Ensure we're tracking a block/tag
                    x_cm = obj.x * cm_per_pixel_x
                    y_cm = obj.y * cm_per_pixel_y
                    print(f"Tag Position -> X: {x_cm:.2f} cm, Y: {y_cm:.2f} cm")
        time.sleep(0.1)  # Reduce CPU usage
except KeyboardInterrupt:
    print("\nTracking stopped.")
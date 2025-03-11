import time
from huskylib import HuskyLensLibrary

# Initialize HuskyLens (adjust port as needed)
hl = HuskyLensLibrary("SERIAL", "/dev/cu.usbserial-110", 3000000)

# Input calibration result
cm_per_pixel_x = 0.1
cm_per_pixel_y = 0.1

print("Tracking robot position in cm... Press Ctrl+C to stop.")

try:
    while True:
        tag = hl.requestAll()
        if tag and isinstance(tag, list):
            for obj in tag:
                if obj.type == "BLOCK":  # Ensure we're tracking a block/tag
                    x_cm = obj.x * cm_per_pixel_x
                    y_cm = obj.y * cm_per_pixel_y
                    print(f"Robot Position -> X: {x_cm:.2f} cm, Y: {y_cm:.2f} cm")
        time.sleep(0.1)  # Reduce CPU usage
except KeyboardInterrupt:
    print("\nTracking stopped.")

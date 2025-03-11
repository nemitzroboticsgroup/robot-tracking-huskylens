import time
from huskylib import HuskyLensLibrary

# Initialize HuskyLens (adjust port as needed)
hl = HuskyLensLibrary("SERIAL", "/dev/tty.usbserial-1430", 3000000)

x_diff_physical = 70 # width of the square for calibration, cm
y_diff_physical = 70 # height of the square for calibration, cm

cm_per_pixel_x_all = []
cm_per_pixel_y_all = []

print("Calibrating camera resolution with April Tag... Press Ctrl+C to stop.")

try:
    while True:
        tag = hl.requestAll()
        if tag and isinstance(tag, list):
            if len(tag) == 4:
                x_all = []
                y_all = []
                print("Detected 4 tags")
                for obj in tag:
                    if obj.type == "BLOCK":  # Ensure we're tracking a block/tag
                        print(f"Tag Position -> X: {obj.x:d}, Y: {obj.y:d}")
                        x_all.append(obj.x)
                        y_all.append(obj.y)

                x_diff_img = ((x_all[1]-x_all[0]) + (x_all[3]-x_all[2])) / 2
                y_diff_img = ((y_all[2]-y_all[0]) + (y_all[3]-y_all[1])) / 2
                print(f"x_diff: {x_diff_img:.1f}, y_diff: {y_diff_img:.1f}")

                cm_per_pixel_x = x_diff_physical / x_diff_img
                cm_per_pixel_y = y_diff_physical / y_diff_img
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

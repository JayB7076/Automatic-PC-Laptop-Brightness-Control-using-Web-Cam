import cv2
import numpy as np
import screen_brightness_control as sbc

def set_camera_settings(camera, exposure_value=-6):
    print("CAM in Manual Exposure Mode")
    camera.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.25)  # Set manual exposure mode
    camera.set(cv2.CAP_PROP_EXPOSURE, exposure_value)

def calculate_brightness(frame):
    # Convert the frame to grayscale
    gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    # Calculate the average intensity (brightness)
    brightness = np.mean(gray_frame)
    return brightness

def map_brightness_to_screen(brightness):
    screen_brightness = int((brightness / 255) * 100)
    return screen_brightness

def smooth_brightness(previous_brightness, new_brightness, smoothing_factor=0.1):
    smoothed_brightness = previous_brightness * (1 - smoothing_factor) + new_brightness * smoothing_factor
    return smoothed_brightness

# Open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Unable to access the camera.")
else:
    print("Press 'q' to exit.")

    # initial exposure value
    exposure_value = -1.5  # Change Exposure of Web CAM Accordingly.

    # initial camera settings
    set_camera_settings(cap, exposure_value)

    # Initialize previous brightness to avoid any unexpected change at the start
    previous_brightness = 50  # Starting from a middle value (50%)
    
    while True:
        # Reads the frame from the camera
        ret, frame = cap.read()
        if not ret:
            print("Error: Unable to capture video.")
            break

        # Calculate light intensity from the frame
        light_intensity = calculate_brightness(frame)
        
        # Map light intensity to screen brightness (0-100)
        screen_brightness = map_brightness_to_screen(light_intensity)

        # Apply smoothing to the brightness control
        smoothed_brightness = smooth_brightness(previous_brightness, screen_brightness)

        # Set the smoothed brightness using the screen-brightness-control library
        sbc.set_brightness(int(smoothed_brightness))

        # Update previous brightness for the next iteration
        previous_brightness = smoothed_brightness

        # Display the light intensity and current screen brightness on the video feed
        text = f"Light Intensity: {light_intensity:.2f} | Screen Brightness: {int(smoothed_brightness)}%"
        text += f" | Exposure: {exposure_value}"  # Fixed manual exposure value
        
        cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

        # Show the video feed
        cv2.imshow('Camera - Manual Exposure and Auto Brightness', frame)
        key = cv2.waitKey(1) & 0xFF

        if key == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()
import cv2
import numpy as np
import pyautogui

# Initialize webcam
cap = cv2.VideoCapture(0)

# Get screen size
screen_w, screen_h = pyautogui.size()

# --- Color thresholds ---
# Red LED detection
lower_red1 = np.array([0, 150, 150])
upper_red1 = np.array([10, 255, 255])
lower_red2 = np.array([170, 150, 150])
upper_red2 = np.array([180, 255, 255])

# Blue corner detection
lower_blue = np.array([100, 150, 50])
upper_blue = np.array([140, 255, 255])

# Morphology kernel for noise removal
kernel = np.ones((5, 5), np.uint8)

# CALIBRATION ---
print("[INFO] Please project 4 bright blue points at the 4 corners of your monitor...")


matrix = None
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Detecting blue points
    mask_blue = cv2.inRange(hsv, lower_blue, upper_blue)
    mask_blue = cv2.GaussianBlur(mask_blue, (7, 7), 0)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_OPEN, kernel)
    mask_blue = cv2.morphologyEx(mask_blue, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(mask_blue, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    blue_points = []

    for cnt in contours:
        area = cv2.contourArea(cnt)
        if area > 20:
            x, y, w, h = cv2.boundingRect(cnt)
            cx, cy = x + w/2, y + h/2
            blue_points.append([cx, cy])
            cv2.circle(frame, (int(cx), int(cy)), 5, (255, 0, 0), -1)

    cv2.putText(frame, f"Blue Points: {len(blue_points)} / 4", (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

    cv2.imshow("Calibration - Detecting Monitor Corners", frame)

    # Waiting until 4 points are detected
    if len(blue_points) == 4:
        print("[INFO] 4 corners detected! Calibrating...")
        blue_points = np.array(sorted(blue_points, key=lambda p: (p[1], p[0])), dtype=np.float32)

        # Sorting points
        top_points = sorted(blue_points[:2], key=lambda p: p[0])
        bottom_points = sorted(blue_points[2:], key=lambda p: p[0])
        src_pts = np.array([top_points[0], top_points[1], bottom_points[1], bottom_points[0]], dtype=np.float32)

        dst_pts = np.array([[0, 0],
                            [screen_w, 0],
                            [screen_w, screen_h],
                            [0, screen_h]], dtype=np.float32)

        matrix = cv2.getPerspectiveTransform(src_pts, dst_pts)
        print("[INFO] Calibration complete.")
        break

    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("[INFO] Calibration cancelled.")
        cap.release()
        cv2.destroyAllWindows()
        exit()

cv2.destroyAllWindows()

# LED TRACKING ---
print("[INFO] Tracking red LED... Press 'ctrl+C' to quit.")

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Red detection
    mask1 = cv2.inRange(hsv, lower_red1, upper_red1)
    mask2 = cv2.inRange(hsv, lower_red2, upper_red2)
    mask = cv2.bitwise_or(mask1, mask2)

    # Brightness filter
    v = cv2.split(hsv)[2]
    _, bright = cv2.threshold(v, 200, 255, cv2.THRESH_BINARY)
    mask = cv2.bitwise_and(mask, bright)

    # Noise reduction
    mask = cv2.GaussianBlur(mask, (7, 7), 0)
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, kernel)
    mask = cv2.morphologyEx(mask, cv2.MORPH_DILATE, kernel)

    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    if contours:
        contour = max(contours, key=cv2.contourArea)
        area = cv2.contourArea(contour)

        if 50 < area < 500:
            x, y, w, h = cv2.boundingRect(contour)
            cx, cy = x , y #center tracing not convenient                  

            # Transform LED point using perspective mapping
            led_point = np.array([[[cx, cy]]], dtype=np.float32)
            mapped_point = cv2.perspectiveTransform(led_point, matrix)
            screen_x, screen_y = mapped_point[0][0]

            # Draw visualization
            #cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            #cv2.circle(frame, (int(cx), int(cy)), 5, (255, 0, 0), -1)

            # Move mouse only if inside screen bounds
            if 0 <= screen_x <= screen_w and 0 <= screen_y <= screen_h:
                pyautogui.moveTo(screen_x, screen_y, duration=0.01)

    #cv2.imshow("LED Tracker", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()

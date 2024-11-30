import cv2
import mediapipe as mp
import pyautogui
import numpy as np
import time

# Initialize MediaPipe Hands
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7, min_tracking_confidence=0.5)
mp_drawing = mp.solutions.drawing_utils

# Get screen width and height
screen_width, screen_height = pyautogui.size()

# Sensitivity multiplier
sensitivity = 1.0

# Capture video from webcam
cap = cv2.VideoCapture(1)

while True:
    start_time = time.time()  # Start timing for performance measurement

    # Read a frame from the webcam
    ret, frame = cap.read()
    if not ret:
        break

    # Flip the frame horizontally for natural interaction
    frame = cv2.flip(frame, 1)

    # Reduce frame size to speed up processing
    small_frame = cv2.resize(frame, (320, 240))

    # Convert the frame to RGB
    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)

    # Process the frame with MediaPipe Hands
    results = hands.process(rgb_frame)

    # If hands are detected, get landmarks
    if results.multi_hand_landmarks:
        for hand_landmarks in results.multi_hand_landmarks:
            # Get coordinates of index finger tip (landmark 8)
            index_finger_tip = hand_landmarks.landmark[8]
            x, y = int(index_finger_tip.x * screen_width), int(index_finger_tip.y * screen_height)

            # Apply sensitivity multiplier
            x *= sensitivity
            y *= sensitivity

            # Move the mouse
            pyautogui.moveTo(x, y)

            # Optional: Detect click gesture (e.g., by checking distance between thumb and index finger)
            thumb_tip = hand_landmarks.landmark[4]
            thumb_x, thumb_y = int(thumb_tip.x * screen_width), int(thumb_tip.y * screen_height)
            distance = np.hypot(x - thumb_x, y - thumb_y)

            # Click detection with a threshold
            if distance < 50:
                pyautogui.click()

            # Draw landmarks and connections on the frame
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # Display the frame with sensitivity info
    cv2.putText(frame, f'Sensitivity: {sensitivity:.1f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
    cv2.imshow('Virtual Mouse', frame)

    # Adjust sensitivity with 'a' and 'd' keys
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q'):
        break
    elif key == ord('a'):
        sensitivity = max(1.0, sensitivity - 0.1)
    elif key == ord('d'):
        sensitivity = min(5.0, sensitivity + 0.1)

    # Performance measurement
    elapsed_time = time.time() - start_time
    print(f"Frame processing time: {elapsed_time:.3f} seconds")

# Release the webcam and close the window
cap.release()
cv2.destroyAllWindows()
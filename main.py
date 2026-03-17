import cv2
from hand_tracking import HandTracker
import time

# Webcam
cap = cv2.VideoCapture(0)

# Hand tracker
tracker = HandTracker()

blocks = []
last_add_time = 0
cooldown = 0.3  # seconds to prevent spam

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.find_hand(frame)

    if landmarks:
        h, w, _ = frame.shape

        # Index finger tip position
        cx = int(landmarks[8].x * w)
        cy = int(landmarks[8].y * h)

        current_time = time.time()

        # 🤏 Pinch → add block (with cooldown)
        if tracker.is_pinch(landmarks):
            if current_time - last_add_time > cooldown:
                blocks.append((cx, cy))
                last_add_time = current_time

        # ✊ Fist → delete last block
        if tracker.is_fist(landmarks):
            if blocks:
                blocks.pop()
                time.sleep(0.2)  # prevent rapid delete

        # Draw cursor
        cv2.circle(frame, (cx, cy), 10, (255, 0, 0), -1)

    # 🧊 Draw blocks ON CAMERA
    for (x, y) in blocks:
        # Draw cube-like effect (fake 3D)
        cv2.rectangle(frame, (x, y), (x+30, y+30), (0, 255, 0), -1)
        cv2.rectangle(frame, (x+5, y-5), (x+35, y+25), (0, 200, 0), 2)

    # Show camera with blocks
    cv2.imshow("AR Gesture Block Builder", frame)

    # Exit with ESC
    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

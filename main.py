import cv2
from hand_tracking import HandTracker
import time

# Webcam
cap = cv2.VideoCapture(0)

# Hand tracker
tracker = HandTracker()

blocks = set()  # use set to avoid duplicates

GRID_SIZE = 40  # size of each block
last_add_time = 0
cooldown = 0.3

while True:
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.find_hand(frame)

    if landmarks:
        h, w, _ = frame.shape

        # finger position
        cx = int(landmarks[8].x * w)
        cy = int(landmarks[8].y * h)

        # 🔥 SNAP TO GRID
        grid_x = (cx // GRID_SIZE) * GRID_SIZE
        grid_y = (cy // GRID_SIZE) * GRID_SIZE

        current_time = time.time()

        # 🤏 Pinch → add block
        if tracker.is_pinch(landmarks):
            if current_time - last_add_time > cooldown:
                blocks.add((grid_x, grid_y))
                last_add_time = current_time

        # ✊ Fist → remove block
        if tracker.is_fist(landmarks):
            if (grid_x, grid_y) in blocks:
                blocks.remove((grid_x, grid_y))
                time.sleep(0.2)

        # Cursor (snapped)
        cv2.rectangle(frame, (grid_x, grid_y), 
                      (grid_x + GRID_SIZE, grid_y + GRID_SIZE), 
                      (255, 0, 0), 2)

    # 🧊 Draw grid (optional but cool)
    for x in range(0, w, GRID_SIZE):
        cv2.line(frame, (x, 0), (x, h), (50, 50, 50), 1)
    for y in range(0, h, GRID_SIZE):
        cv2.line(frame, (0, y), (w, y), (50, 50, 50), 1)

    # 🧊 Draw blocks
    for (x, y) in blocks:
        cv2.rectangle(frame, (x, y), 
                      (x + GRID_SIZE, y + GRID_SIZE), 
                      (0, 255, 0), -1)

        # fake 3D shading
        cv2.rectangle(frame, (x, y), 
                      (x + GRID_SIZE, y + GRID_SIZE), 
                      (0, 200, 0), 2)

    cv2.imshow("Minecraft Style Builder", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()

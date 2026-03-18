from ursina import *
import cv2
from hand_tracking import HandTracker

app = Ursina()

# Camera
camera.position = (0, 10, -20)
camera.rotation_x = 30

# Hand tracking
cap = cv2.VideoCapture(0)
tracker = HandTracker()

blocks = {}
GRID_SIZE = 1

def update():
    global blocks

    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.find_hand(frame)

    if landmarks:
        h, w, _ = frame.shape

        cx = int(landmarks[8].x * w)
        cy = int(landmarks[8].y * h)

        # Convert to 3D grid
        gx = int(cx / 40)
        gz = int(cy / 40)
        gy = 0  # ground level

        pos = (gx, gy, gz)

        # 🤏 Pinch → place block
        if tracker.is_pinch(landmarks):
            if pos not in blocks:
                block = Entity(
                    model='cube',
                    color=color.green,
                    position=pos,
                    scale=1
                )
                blocks[pos] = block

        # ✊ Fist → remove block
        if tracker.is_fist(landmarks):
            if pos in blocks:
                destroy(blocks[pos])
                del blocks[pos]

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        application.quit()

app.run()

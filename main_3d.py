from ursina import *
import cv2
from hand_tracking import HandTracker

app = Ursina()

# Scene lighting
DirectionalLight().look_at(Vec3(1,-1,-1))
Sky()

# Camera setup
camera.position = (0, 10, -20)
camera.rotation_x = 30

# Ground plane (IMPORTANT so you see something)
ground = Entity(model='plane', scale=50, color=color.gray)

# Hand tracking
cap = cv2.VideoCapture(0)
tracker = HandTracker()

blocks = {}

def update():
    global blocks

    if not cap.isOpened():
        return

    success, frame = cap.read()
    if not success:
        return

    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.find_hand(frame)

    if landmarks:
        h, w, _ = frame.shape

        cx = int(landmarks[8].x * w)
        cy = int(landmarks[8].y * h)

        gx = int(cx / 40)
        gz = int(cy / 40)
        gy = 0

        pos = (gx, gy, gz)

        # 🤏 Place block
        if tracker.is_pinch(landmarks):
            if pos not in blocks:
                blocks[pos] = Entity(
                    model='cube',
                    color=color.azure,
                    position=pos,
                    scale=1
                )

        # ✊ Delete block
        if tracker.is_fist(landmarks):
            if pos in blocks:
                destroy(blocks[pos])
                del blocks[pos]

    cv2.imshow("Camera", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        application.quit()

app.run()

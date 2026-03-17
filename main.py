import cv2
import pygame
from hand_tracking import HandTracker

# Initialize pygame
pygame.init()
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Gesture Block Builder")

# Webcam
cap = cv2.VideoCapture(0)

# Hand tracker
tracker = HandTracker()

blocks = []

running = True

while running:
    # Read camera
    success, frame = cap.read()
    frame = cv2.flip(frame, 1)

    frame, landmarks = tracker.find_hand(frame)

    cx, cy = None, None

    if landmarks:
        # Use index finger tip
        cx = int(landmarks[8].x * WIDTH)
        cy = int(landmarks[8].y * HEIGHT)

        # Pinch → add block
        if tracker.is_pinch(landmarks):
            if (cx, cy) not in blocks:
                blocks.append((cx, cy))

        # Fist → delete last block
        if tracker.is_fist(landmarks):
            if blocks:
                blocks.pop()

    # Draw
    screen.fill((0, 0, 0))

    for block in blocks:
        pygame.draw.rect(screen, (0, 255, 0), (block[0], block[1], 20, 20))

    # Show camera feed (optional overlay window)
    cv2.imshow("Camera", frame)

    pygame.display.flip()

    # Exit controls
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if cv2.waitKey(1) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
pygame.quit()

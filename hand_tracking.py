import cv2
import mediapipe as mp
import math

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(max_num_hands=1)
        self.mp_draw = mp.solutions.drawing_utils

    def find_hand(self, img):
        imgRGB = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        results = self.hands.process(imgRGB)

        landmarks = []

        if results.multi_hand_landmarks:
            for handLms in results.multi_hand_landmarks:
                for id, lm in enumerate(handLms.landmark):
                    landmarks.append(lm)

                self.mp_draw.draw_landmarks(img, handLms, self.mp_hands.HAND_CONNECTIONS)

        return img, landmarks

    def is_pinch(self, landmarks):
        if len(landmarks) < 9:
            return False

        x1, y1 = landmarks[4].x, landmarks[4].y   # thumb tip
        x2, y2 = landmarks[8].x, landmarks[8].y   # index tip

        distance = math.hypot(x2 - x1, y2 - y1)
        return distance < 0.05

    def is_fist(self, landmarks):
        if len(landmarks) < 9:
            return False

        # index finger tip below middle joint = folded
        return landmarks[8].y > landmarks[6].y

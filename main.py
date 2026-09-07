import cv2
import mediapipe as mp
import time

from gesture_recognizer import detect_gesture
from portal import Portal

import tkinter as tk

# ---------------- Screen Utilities ----------------
def resize_to_screen(frame, screen_w, screen_h):
    """
    Resize frame while preserving aspect ratio.
    """
    h, w = frame.shape[:2]

    scale = min(screen_w / w, screen_h / h)

    new_w = int(w * scale)
    new_h = int(h * scale)

    return cv2.resize(frame, (new_w, new_h))

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0)

# ---------------- Screen Size ----------------
root = tk.Tk()
root.withdraw()

SCREEN_W = int(root.winfo_screenwidth() * 0.8)
SCREEN_H = int(root.winfo_screenheight() * 0.8)

root.destroy()

if not cap.isOpened():
    print("Cannot open camera")
    exit()

# ---------------- MediaPipe ----------------
mp_hands = mp.solutions.hands

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

mp_draw = mp.solutions.drawing_utils

# ---------------- Background Capture ----------------
print("Stand away from camera...")

for i in range(3, 0, -1):
    print(i)
    time.sleep(1)

ret, background = cap.read()

if not ret:
    print("Failed to capture background.")
    cap.release()
    exit()

background = cv2.flip(background, 1)

# ---------------- Portal ----------------
portal = Portal(radius=120)

# ---------------- Gesture State ----------------
last_triggered_gesture = None
gesture_stable_count = 0
current_stable_gesture = None
gesture_cooldown = 0

# ---------------- Portal State ----------------
portal_visible = True
portal_paused = False
gesture_message = None
gesture_message_timer = 0



# ---------------- Window ----------------
WINDOW_NAME = "AI Magic Invisibility Portal"

cv2.namedWindow(WINDOW_NAME, cv2.WINDOW_NORMAL)
cv2.resizeWindow(WINDOW_NAME, SCREEN_W, SCREEN_H)

# FIX: Initialize fullscreen state outside the loop so it doesn't reset every frame
fullscreen = False

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    results = hands.process(rgb)

    h, w = frame.shape[:2]

    if results.multi_hand_landmarks:

        hand = results.multi_hand_landmarks[0]

        mp_draw.draw_landmarks(
            frame,
            hand,
            mp_hands.HAND_CONNECTIONS
        )

        # Index Finger
        tip = hand.landmark[8]

        # Thumb
        thumb = hand.landmark[4]

        # Portal Position
        x = int(tip.x * w)
        y = int(tip.y * h)

        portal.update(x, y)

        # Portal Radius
        distance = ((tip.x - thumb.x) ** 2 + (tip.y - thumb.y) ** 2) ** 0.5

        radius = int(distance * 500)

        portal.set_radius(radius)

        # ---------------- Gesture Detection ----------------
        handedness = results.multi_handedness[0].classification[0].label
        gesture = detect_gesture(hand, handedness)

        # Gesture stability check
        if gesture == current_stable_gesture and gesture is not None:
            gesture_stable_count += 1
        else:
            current_stable_gesture = gesture
            gesture_stable_count = 1

        # Gesture cooldown
        if gesture_cooldown > 0:
            gesture_cooldown -= 1

        # Execute gesture if stable and not on cooldown
        if gesture_stable_count >= 5 and gesture_cooldown == 0:

            if gesture == "ok":

                print("Stand away from camera...")
                time.sleep(2)

                ret, bg = cap.read()

                if ret:
                    background = cv2.flip(bg, 1)
                    print("Background Updated Successfully!")
                    gesture_message = "Gesture: OK Sign\nAction: Background Captured"
                    gesture_message_timer = 60

            elif gesture == "peace":

                portal_visible = not portal_visible
                gesture_message = "Gesture: Peace\nAction: Portal " + ("Hidden" if not portal_visible else "Visible")
                gesture_message_timer = 60

            elif gesture == "fist":

                portal_paused = not portal_paused
                gesture_message = "Gesture: Fist\nAction: Portal " + ("Paused" if portal_paused else "Resumed")
                gesture_message_timer = 60

            elif gesture == "open_palm":

                portal_visible = True
                portal_paused = False
                gesture_message = "Gesture: Open Palm\nAction: Reset"
                gesture_message_timer = 60

            last_triggered_gesture = gesture
            gesture_cooldown = 30
            gesture_stable_count = 0

    # ---------------- Draw Portal ----------------
    if portal_visible:
        frame = portal.draw(frame, background)

    # ---------------- Title ----------------
    cv2.putText(
        frame,
        "AI Magic Invisibility Portal",
        (20, 40),
        cv2.FONT_HERSHEY_DUPLEX,
        0.9,
        (255, 255, 255),
        2,
        cv2.LINE_AA
    )

    #----------------- C=Change Shape -----------
    cv2.putText(
    frame,
    f"Portal Shape : {portal.get_shape().title()}",
    (20, 130),
    cv2.FONT_HERSHEY_SIMPLEX,
    0.6,
    (0,255,255),
    2,
    cv2.LINE_AA
)
    # ---------------- Developer ----------------
    cv2.putText(
        frame,
        "Developed by Sanya Rathore",
        (20, 70),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (0, 255, 255),
        2,
        cv2.LINE_AA
    )

    # ---------------- Controls ----------------
    cv2.putText(
    frame, "Move: Index | Size: Thumb | B=Capture | C=Shape | V=Color | F=Fitscreen | Q=Quit",
    (20, 100),
    cv2.FONT_HERSHEY_SIMPLEX, 0.55,
    (200, 200, 200), 1,
    cv2.LINE_AA
    )

    # ---------------- Gesture Feedback ----------------
    if gesture_message_timer > 0:
        gesture_message_timer -= 1

        lines = gesture_message.split("\n")
        y_offset = 160

        for line in lines:
            cv2.putText(
                frame,
                line,
                (20, y_offset),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 255),
                2,
                cv2.LINE_AA
            )
            y_offset += 25

    # ---------------- Watermark ----------------
    cv2.putText(
        frame,
        "© Sanya Rathore",
        (frame.shape[1] - 190, frame.shape[0] - 20),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (180, 180, 180),
        2,
        cv2.LINE_AA
    )

    display_frame = resize_to_screen(frame, SCREEN_W, SCREEN_H)

    cv2.imshow("AI Magic Invisibility Portal", display_frame)


    # FIX: Use elif statements for all key checks to avoid execution overlap
    key = cv2.waitKey(1) & 0xFF
    
    # ---------------- Toggle Fullscreen ----------------
    if key == ord("f"):

        fullscreen = not fullscreen

        if fullscreen:
            cv2.resizeWindow(WINDOW_NAME, 1920, 1080)
        else:
            cv2.resizeWindow(WINDOW_NAME, 1000, 700)

    #------------- Change Shape -----------------------------
    elif key == ord("c"):
        portal.next_shape()

    #------------- Change Color -----------------------------
    elif key == ord("v"):
        portal.next_color()

    # ---------------- Re-Capture Background ----------------
    elif key == ord("b"):

        print("Stand away from camera...")
        time.sleep(2)

        ret, bg = cap.read()

        if ret:
            background = cv2.flip(bg, 1)
            print("Background Updated Successfully!")

    # ---------------- Quit ----------------
    elif key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
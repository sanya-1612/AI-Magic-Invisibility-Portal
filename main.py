import cv2
import mediapipe as mp

from portal import Portal

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0)

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

# ---------------- Dynamic Background Estimation ----------------
print("Initializing dynamic background model...")
bg_subtractor = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=16, detectShadows=False)
background = None

# ---------------- Portal ----------------
portal = Portal(radius=120)

while True:

    ret, frame = cap.read()

    if not ret:
        break

    frame = cv2.flip(frame, 1)

    # ---------------- Update Background Model ----------------
    bg_subtractor.apply(frame, learningRate=0.005)
    bg_model_frame = bg_subtractor.getBackgroundImage()
    
    if bg_model_frame is not None:
        background = bg_model_frame
    else:
        background = frame.copy()

    # ---------------- Hand Tracking ----------------
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

    # ---------------- Draw Portal ----------------
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
        frame,
        "Move Index Finger | Thumb = Portal Size | Q = Quit",
        (20, 100),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (200, 200, 200),
        1,
        cv2.LINE_AA
    )

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

    cv2.imshow("AI Magic Invisibility Portal", frame)

    key = cv2.waitKey(1) & 0xFF

    # ---------------- Quit ----------------
    if key == ord("q"):
        break

cap.release()
cv2.destroyAllWindows()
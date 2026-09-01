import cv2
import mediapipe as mp
import time
import threading
import queue

from portal import Portal

# ---------------- Camera ----------------
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Cannot open camera")
    exit()

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

# ---------------- Multi-Threading Queues ----------------
frame_queue = queue.Queue(maxsize=2)
result_queue = queue.Queue(maxsize=2)
stop_event = threading.Event()

# ---------------- Thread 1: Camera Capture ----------------
def capture_frames():
    while not stop_event.is_set():
        ret, frame = cap.read()
        if not ret:
            stop_event.set()
            break
            
        frame = cv2.flip(frame, 1)
        
        # Keep queue fresh by removing oldest if full
        if frame_queue.full():
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass
        
        frame_queue.put(frame)

# ---------------- Thread 2: ML Inference ----------------
def process_frames():
    mp_hands = mp.solutions.hands
    hands = mp_hands.Hands(
        max_num_hands=1,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.7
    )
    
    while not stop_event.is_set():
        try:
            frame = frame_queue.get(timeout=0.1)
        except queue.Empty:
            continue
            
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = hands.process(rgb)
        
        if result_queue.full():
            try:
                result_queue.get_nowait()
            except queue.Empty:
                pass
                
        result_queue.put((frame, results))
        
    hands.close()

# Start Threads
capture_thread = threading.Thread(target=capture_frames, daemon=True)
inference_thread = threading.Thread(target=process_frames, daemon=True)

capture_thread.start()
inference_thread.start()

# ---------------- Main Thread: Rendering ----------------
mp_draw = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

while not stop_event.is_set():
    try:
        frame, results = result_queue.get(timeout=0.1)
    except queue.Empty:
        # Check for keyboard events even if no frame is ready
        key = cv2.waitKey(1) & 0xFF
        if key == ord("q"):
            stop_event.set()
        continue

    h, w = frame.shape[:2]

    if results.multi_hand_landmarks:
        hand = results.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        tip = hand.landmark[8]
        thumb = hand.landmark[4]

        x = int(tip.x * w)
        y = int(tip.y * h)
        portal.update(x, y)

        distance = ((tip.x - thumb.x) ** 2 + (tip.y - thumb.y) ** 2) ** 0.5
        radius = int(distance * 500)
        portal.set_radius(radius)

    frame = portal.draw(frame, background)

    cv2.putText(frame, "AI Magic Invisibility Portal", (20, 40), cv2.FONT_HERSHEY_DUPLEX, 0.9, (255, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Developed by Sanya Rathore", (20, 70), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 255), 2, cv2.LINE_AA)
    cv2.putText(frame, "Move Index Finger | Thumb = Portal Size | Press B = Capture Background", (20, 100), cv2.FONT_HERSHEY_SIMPLEX, 0.55, (200, 200, 200), 1, cv2.LINE_AA)
    cv2.putText(frame, "© Sanya Rathore", (frame.shape[1] - 190, frame.shape[0] - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (180, 180, 180), 2, cv2.LINE_AA)

    cv2.imshow("AI Magic Invisibility Portal", frame)

    key = cv2.waitKey(1) & 0xFF

    if key == ord("b"):
        print("Stand away from camera...")
        time.sleep(2)
        # Flush the frame queue to get the latest background
        while not frame_queue.empty():
            try:
                frame_queue.get_nowait()
            except queue.Empty:
                pass
                
        ret, bg = cap.read()
        if ret:
            background = cv2.flip(bg, 1)
            print("Background Updated Successfully!")

    if key == ord("q"):
        stop_event.set()

cap.release()
cv2.destroyAllWindows()
capture_thread.join()
inference_thread.join()
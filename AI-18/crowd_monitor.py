import cv2
import time
import threading
import winsound  # For beep
from ultralytics import YOLO
import alert_system 

# === SETTINGS ===
model = YOLO('yolov8n.pt')  
CROWD_LIMIT = 2
CAMERA_NAME = "Main Gate" 
ALERT_COOLDOWN_SECONDS = 10
last_alert_time = 0

# === FUNCTIONS ===
def play_beep():
    """
    Play beep sound on overcrowding detection.
    """
    duration = 500  # milliseconds
    freq = 1000  # Hz
    winsound.Beep(freq, duration)

# === CAMERA SETUP ===
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("❌ Error: Camera could not be opened.")
    exit()

print(f"✅ Camera started at {CAMERA_NAME}. Monitoring crowd...")

# === MONITOR LOOP ===
while True:
    ret, frame = cap.read()
    if not ret:
        print("❌ Failed to grab frame!")
        break

    results = model.predict(frame, conf=0.6, verbose=False)
    person_count = 0

    for r in results:
        for box in r.boxes:
            cls_id = int(box.cls[0])
            if cls_id == 0:  # 'person' class
                person_count += 1
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

    # Show People Count
    cv2.putText(frame, f"People Count: {person_count}", (20, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

    current_time = time.time()

    if person_count >= CROWD_LIMIT:
        if current_time - last_alert_time > ALERT_COOLDOWN_SECONDS:
            print(f"🚨 Overcrowding at {CAMERA_NAME}! People: {person_count}")

            # Trigger evacuation alert
            alert_system.trigger_alert(CAMERA_NAME, person_count)

            # Play beep sound
            threading.Thread(target=play_beep).start()

            last_alert_time = current_time
    else:
        last_alert_time = 0

    # Display the frame
    cv2.imshow(f"Crowd Monitoring - {CAMERA_NAME}", frame)

    # Press 'q' to quit
    if cv2.waitKey(1) & 0xFF == ord('q'):
        print("\n👋 Exiting monitoring...")
        break

# === CLEANUP ===
cap.release()
cv2.destroyAllWindows()

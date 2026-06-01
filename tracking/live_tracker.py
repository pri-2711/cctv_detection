from ultralytics import YOLO
import win32gui
import win32ui
import ctypes
import cv2
import numpy as np
import os
import time
from datetime import datetime

# -----------------------------
# Configuration
# -----------------------------
WINDOW_NAME = "BlueStacks App Player"

OUTPUT_FOLDER = "data/tracking_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

COOLDOWN_SECONDS = 10

# Green
BOX_COLOR = (0, 255, 0)

# Detection confidence threshold
CONFIDENCE_THRESHOLD = 0.50

# -----------------------------
# Load YOLO
# -----------------------------
model = YOLO("yolov8n.pt")

# -----------------------------
# Find Bluestacks
# -----------------------------
hwnd = win32gui.FindWindow(None, WINDOW_NAME)

if not hwnd:
    print("Bluestacks not found")
    exit()

left, top, right, bottom = win32gui.GetWindowRect(hwnd)

width = right - left
height = bottom - top

print("Tracking started...")
print("Press CTRL+C to stop.")

last_saved_time = 0

try:

    while True:

        # -----------------------------
        # Background Capture
        # -----------------------------
        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        bitmap = win32ui.CreateBitmap()
        bitmap.CreateCompatibleBitmap(
            mfcDC,
            width,
            height
        )

        saveDC.SelectObject(bitmap)

        result = ctypes.windll.user32.PrintWindow(
            hwnd,
            saveDC.GetSafeHdc(),
            3
        )

        if result != 1:
            continue

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        frame = np.frombuffer(
            bmpstr,
            dtype=np.uint8
        )

        frame = frame.reshape(
            (
                bmpinfo["bmHeight"],
                bmpinfo["bmWidth"],
                4
            )
        )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGRA2BGR
        )

        # -----------------------------
        # YOLO + ByteTrack
        # -----------------------------
        results = model.track(
            frame,
            persist=True,
            conf=CONFIDENCE_THRESHOLD,
            verbose=False,
            tracker="bytetrack.yaml"
        )

        tracked_persons = 0

        for result in results:

            if result.boxes is None:
                continue

            for box in result.boxes:

                class_id = int(box.cls[0])
                class_name = model.names[class_id]

                # Only track persons
                if class_name != "person":
                    continue

                confidence = float(box.conf[0])

                # Ignore weak detections
                if confidence < CONFIDENCE_THRESHOLD:
                    continue

                tracked_persons += 1

                x1, y1, x2, y2 = map(
                    int,
                    box.xyxy[0]
                )

                # Track ID
                if box.id is not None:
                    track_id = int(box.id[0])
                else:
                    track_id = -1

                # Draw box
                cv2.rectangle(
                    frame,
                    (x1, y1),
                    (x2, y2),
                    BOX_COLOR,
                    2
                )

                label = (
                    f"ID {track_id} | "
                    f"{confidence:.2f}"
                )

                cv2.putText(
                    frame,
                    label,
                    (x1, y1 - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    BOX_COLOR,
                    2
                )

        # -----------------------------
        # Save Tracking Snapshot
        # -----------------------------
        current_time = time.time()

        if (
            tracked_persons > 0 and
            current_time - last_saved_time >= COOLDOWN_SECONDS
        ):

            timestamp = datetime.now().strftime(
                "%Y-%m-%d_%H-%M-%S"
            )

            filename = (
                f"{timestamp}_tracked_person.png"
            )

            output_path = os.path.join(
                OUTPUT_FOLDER,
                filename
            )

            cv2.imwrite(
                output_path,
                frame
            )

            last_saved_time = current_time

            print(
                f"[{timestamp}] "
                f"Tracked Persons: {tracked_persons}"
            )

            print(
                f"Saved: {output_path}"
            )

        # -----------------------------
        # Cleanup
        # -----------------------------
        win32gui.DeleteObject(
            bitmap.GetHandle()
        )

        saveDC.DeleteDC()
        mfcDC.DeleteDC()

        win32gui.ReleaseDC(
            hwnd,
            hwndDC
        )

except KeyboardInterrupt:

    print("\nTracking stopped.")
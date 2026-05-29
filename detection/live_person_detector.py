from ultralytics import YOLO
import win32gui
import win32ui
import ctypes
import cv2
import numpy as np
import os
from datetime import datetime

WINDOW_NAME = "BlueStacks App Player"

OUTPUT_FOLDER = "data/detection_persons_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

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

print("Monitoring started...")

while True:

    # -----------------------------
    # Background Capture
    # -----------------------------
    hwndDC = win32gui.GetWindowDC(hwnd)
    mfcDC = win32ui.CreateDCFromHandle(hwndDC)
    saveDC = mfcDC.CreateCompatibleDC()

    bitmap = win32ui.CreateBitmap()
    bitmap.CreateCompatibleBitmap(mfcDC, width, height)

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
    # YOLO Detection
    # -----------------------------
    results = model(frame, verbose=False)

    person_count = 0

    for detection_result in results:

        boxes = detection_result.boxes

        for box in boxes:

            class_id = int(box.cls[0])
            confidence = float(box.conf[0])

            class_name = model.names[class_id]

            if class_name != "person":
                continue

            person_count += 1

            x1, y1, x2, y2 = map(
                int,
                box.xyxy[0]
            )

            cv2.rectangle(
                frame,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"Person {confidence:.2f}"

            cv2.putText(
                frame,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.6,
                (0, 255, 0),
                2
            )

    # -----------------------------
    # Detection Event
    # -----------------------------
    if person_count > 0:

        timestamp = datetime.now().strftime(
            "%Y-%m-%d_%H-%M-%S"
        )

        filename = (
            f"{timestamp}_detected_person_image.png"
        )

        output_path = os.path.join(
            OUTPUT_FOLDER,
            filename
        )

        cv2.imwrite(
            output_path,
            frame
        )

        print(
            f"Persons Found: {person_count}"
        )

    # -----------------------------
    # Cleanup
    # -----------------------------
    win32gui.DeleteObject(bitmap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)
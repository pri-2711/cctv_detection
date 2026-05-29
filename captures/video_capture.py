import win32gui
import win32ui
import ctypes
import cv2
import numpy as np
import os
import time
from datetime import datetime

WINDOW_NAME = "BlueStacks App Player"

FPS = 10
DURATION = 30  # seconds

# -----------------------------
# Find Bluestacks window
# -----------------------------
hwnd = win32gui.FindWindow(None, WINDOW_NAME)

if not hwnd:
    print("Window not found")
    exit()

left, top, right, bottom = win32gui.GetWindowRect(hwnd)

width = right - left
height = bottom - top

# -----------------------------
# Video folder
# -----------------------------
script_dir = os.path.dirname(os.path.abspath(__file__))
save_folder = os.path.join(script_dir, "..", "data", "saved_videos")
os.makedirs(save_folder, exist_ok=True)

timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

video_path = os.path.join(
    save_folder,
    f"video_{timestamp}.mp4"
)

# -----------------------------
# Video writer
# -----------------------------
fourcc = cv2.VideoWriter_fourcc(*"mp4v")

video_writer = cv2.VideoWriter(
    video_path,
    fourcc,
    FPS,
    (width, height)
)

# -----------------------------
# Capture loop
# -----------------------------
total_frames = FPS * DURATION

print(f"Recording {DURATION}s...")
print(f"Frames: {total_frames}")

for frame_no in range(total_frames):

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

    if result == 1:

        bmpinfo = bitmap.GetInfo()
        bmpstr = bitmap.GetBitmapBits(True)

        frame = np.frombuffer(
            bmpstr,
            dtype=np.uint8
        )

        frame = frame.reshape(
            (bmpinfo["bmHeight"],
             bmpinfo["bmWidth"],
             4)
        )

        frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGRA2BGR
        )

        video_writer.write(frame)

    win32gui.DeleteObject(bitmap.GetHandle())
    saveDC.DeleteDC()
    mfcDC.DeleteDC()
    win32gui.ReleaseDC(hwnd, hwndDC)

    time.sleep(1 / FPS)

video_writer.release()

print(f"Saved: {video_path}")
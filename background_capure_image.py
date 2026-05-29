import win32gui
import win32ui
import ctypes
from PIL import Image
from datetime import datetime
import os

window_name = "BlueStacks App Player"

hwnd = win32gui.FindWindow(None, window_name)

if not hwnd:
    print("Window not found")
    exit()

left, top, right, bottom = win32gui.GetWindowRect(hwnd)
width = right - left
height = bottom - top

hwndDC = win32gui.GetWindowDC(hwnd)
mfcDC = win32ui.CreateDCFromHandle(hwndDC)
saveDC = mfcDC.CreateCompatibleDC()

bitmap = win32ui.CreateBitmap()
bitmap.CreateCompatibleBitmap(mfcDC, width, height)
saveDC.SelectObject(bitmap)

# Capture window
result = ctypes.windll.user32.PrintWindow(
    hwnd,
    saveDC.GetSafeHdc(),
    3
)

bmpinfo = bitmap.GetInfo()
bmpstr = bitmap.GetBitmapBits(True)

img = Image.frombuffer(
    'RGB',
    (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
    bmpstr,
    'raw',
    'BGRX',
    0,
    1
)

# Create folder if not exists
save_folder = "saved_captures"
os.makedirs(save_folder, exist_ok=True)

# Generate timestamp filename
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")

filename = f"capture_{timestamp}.png"
filepath = os.path.join(save_folder, filename)

# Save image
img.save(filepath)

print(f"Saved: {filepath}")
print("Result =", result)

# Cleanup
win32gui.DeleteObject(bitmap.GetHandle())
saveDC.DeleteDC()
mfcDC.DeleteDC()
win32gui.ReleaseDC(hwnd, hwndDC)
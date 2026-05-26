# AI CCTV Detection Extension (Local Surveillance Prototype)

## Project Idea
Build a **local AI surveillance layer** over a CCTV stream running via Bluestacks + ezyKam+.

Pipeline (planned):

CCTV → Bluestacks → Background capture → AI detection → Unknown person detection → Save suspicious clips locally

---

## Possible Features
- Detect humans in CCTV feed
- Known vs unknown face identification
- Ignore known family members
- Detect masks / covered faces (optional)
- Intrusion / restricted-area alerts
- Save only suspicious clips locally
- Timestamp logs
- Notifications (future)

---

## Technologies (possible)
- Python
- OpenCV
- MSS / pywin32
- Bluestacks (Android emulator)
- YOLO (person detection)
- Face recognition models
- NumPy
- pygetwindow
- Pillow
- Windows APIs (`PrintWindow`)
- Local storage (SQLite/filesystem)

---

## Current Progress
### Working:
- Installed Bluestacks
- Installed ezyKam+ in Bluestacks
- Logged into CCTV account
- Accessed live CCTV feed
- Tested screen capture methods
- Implemented **background window capture**
- Successfully captured Bluestacks while not actively focused

### Result:
Proof that:

Bluestacks → Python → Background capture

works.

This means AI inference on CCTV frames is feasible.

---

## Next Steps
1. Continuous frame extraction
2. Human detection
3. Face recognition
4. Unknown-person filtering
5. Clip storage
6. Alerts
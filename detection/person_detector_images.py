from ultralytics import YOLO
import cv2
import os

# Load YOLOv8 Nano
model = YOLO("yolov8n.pt")

INPUT_FOLDER = "data/saved_images"

OUTPUT_FOLDER = "data/detection_persons_images"
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

# Supported image formats
VALID_EXTENSIONS = (".png", ".jpg", ".jpeg")

for filename in os.listdir(INPUT_FOLDER):

    if not filename.lower().endswith(VALID_EXTENSIONS):
        continue

    image_path = os.path.join(INPUT_FOLDER, filename)

    image = cv2.imread(image_path)

    if image is None:
        print(f"Could not read {image_path}")
        continue

    results = model(image)

    person_count = 0

    for result in results:

        boxes = result.boxes

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
                image,
                (x1, y1),
                (x2, y2),
                (0, 255, 0),
                2
            )

            label = f"Person {confidence:.2f}"

            cv2.putText(
                image,
                label,
                (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2
            )

    # Create output filename
    name, ext = os.path.splitext(filename)

    output_filename = f"{name}_detected_person_image{ext}"

    output_path = os.path.join(
        OUTPUT_FOLDER,
        output_filename
    )

    cv2.imwrite(output_path, image)

    print(f"\nImage: {filename}")
    print(f"Persons Found: {person_count}")
    print(f"Saved: {output_path}")
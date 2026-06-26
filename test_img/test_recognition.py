import cv2
from face_recognition.face_identifier import identify_person

image = cv2.imread(
    "test_img/test_img_1.jpeg"
)

result = identify_person(image)

person, score = result
print("---------------------------------")
print(f"Prediction : {person}")
print(f"Similarity : {score:.3f}")
print("---------------------------------")
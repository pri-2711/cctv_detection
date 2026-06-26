import os
import cv2

from embedding_generator import (
    get_face_embedding
)

from face_database import (
    save_embedding
)

KNOWN_FACE_FOLDER = (
    "data/known_faces"
)


def register_person(
        person_name
):

    person_folder = os.path.join(
        KNOWN_FACE_FOLDER,
        person_name
    )

    if not os.path.exists(
            person_folder
    ):
        print(
            "Person folder not found."
        )
        return

    embeddings = []

    for file in os.listdir(
            person_folder
    ):

        if not file.lower().endswith(
                (
                    ".jpg",
                    ".jpeg",
                    ".png"
                )
        ):
            continue

        path = os.path.join(
            person_folder,
            file
        )

        image = cv2.imread(path)

        if image is None:
            continue

        embedding = (
            get_face_embedding(
                image
            )
        )

        if embedding is None:

            print(
                f"No face found in {file}"
            )
            continue

        embeddings.append(
            embedding
        )

        print(
            f"Processed {file}"
        )

    if len(embeddings) == 0:

        print(
            "No valid faces found."
        )

        return

    save_embedding(
        person_name,
        embeddings
    )

    print(
        f"{person_name} registered."
    )


if __name__ == "__main__":

    person_name = input(
        "Enter person name: "
    )

    register_person(
        person_name
    )
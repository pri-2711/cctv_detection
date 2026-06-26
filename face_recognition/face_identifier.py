import cv2
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

from embedding_generator import (
    get_face_embedding
)

from face_database import (
    load_all_embeddings
)

SIMILARITY_THRESHOLD = 0.50


def identify_person(image):

    unknown_embedding = (
        get_face_embedding(image)
    )

    if unknown_embedding is None:
        return "No Face"

    database = (
        load_all_embeddings()
    )

    best_match = None
    best_score = 0

    for person_name, embeddings in (
            database.items()
    ):

        for emb in embeddings:

            score = cosine_similarity(
                [unknown_embedding],
                [emb]
            )[0][0]

            if score > best_score:

                best_score = score
                best_match = person_name

    if (
            best_score >
            SIMILARITY_THRESHOLD
    ):
        return (
            best_match,
            best_score
        )

    return (
        "Unknown",
        best_score
    )
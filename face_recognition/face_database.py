import os
import joblib

EMBEDDING_FOLDER = "data/embeddings"

os.makedirs(
    EMBEDDING_FOLDER,
    exist_ok=True
)


def save_embedding(
        person_name,
        embeddings
):

    path = os.path.join(
        EMBEDDING_FOLDER,
        f"{person_name}.pkl"
    )

    joblib.dump(
        embeddings,
        path
    )


def load_all_embeddings():

    database = {}

    for file in os.listdir(
        EMBEDDING_FOLDER
    ):

        if not file.endswith(".pkl"):
            continue

        person_name = file.replace(
            ".pkl",
            ""
        )

        path = os.path.join(
            EMBEDDING_FOLDER,
            file
        )

        database[
            person_name
        ] = joblib.load(path)

    return database
from insightface.app import FaceAnalysis

app = FaceAnalysis(
    providers=['CPUExecutionProvider']
)

app.prepare(
    ctx_id=0,
    det_size=(640, 640)
)


def get_face_embedding(image):

    faces = app.get(image)

    if len(faces) == 0:
        return None

    # Largest face
    face = max(
        faces,
        key=lambda f:
        (f.bbox[2] - f.bbox[0]) *
        (f.bbox[3] - f.bbox[1])
    )

    return face.embedding
from fastembed import TextEmbedding


EMBEDDING_MODEL = "BAAI/bge-small-en-v1.5"

_embedding_model = None


def get_embedding_model():
    global _embedding_model

    if _embedding_model is None:
        _embedding_model = TextEmbedding(
            model_name=EMBEDDING_MODEL
        )

    return _embedding_model


def generate_embedding(text):
    model = get_embedding_model()

    embedding = next(
        model.embed([text])
    )

    return embedding.tolist()
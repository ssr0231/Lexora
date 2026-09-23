from sentence_transformers import SentenceTransformer


MODEL_NAME = "all-MiniLM-L6-v2"

model = SentenceTransformer(MODEL_NAME)


def generate_embedding(text: str) -> list[float]:
    embedding = model.encode(
        text,
        normalize_embeddings=True,
    )

    return embedding.tolist()


def save_chunk_embedding(
    supabase,
    chunk_id: str,
    text: str,
) -> list[float]:
    embedding = generate_embedding(text)

    supabase.table("document_chunks").update(
        {
            "embedding": embedding,
        }
    ).eq(
        "id",
        chunk_id,
    ).execute()

    return embedding
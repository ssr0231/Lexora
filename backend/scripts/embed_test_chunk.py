from getpass import getpass

from supabase import create_client

from backend.app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY
from backend.app.services.embedding_service import save_chunk_embedding


CHUNK_ID = "7656e725-2cea-4720-b56d-f7efa2819510"

EMAIL = "singh.shubham0231@gmail.com"


def main():
    password = getpass("Enter your Supabase password: ")

    supabase = create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY,
    )

    response = supabase.auth.sign_in_with_password(
        {
            "email": EMAIL,
            "password": password,
        }
    )

    access_token = response.session.access_token

    authenticated_supabase = create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY,
    )

    authenticated_supabase.postgrest.auth(access_token)

    result = (
        authenticated_supabase.table("document_chunks")
        .select("id, content")
        .eq("id", CHUNK_ID)
        .single()
        .execute()
    )

    chunk = result.data

    embedding = save_chunk_embedding(
        supabase=authenticated_supabase,
        chunk_id=chunk["id"],
        text=chunk["content"],
    )

    print("Embedding saved successfully.")
    print("Chunk ID:", chunk["id"])
    print("Embedding dimensions:", len(embedding))


if __name__ == "__main__":
    main()
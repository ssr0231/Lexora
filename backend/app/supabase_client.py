from supabase import create_client, Client

from backend.app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY,
)

from supabase import create_client, Client

from backend.app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY,
)


def get_supabase_client(access_token: str) -> Client:
    client = create_client(
        SUPABASE_URL,
        SUPABASE_PUBLISHABLE_KEY,
    )

    client.postgrest.auth(access_token)

    return client
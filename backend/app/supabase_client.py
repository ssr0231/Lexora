from supabase import create_client, Client

from backend.app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY


supabase: Client = create_client(
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY,
)
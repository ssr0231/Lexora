from getpass import getpass

from supabase import create_client

from backend.app.config import SUPABASE_URL, SUPABASE_PUBLISHABLE_KEY


email = "singh.shubham0231@gmail.com"
password = getpass("Enter your Supabase password: ")

supabase = create_client(
    SUPABASE_URL,
    SUPABASE_PUBLISHABLE_KEY,
)

response = supabase.auth.sign_in_with_password(
    {
        "email": email,
        "password": password,
    }
)

print("\nLogin successful.")
print("\nAccess token:\n")
print(response.session.access_token)
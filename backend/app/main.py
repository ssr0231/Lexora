from fastapi import Depends, FastAPI

from backend.app.auth import get_current_user
from backend.app.schemas.client import ClientCreate
from backend.app.supabase_client import get_supabase_client


app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/me")
def get_me(auth=Depends(get_current_user)):
    user = auth["user"]

    return {
        "id": str(user.id),
        "email": user.email,
    }


@app.get("/me/profile")
def get_my_profile(auth=Depends(get_current_user)):
    user = auth["user"]
    access_token = auth["access_token"]

    client = get_supabase_client(access_token)

    response = (
        client.table("users")
        .select("id, full_name, role")
        .eq("id", str(user.id))
        .single()
        .execute()
    )

    return response.data


@app.post("/clients")
def create_client(
    client: ClientCreate,
    auth=Depends(get_current_user),
):
    access_token = auth["access_token"]

    supabase = get_supabase_client(access_token)

    response = (
        supabase.table("clients")
        .insert(client.model_dump())
        .execute()
    )

    return response.data[0]
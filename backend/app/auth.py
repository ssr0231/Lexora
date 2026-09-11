from fastapi import Header, HTTPException

from backend.app.supabase_client import supabase


def get_current_user(authorization: str | None = Header(default=None)):
    if not authorization:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    if not authorization.startswith("Bearer "):
        raise HTTPException(
            status_code=401,
            detail="Invalid Authorization header",
        )

    access_token = authorization.removeprefix("Bearer ").strip()

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Missing access token",
        )

    try:
        response = supabase.auth.get_user(access_token)
    except Exception:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        )

    return {
    "user": response.user,
    "access_token": access_token,
    }

from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer

from backend.app.supabase_client import supabase


security = HTTPBearer(auto_error=False)


def get_current_user(
    credentials: HTTPAuthorizationCredentials | None = Depends(security),
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Missing Authorization header",
        )

    access_token = credentials.credentials

    if not access_token:
        raise HTTPException(
            status_code=401,
            detail="Missing access token",
        )

    try:
        response = supabase.auth.get_user(access_token)
    except Exception as error:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired access token",
        ) from error

    return {
        "user": response.user,
        "access_token": access_token,
    }
from fastapi import Depends, FastAPI

from backend.app.auth import get_current_user

app = FastAPI()


@app.get("/health")
def health_check():
    return {"status": "ok"}


@app.get("/me")
def get_me(user=Depends(get_current_user)):
    return {
        "id": str(user.id),
        "email": user.email,
    }
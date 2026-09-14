from pydantic import BaseModel


class ClientAssignmentCreate(BaseModel):
    user_id: str
    client_id: str
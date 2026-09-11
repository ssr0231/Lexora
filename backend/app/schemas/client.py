from pydantic import BaseModel


class ClientCreate(BaseModel):
    name: str
    gstin: str | None = None
    industry: str | None = None
    description: str | None = None
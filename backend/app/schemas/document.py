from enum import Enum
from uuid import UUID

from pydantic import BaseModel


class DocumentType(str, Enum):
    GST_ACT = "gst_act"
    GST_RULE = "gst_rule"
    NOTIFICATION = "notification"
    CIRCULAR = "circular"
    CLIENT_DOCUMENT = "client_document"


class DocumentCreate(BaseModel):
    title: str
    document_type: DocumentType
    client_id: UUID | None = None
    storage_path: str | None = None
    processing_status: str = "pending"
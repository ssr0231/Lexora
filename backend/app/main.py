
import httpx

from fastapi import Depends, FastAPI, File, Form, HTTPException, UploadFile
from pathlib import Path
from uuid import uuid4

from backend.app.auth import get_current_user
from backend.app.config import (
    DOCUMENTS_BUCKET,
    SUPABASE_PUBLISHABLE_KEY,
    SUPABASE_URL,
)
from backend.app.schemas.assignment import ClientAssignmentCreate
from backend.app.schemas.client import ClientCreate
from backend.app.schemas.document import DocumentCreate, DocumentType
from backend.app.supabase_client import get_supabase_client
from backend.app.services.pdf_extractor import extract_text_from_pdf
from backend.app.services.text_chunker import chunk_text
from backend.app.services.embedding_service import generate_embedding

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

    try:
        response = (
            supabase.table("clients")
            .insert(client.model_dump())
            .execute()
        )
    except Exception as error:
        raise HTTPException(
            status_code=403,
            detail="You are not allowed to create clients",
        ) from error

    return response.data[0]


@app.get("/clients")
def list_clients(auth=Depends(get_current_user)):
    access_token = auth["access_token"]
    supabase = get_supabase_client(access_token)

    response = (
        supabase.table("clients")
        .select(
            "id, name, gstin, industry, description, created_at"
        )
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


@app.post("/client-assignments")
def assign_client(
    assignment: ClientAssignmentCreate,
    auth=Depends(get_current_user),
):
    access_token = auth["access_token"]
    supabase = get_supabase_client(access_token)

    response = (
        supabase.table("user_clients")
        .insert(assignment.model_dump())
        .execute()
    )

    return response.data[0]


@app.post("/documents")
def create_document(
    document: DocumentCreate,
    auth=Depends(get_current_user),
):
    access_token = auth["access_token"]
    supabase = get_supabase_client(access_token)

    response = (
        supabase.table("documents")
        .insert(document.model_dump(mode="json"))
        .execute()
    )

    return response.data[0]


@app.get("/documents")
def list_documents(auth=Depends(get_current_user)):
    access_token = auth["access_token"]
    supabase = get_supabase_client(access_token)

    response = (
        supabase.table("documents")
        .select(
            "id, title, document_type, client_id, "
            "source_url, storage_path, processing_status, created_at"
        )
        .order("created_at", desc=True)
        .execute()
    )

    return response.data


@app.post("/documents/upload")
def upload_document(
    file: UploadFile = File(...),
    title: str = Form(...),
    document_type: DocumentType = Form(...),
    client_id: str | None = Form(default=None),
    auth=Depends(get_current_user),
):
    # Validate the uploaded file's content type.
    if file.content_type != "application/pdf":
        raise HTTPException(
            status_code=400,
            detail="Only PDF files are supported",
        )

    # Validate that a filename exists.
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="A filename is required",
        )

    # Validate the file extension.
    file_extension = Path(file.filename).suffix.lower()

    if file_extension != ".pdf":
        raise HTTPException(
            status_code=400,
            detail="The uploaded file must have a .pdf extension",
        )

    # Read the uploaded file into memory.
    file_bytes = file.file.read()

    # Enforce the 20 MB file-size limit.
    if len(file_bytes) > 20 * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail="File size must not exceed 20 MB",
        )

    # Extract text and split it into chunks.
    try:
        extracted_text = extract_text_from_pdf(file_bytes)
        text_chunks = chunk_text(extracted_text)

        print(f"EXTRACTED TEXT LENGTH: {len(extracted_text)}")
        print(f"NUMBER OF TEXT CHUNKS: {len(text_chunks)}")
        print(
            "FIRST CHUNK PREVIEW: "
            f"{text_chunks[0][:500] if text_chunks else 'No text found'}"
        )

        if not text_chunks:
            raise HTTPException(
                status_code=400,
                detail="No readable text was found in the PDF",
            )

    except HTTPException:
        raise

    except Exception as error:
        print(f"PDF TEXT EXTRACTION ERROR: {error!r}")

        raise HTTPException(
            status_code=400,
            detail="Unable to extract text from the PDF",
        ) from error

    access_token = auth["access_token"]

    # Generate a unique Storage path.
    storage_path = f"regulatory/{uuid4()}.pdf"

    try:
        # Upload the PDF to Supabase Storage.
        storage_url = (
            f"{SUPABASE_URL}/storage/v1/object/"
            f"{DOCUMENTS_BUCKET}/{storage_path}"
        )

        response = httpx.post(
            storage_url,
            content=file_bytes,
            headers={
                "apikey": SUPABASE_PUBLISHABLE_KEY,
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/pdf",
                "x-upsert": "false",
            },
            timeout=30.0,
        )

        print(f"STORAGE STATUS: {response.status_code}")
        print(f"STORAGE RESPONSE: {response.text}")

        response.raise_for_status()

        # Create the document metadata record.
        supabase = get_supabase_client(access_token)

        document_response = (
            supabase.table("documents")
            .insert(
                {
                    "title": title,
                    "document_type": document_type.value,
                    "client_id": client_id,
                    "storage_path": storage_path,
                    "processing_status": "pending",
                }
            )
            .execute()
        )

        document_record = document_response.data[0]

        # Prepare chunk records for the document_chunks table.
        chunk_records = [
            {
                "document_id": document_record["id"],
                "content": chunk,
                "embedding": generate_embedding(chunk),
                "page_number": None,
                "chunk_index": index,
            }
            for index, chunk in enumerate(text_chunks)
        ]

        # Save the extracted chunks to the database.
        supabase.table("document_chunks").insert(
            chunk_records
        ).execute()

        print(f"SAVED CHUNKS: {len(chunk_records)}")

    except Exception as error:
        print(f"STORAGE OR DATABASE ERROR: {error!r}")

        raise HTTPException(
            status_code=500,
            detail="PDF upload or document processing failed",
        ) from error

    return {
        "message": (
            "PDF uploaded, document record created, "
            "and text chunks saved successfully"
        ),
        "document": document_record,
        "chunks_saved": len(chunk_records),
    }
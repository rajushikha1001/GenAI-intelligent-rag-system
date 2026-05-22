from fastapi import APIRouter, UploadFile, File
from app.services.document_service import process_document

router = APIRouter()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    content = await file.read()

    result = process_document(
        filename=file.filename,
        content=content
    )

    return {
        "message": "Document processed",
        "result": result
    }
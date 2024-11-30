import io

from fastapi import APIRouter
from pydantic import BaseModel

from common.db.utils import *
from common.db.schemes import Document

from fastapi.responses import StreamingResponse

from typing import Literal


router = APIRouter()


@router.get("/documents")
def documents() -> List[Document]:
    return get_all_documents_without_bytes()


@router.get("/document")
def document(document_id: str) -> Document:
    return get_document_by_id(document_id, add_file=False)


@router.delete("/document")
def delete(document_id: str) -> str:
    return delete_document(document_id)


@router.get("/download")
def download(document_id: str, download_type: Literal["docx", "pdf"] = "docx") -> StreamingResponse:
    document = get_document_by_id(document_id, add_file=True)

    file_like_document = io.BytesIO(document["file"])
    file_like_document.seek(0)
    
    return StreamingResponse(
            file_like_document, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
            headers={"Content-Disposition": f"attachment; filename=document.{download_type}"}
        )
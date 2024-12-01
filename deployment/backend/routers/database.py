import io
import traceback
import requests
import common.db.utils as db_utils

from urllib.parse import quote

from fastapi import APIRouter, UploadFile, File
from pydantic import BaseModel

from common.db.schemes import Document, DocumentInfo, DocumentType, Entity
from common.parser.utils import parse_document

from fastapi.responses import StreamingResponse

from typing import Literal, List


router = APIRouter()


@router.get("/documents")
def documents() -> List[Document]:
    return db_utils.get_all_documents_without_bytes()


@router.get("/document")
def get_document(document_id: str) -> Document:
    return db_utils.get_document_by_id(document_id, add_file=False)


@router.delete("/document")
def delete(document_id: str) -> str:
    return db_utils.delete_document(document_id)


@router.get("/download")
def download(document_id: str) -> StreamingResponse:
    document = db_utils.get_document_by_id(document_id, add_file=True)

    file_like_document = io.BytesIO(document["file"])
    file_like_document.seek(0)

    filename = quote(document['name'], encoding='utf-8')
    
    return StreamingResponse(
            file_like_document, 
            media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", 
            headers={"Content-Disposition": f"attachment; filename={filename}.docx"}
        )
import io
import json
import requests

from fastapi import HTTPException, APIRouter
from typing import List, Dict, Any

from pydantic import BaseModel
from docx import Document

from pymongo import MongoClient

from dependencies.models import SamplingParams
from dependencies.utils import get_response_from_llamacpp_server
from dependencies.constants import LLAMACPP_SERVER_ENDPOINT

from datetime import datetime


client = MongoClient("mongodb://mongodb:27017/")

database = client["database"]
collection = database["documents"]


class InputModel(BaseModel):
    fields: Dict[str, str]
    params: SamplingParams


def text_to_docx_bytes(text: str) -> bytes:
    """
    Return .docx file in bytes.

    Parameters
    ----------
    text : str
        Content of document.

    Returns
    -------
    bytes
        Bytes of document.
    """

    doc = Document()
    
    doc.add_paragraph(text)
    
    byte_stream = io.BytesIO()
    
    doc.save(byte_stream)
    
    byte_stream.seek(0)
    return byte_stream.getvalue()


router = APIRouter()


@router.post("/generate-document")
def generate(input: InputModel):
    document_as_bytes = text_to_docx_bytes(json.dumps(input.fields))

    try:
        collection.insert_one(document={
            "bytes": document_as_bytes, "timestamp": datetime.now()
        })
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to save document to the MongoDB: {e}")
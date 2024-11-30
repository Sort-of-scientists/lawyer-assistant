import io
import os
import json
import docx

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from pymongo import MongoClient
from typing import Dict
from pydantic import BaseModel

from common.llm.models import SamplingParams
from common.llm.utils import change_current_lora_adapter, get_completion

from common.db.utils import upload_document
from common.db.models import *

from common.classification.utils import get_classification_result


class InputModel(BaseModel):
    type: str
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

    doc = docx.Document()
    
    doc.add_paragraph(text)
    
    byte_stream = io.BytesIO()
    
    doc.save(byte_stream)
    
    byte_stream.seek(0)
    return byte_stream.getvalue()


router = APIRouter()


@router.put("/generate")
async def generate(input: InputModel):
    # change current lora adapter if need:
    change_current_lora_adapter(adapter_id=os.environ.get("GENERATE_LORA_ADAPTER_ID"))
    # generate document based on fields:
    document_as_text = get_completion(prompt=json.dumps(input.fields), params=input.params.model_dump())
    
    # transform document in text format to byte
    document_as_byte = text_to_docx_bytes(document_as_text)
    
    # upload document to mongodb
    upload_document(
        Document(
            file=document_as_byte, 
            info=DocumentInfo(
                header=input.type, desciption="hello ann mockLyakova"
            ),
            type=DocumentType(
                label=input.type, score=1.0
            ),
            entities=[Entity(label="", value="") for key, value in input.fields.items()]
        )
    )

    # return document from FastAPI
    file_like_document = io.BytesIO(document_as_byte)
    file_like_document.seek(0)

    return StreamingResponse(file_like_document, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "attachment; filename=document.docx"})


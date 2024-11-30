import os

from fastapi import APIRouter
from pydantic import BaseModel

from common.db.utils import *


router = APIRouter()


class Document(BaseModel):
    pass


@router.get("/documents-wo-bytes")
def documents():
    return get_all_documents_without_bytes()
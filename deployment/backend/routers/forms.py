from fastapi import APIRouter
from typing import List


DOCUMENTS_TYPES_TO_FORMS = {
    "Жалоба": [],
    "Акт": [],
    "Договор купли-продажи": []
}


router = APIRouter()


@router.get("/forms")
def forms(document_type: str) -> List[str]:
    return DOCUMENTS_TYPES_TO_FORMS[document_type]
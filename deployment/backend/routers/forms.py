from fastapi import APIRouter
from typing import List


DOCUMENTS_TYPES_TO_FORMS = {
    "Жалоба": ["Заказчик", "Предмет договора", "Исполнитель", "Дата"],
    "Акт": ["Заказчик", "Предмет договора", "Исполнитель", "Дата"],
    "Договор купли-продажи": ["Заказчик", "Предмет договора", "Исполнитель", "Дата"]
}

DOCUMENTS_TYPES = list(DOCUMENTS_TYPES_TO_FORMS.keys())


router = APIRouter()


@router.get("/forms")
def forms(document_type: str) -> List[str]:
    return DOCUMENTS_TYPES_TO_FORMS[document_type]


@router.get("/types")
def types() -> List[str]:
    return DOCUMENTS_TYPES

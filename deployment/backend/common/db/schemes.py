from pydantic import BaseModel
from typing import List


class Entity(BaseModel):
    """
    A model to represent an Entity.

    Attributes
    ----------
    value : str
        Value of Entity. For example, "Moscow" is a value of entity with label "LOC"

    label : str
        Label of Entity. "LOC", "PER", etc.

    score : float
        Confidence level

    start : int
        Begin of entity index

    end : int
        End of entity index
    """

    value: str
    label: str
    score: float | None = None
    start: int | None = None
    end: int | None = None


class DocumentInfo(BaseModel):
    """
    A model to represen document short information.

    Attributes
    ----------
    header : str
    description: str
    """
    header: str
    description: str


class DocumentType(BaseModel):
    """
    A model to represen document type.

    Attributes
    ----------
    label : str
    score : float
    """

    label: str
    score: float | None = None


class Document(BaseModel):
    """
    A model to represent a document.

    Attributes
    ----------
    id : str
    
    name : str
    file : bytes
    info : DocumentInfo

    type : DocumentType
    entities : List[Entity]
    """
    id: str | None = None

    file: bytes | None = None
    info: DocumentInfo | None = None

    type: DocumentType | None = None
    entities: List[Entity] | None = None

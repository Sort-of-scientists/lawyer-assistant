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
    score: float
    start: int
    end: int


class DocumentInfo(BaseModel):
    """
    A model to represen document short information.

    Attributes
    ----------
    header : str
    desciption: str
    """

    header: str
    desciption: str


class DocumentType(BaseModel):
    """
    A model to represen document type.

    Attributes
    ----------
    label : str
    score : float
    """

    label: str
    score: float


class Document(BaseModel):
    """
    A model to represent a document.

    Attributes
    ----------
    file : bytes
    info : DocumentInfo

    type : DocumentType
    entities : List[Entity]
    """
    file: bytes
    info: DocumentInfo

    type: DocumentType
    entities: List[Entity]

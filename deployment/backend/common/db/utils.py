import os
import requests

from pymongo import MongoClient
from bson import ObjectId
from fastapi import HTTPException

from pymongo.collection import Collection
from typing import List, Dict

from datetime import datetime

from .schemes import *


client = MongoClient(os.environ.get("MONGO_URI"))
database = client[os.environ.get("MONGO_DATABASE")]
collection = database[os.environ.get("MONGO_COLLECTION")]


def upload_document(document: Document):
    """
    Upload new document in bytes to collection.

    Parameters
    ----------
    collection : Collection

    document_as_bytes : bytes
    """

    try:
        collection.insert_one(document={
            "file": document.file,
            "info": document.info.model_dump(),
            "type": document.type.model_dump(),
            "entities": [ent.model_dump() for ent in document.entities],
            "timestamp": datetime.now()
        })

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to upload document: {e}")

def delete_document(document_id: str):
    """
    Delete document by its ID.

    Parameters
    ----------
    document_id : int
    Returns
    -------
    "OK!" if delete was success
    """

    try:
        collection.delete_one({"_id": ObjectId(document_id)})

        return "OK!"
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to delete document from database: {e}")


def get_all_documents_without_bytes() -> List[Document]:
    """
    Return all documents from collection.

    Parameters
    ----------
    collection : Collection

    Returns
    -------
    List[bytes]
    """

    documents = []

    for document in collection.find({}, {"file": 0}).sort({"timestamp": -1}):
        documents.append(
            Document(
                id=str(document["_id"]),
                info=DocumentInfo(
                    header=document["info"]["header"],
                    description=document["info"]["description"]
                ),
                type=DocumentType(
                    label=document["type"]["label"],
                    score=document["type"]["score"]
                ),

                entities=[Entity(**ent) for ent in document["entities"]]
            )
        )

    return documents


def get_document_by_id(document_id: str, add_file: bool = False) -> Document:
    """
    Get document by **document_id** without field **file**.

    Parameters
    ----------
    document_id : str

    Returns
    -------
    Document
    """

    try:
        if add_file:
            document = collection.find({"_id": ObjectId(document_id)})
        else:
            document = collection.find({"_id": ObjectId(document_id)}, {"file": 0})

        document = list(document)

        return document[0]
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to get document with id {document_id}: {e}")
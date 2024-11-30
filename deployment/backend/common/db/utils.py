import os

from pymongo import MongoClient

from pymongo.collection import Collection
from typing import List, Dict

from datetime import datetime

from models import Document


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

    collection.insert_one(document={
        "file": document.file,
        "info": document.info,
        "type": document.type,
        "entities": document.entities,
        "timestamp": datetime.now()
    })


def delete_document(document_id: int):
    pass


def get_all_documents_without_bytes() -> List[bytes]:
    """
    Return all documents from collection.

    Parameters
    ----------
    collection : Collection

    Returns
    -------
    List[bytes]
    """

    documents = collection.find({}, {"bytes": 0})

    documents = list(documents)

    print(documents)

    return documents
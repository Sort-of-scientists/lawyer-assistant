import os
import io
import json

import common.ml.utils as ml_utils
import common.db.utils as db_utils

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from common.ml.schemes import *

from common.parser.utils import parse_document, text_to_docx_bytes

from common.db.schemes import *


router = APIRouter()

# initialize the document classifier
docs_classifier = ml_utils.DocsClassifier(model_path="models/docs-classifier", tokenizer_path="models/docs-classifier")


@router.post("/generate")
async def generate(input: GenerateInputModel) -> StreamingResponse:
    """
    A route to generate a document using LLM API.

    Parameters
    ----------
    input : GenerateInputModel
        _description_

    Returns
    -------
    StreamingResponse
    """
    ml_utils.change_current_lora_adapter(adapter_id=int(os.environ.get("GENERATE_LORA_ADAPTER_ID")))
    
    # generate document based on fields:
    document_as_text = ml_utils.get_completion(prompt=json.dumps(input.fields, ensure_ascii=False), params=input.params.model_dump())
    
    # transform document in text format to byte
    document_as_byte = text_to_docx_bytes(document_as_text)
    
    # upload document to mongodb
    db_utils.upload_document(
        Document(
            file=document_as_byte, 
            info=DocumentInfo(
                header=input.type, description=", ".join(list(input.fields.values()))
            ),
            type=DocumentType(
                label=input.type, score=1.0
            ),
            entities=[Entity(label=key, value=value) for key, value in input.fields.items()]
        )
    )

    # return document from FastAPI
    file_like_document = io.BytesIO(document_as_byte)
    file_like_document.seek(0)

    return StreamingResponse(file_like_document, media_type="application/vnd.openxmlformats-officedocument.wordprocessingml.document", headers={"Content-Disposition": "attachment; filename=document.docx"})


@router.post("/summarize")
async def summarize(file: UploadFile = File(...), n_sentences_to_keep: int = 2, n_predict: int = 300, temperature: float = 0.8) -> str:
    """
    A route to make a summary of the input text.

    Parameters
    ----------
    file : UploadFile = File(...),
        Uploaded file to summarize.

    n_sentences_to_keep : int, optional
        Number of sentences to keep in result summary,
    
    n_predict : int
        Number of tokens to generate in summary,

    temperature : float
        Temperature of generation.
    """
    ml_utils.change_current_lora_adapter(adapter_id=int(os.environ.get("SUMMARY_LORA_ADAPTER_ID")))

    # parse document
    document = await file.read()
    document = parse_document(document)

    # preprocess input text
    text = ml_utils.get_preprocessed_text(text=document)
    # make request to llama.cpp server
    summary = ml_utils.get_completion(prompt=text, params={"n_predict": n_predict, "temperature": temperature})
    # reduce summary
    summary = ml_utils.get_reduced_summary(summary=summary, n_sentences_to_keep=n_sentences_to_keep)

    return summary


@router.post("/classify")
async def classify(file: UploadFile = File(...), threshold: float = 0.4) -> ClassifyOutputModel:
    """
    Processes a request for document classification.

    Parameters
    ----------
    file: UploadFile = File(...) 
        Uploaded file.
        
    Return
    ----------
    ClassifyOutputModel
        Output with **label** and **score**.

    """
    document = await file.read()
    document = parse_document(document)

    pred = docs_classifier.predict(document)[0]   
    
    if pred['score'] < threshold:
        pred['label'] = "Не определен"
    
    return ClassifyOutputModel(label=pred["label"], score=pred["score"])


@router.post("/entity-recognize")
def entity_recognize(input: EntityRecognizeInputModel) -> EntityRecognizeOutputModel:
    pass
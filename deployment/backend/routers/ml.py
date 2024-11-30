import os
import json

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from common.ml.schemes import *
from common.ml.utils import *

from common.parser.utils import *

from common.db.schemes import *
from common.db.utils import *


router = APIRouter()

# Initialize the document classifier
docs_classifier = DocsClassifier(model_path="models/docs-classifier", tokenizer_path="models/docs-classifier")


@router.post("/summarize")
def summarize(input: SummarizeInputModel, n_sentences_to_keep: int = 2) -> str:
    """
    A route to make a summary of the input text.

    Parameters
    ----------
    input : InputModel
        Input with **text** and sampling **params**,
    n_sentences_to_keep : int, optional
        Number of sentences to keep in result summary.
    """

    change_current_lora_adapter(adapter_id=int(os.environ.get("SUMMARY_LORA_ADAPTER_ID")))

    # preprocess input text
    text = get_preprocessed_text(text=input.text)
    # make request to llama.cpp server
    summary = get_completion(prompt=text, params=input.params.model_dump())
    # reduce summary
    summary = get_reduced_summary(summary=summary, n_sentences_to_keep=n_sentences_to_keep)

    return summary


@router.post("/generate")
async def generate(input: GenerateInputModel) -> StreamingResponse:
    change_current_lora_adapter(adapter_id=int(os.environ.get("GENERATE_LORA_ADAPTER_ID")))
    
    # generate document based on fields:
    document_as_text = get_completion(prompt=json.dumps(input.fields, ensure_ascii=False), params=input.params.model_dump())
    
    # transform document in text format to byte
    document_as_byte = text_to_docx_bytes(document_as_text)
    
    # upload document to mongodb
    upload_document(
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


@router.post("/classify")
def classify(input: ClassifyInputModel) -> ClassifyOutputModel:
    """
    Processes a request for document classification.

    Parameters
    ----------
    input: ClassifyInputModeltext 
        Input with **text** and **thereshold**(str).
        
    Return
    ----------
    ClassifyOutputModel
        Output with **label** and **score**.

    """
    pred = docs_classifier.predict(input.text)[0]   
    if pred['score'] < input.thereshold:
        pred['label'] = 'Не определен'
    return ClassifyOutputModel(label=pred["label"], score=pred["score"])


@router.post("/entity-recognize")
def entity_recognize(input: EntityRecognizeInputModel) -> EntityRecognizeOutputModel:
    pass
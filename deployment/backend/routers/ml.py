import os
import io
import json

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from common.ml.schemes import *
from common.ml.utils import *

from common.parser.utils import parse_document, text_to_docx_bytes

from common.db.schemes import *
from common.db.utils import *
from common.ml.ner import DocEntityRecognizer

router = APIRouter()

# initialize the document classifier
docs_classifier = DocsClassifier(model_path="models/docs-classifier", tokenizer_path="models/docs-classifier")
docs_ner = DocEntityRecognizer()

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
async def entity_recognize(file: UploadFile = File(...)) -> List: #List[EntityRecognizeResult]:
    document = await file.read()
    document: str = parse_document(document)

    recognizer_result = docs_ner.predict(document)
    return recognizer_result
    # return [EntityRecognizeResult(**recognizer) for recognizer in recognizer_result]
    # return EntityRecognizeOutputModel(recognizer_result=recognizer_result)

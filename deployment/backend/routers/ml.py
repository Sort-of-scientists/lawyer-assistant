import os
import io
import json
import base64

import common.ml.utils as ml_utils
import common.db.utils as db_utils

from fastapi import APIRouter, UploadFile, File
from fastapi.responses import StreamingResponse

from datetime import datetime

from common.ml.schemes import *

from common.parser.utils import parse_document, text_to_docx_bytes

from common.db.schemes import *

from common.db.utils import *
from common.ml.ner import DocEntityRecognizer
from common.ml.utils import DocsClassifier

router = APIRouter()

# initialize the document classifier

docs_classifier = DocsClassifier(model_path="models/docs-classifier", tokenizer_path="models/docs-classifier")
docs_ner = DocEntityRecognizer()


SYSTEM_PROMPT = """Ты — ИИ-помощник. Тебе дано задание: необходимо сгенерировать подробный и развернутый ответ.

### Инструкция:
Сгенерируй документ относительно входных данных

### Входные данные:
{}

### Ответ:
{}"""



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

    # prompt to LLM
    prompt = json.dumps(input.fields, ensure_ascii=False)
    prompt = SYSTEM_PROMPT.format(prompt, "")
    
    # generate document based on fields:
    document_as_text = ml_utils.get_completion(prompt=prompt, params=input.params.model_dump())
    
    # transform document in text format to byte
    document_as_byte = text_to_docx_bytes(document_as_text)
    
    # upload document to mongodb
    db_utils.upload_document(
        Document(
            file=document_as_byte,
            name=f"{input.type}",
            info=DocumentInfo(
                header=input.type, description="Описание документа"
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
def classify(text: str) -> ClassifyOutputModel:
    """
    Processes a request for document classification.

    Parameters
    ----------
    input: ClassifyInputModel
        Classifier input model.
        
    Return
    ----------
    ClassifyOutputModel
        Output with **label** and **score**.

    """

    pred = docs_classifier.predict(text)[0]   
    
    if pred['score'] < docs_classifier.DEFAULT_THRESHOLD:
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


@router.post("/upsert")
async def upsert_document(file: UploadFile = File(...), document_id: str | None = None):
    file_content = await file.read()
    text = parse_document(file_content)

    classifier_output = classify(text)
    ner_output = entity_recognize(text)

    info = DocumentInfo(header=classifier_output.label, description=classifier_output.label)
    type = DocumentType(label=classifier_output.label, score=classifier_output.score)
    ents = [Entity(value=ent.value, label=ent.label, score=ent.score, start=ent.start, end=ent.end) for ent in ner_output]
    
    document = Document(file=text_to_docx_bytes(text), name=file.filename, info=info, type=type, entities=ents)
    
    if document_id is None:
        return db_utils.upload_document(
            document=document
        )

    else:
        return db_utils.update_document(
            document_id=document_id, new_document=document
        )

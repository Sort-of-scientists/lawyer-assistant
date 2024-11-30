import re
import os

from fastapi import HTTPException, APIRouter
from typing import List, Dict, Any

from pydantic import BaseModel

from common.llm.models import SamplingParams
from common.llm.utils import get_completion, change_current_lora_adapter


class InputModel(BaseModel):
    """
    A model to represent an input to **/complete** route.

    Parameters
    ----------
    text : str
        Input text to summarize,
    params : str
        Generation parameters.
    """

    text: str
    params: SamplingParams


class OutputModel(BaseModel):
    """
    A model to represent an output from **/complete** route.

    Parameters
    ----------
    text : str
        Summarized text.
    """

    text: str
    

def get_preprocessed_text(text: str) -> str:
    """
    Preprocess text to remove unnecessary spaces, **\\n**, **\\r**, **\\t** symbols.

    Parameters
    ----------
    text : str

    Returns
    -------
    str
    """

    text = text.replace("\n", " ").replace("\t", " ").replace("\r", " ")
    text = re.sub(' +', ' ', text)

    return text

    
def get_reduced_summary(summary: str, n_sentences_to_keep: int) -> str:
    """
    Returns reduced summary. If summary has more than **n_sentences_to_keep** sentences, this func will remain only first **n_sentences_to_keep**.

    Parameters
    ----------
    summary : str
        
    n_sentences_to_keep : int

    Returns
    -------
    str
        Reduced summary.
    """

    if n_sentences_to_keep <= 0:
        raise ValueError("n_sentences_to_keep must be a positive integer.")
    
    sentences = re.split(r'(?<=[.!?])\s+', summary.strip())

    if len(sentences) <= n_sentences_to_keep:
        return summary
    
    reduced_summary = " ".join(sentences[:n_sentences_to_keep])

    return reduced_summary


router = APIRouter()


@router.post("/summarize")
def summarize(input: InputModel, n_sentences_to_keep: int = 2) -> OutputModel:
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

    return OutputModel(text=summary)

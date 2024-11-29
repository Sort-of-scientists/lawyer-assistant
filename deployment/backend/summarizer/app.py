import re
import requests

from fastapi import FastAPI, HTTPException
from typing import List, Dict, Any

from pydantic import BaseModel


LLAMACPP_SERVER_ENDPOINT = "http://llamacpp-server:8080/completion"


class Params(BaseModel):
    """
    A model to represent sampling params to LLM.

    Parameters
    ----------
    n_predict : int
        Number of tokens to generate,

    temperature : int
        Temperature of generation. As big, as more randomly output will be.
    """

    n_predict: int = 100
    temperature: float = 0.01


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
    params: Params


class OutputModel(BaseModel):
    """
    A model to represent an output from **/complete** route.

    Parameters
    ----------
    text : str
        Summarized text.
    """

    text: str


def get_summary(prompt: str, params: Dict[str, Any], endpoint: str = LLAMACPP_SERVER_ENDPOINT) -> str:
    """
    Make a request to llama.cpp server to get summary with LLM.

    Parameters
    ----------
    prompt : str
        The prompt to send to the LLM for summarization.
        
    params : Dict[str, Any]
        Additional parameters for the request (e.g., temperature, max_tokens).
        
    endpoint : str, optional
        The server endpoint for the LLM API. Default is LLAMACPP_SERVER_ENDPOINT.

    Returns
    -------
    str
        The response from the LLM summarization API.
    """

    try:
        response = requests.post(
            url=endpoint,
            headers={
                'Content-Type': 'application/json',
            },
            json={"prompt": prompt} | params
        )

        response.raise_for_status()

        return response.json().get("content", "No content found in response.")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the server: {e}")
    

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


app = FastAPI()


@app.get("/")
def read_root():
    return {}


@app.post("/complete")
def complete(input: InputModel, n_sentences_to_keep: int = 2) -> OutputModel:
    """
    A route to make a summary of the input text.

    Parameters
    ----------
    input : InputModel
        Input with **text** and sampling **params**,
    n_sentences_to_keep : int, optional
        Number of sentences to keep in result summary.
    """

    # preprocess input text
    text = get_preprocessed_text(text=input.text)
    # make request to llama.cpp server
    summary = get_summary(prompt=text, params=input.params.model_dump())
    # reduce summary
    summary = get_reduced_summary(summary=summary, n_sentences_to_keep=n_sentences_to_keep)

    return OutputModel(text=summary)

from pydantic import BaseModel
from typing import Dict, List


class SamplingParams(BaseModel):
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


class SummarizeInputModel(BaseModel):
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


class GenerateInputModel(BaseModel):
    """
    A model to represent input to **/generate** method.

    Attributes
    ----------
    type : str
        Type of the document: "Акты", "Жалобы", etc.

    fields : Dict[str, str]
        Dynamic fields of the specific document type.

    params : SamplingParams
        Params to LLM generation: max_new_tokens, temperature, etc. 
    """
    
    type: str
    fields: Dict[str, str]
    params: SamplingParams


class ClassifyInputModel(BaseModel):
    """
    A model to represent input to **/classify** method.

    Attributes
    ----------
    text : str
        Text to classify.   
    """
    
    text: str


class ClassifyOutputModel(BaseModel):
    """
    A model to represent output from **/classify** method.

    Attributes
    ----------
    label : str 
        The predicted label (class).
        
    score : float 
        The confidence score of the prediction (a value between 0 and 1).
    """
    
    label: str
    score: float


class EntityRecognizeInputModel(BaseModel):
    """
    A model to represent input to **/entity-recognize** method.

    Attributes
    ----------
    """
    text: str


class EntityRecognizeResult(BaseModel):
    """
    A model representing the output of named entity recognition (NER).

    Attributes
    ----------
    value : str
        The recognized entity value.

    label : str
        The type of the recognized entity (e.g., PERSON, ORGANIZATION).

    score : float
        The confidence score of the recognition (a value between 0 and 1).

    start : int
        The starting index of the recognized entity in the input text.

    end : int
        The ending index of the recognized entity in the input text.
    """
    value: str
    label: str
    score: float
    start: int
    end: int


class EntityRecognizeOutputModel(BaseModel):
    """
    A model to represent the output from the **/entity-recognize** method.

    Attributes
    ----------
    recognizer_result : List[EntityRecognizeResult]
        A list of recognized entities and their associated details from the input text.
    """
    recognizer_result: List  # [EntityRecognizeResult]


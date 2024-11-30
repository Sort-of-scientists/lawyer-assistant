from pydantic import BaseModel
from typing import Dict


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
        
    thereshold : float    
        Classification reliability threshold.    
    """
    
    text: str
    thereshold: float


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
    pass


class EntityRecognizeOutputModel(BaseModel):
    """
    A model to represent input to **/entity-recognize** method.

    Attributes
    ----------
    """
    pass
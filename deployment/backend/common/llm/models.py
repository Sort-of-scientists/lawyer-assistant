from pydantic import BaseModel


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
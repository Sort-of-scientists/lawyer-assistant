from typing import Tuple

def get_ner_result(text: str, threshold: float = 0.4) -> Tuple[str, float]:
    """
    Return a classification result

    Parameters
    ----------
    text : str
        
    threshold : float

    Returns
    -------
    Tuple[str, float]
        The first element is label, the second is score.
    """
    pass
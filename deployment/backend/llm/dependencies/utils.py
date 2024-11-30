import requests

from typing import Dict, Any
from fastapi import HTTPException


def get_response_from_llamacpp_server(prompt: str, params: Dict[str, Any], endpoint: str) -> str:
    """
    Make a request to llama.cpp server.

    Parameters
    ----------
    prompt : str
        The prompt to send to the LLM API.
        
    params : Dict[str, Any]
        Additional parameters for the request (e.g., temperature, max_tokens).
        
    endpoint : str, optional
        The server endpoint for the LLM API.

    Returns
    -------
    str
        The response from the LLM API.
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
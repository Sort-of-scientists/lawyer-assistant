import requests

from typing import Dict, Any, List
from fastapi import HTTPException

from dataclasses import dataclass


LLAMACPP_SERVER = "http://llamacpp-server:8080"


def get_completion(prompt: str, params: Dict[str, Any]) -> str:
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
        The responsed completion from the LLM API.
    """

    try:
        response = requests.post(
            url=LLAMACPP_SERVER + "/completion",
            headers={
                'Content-Type': 'application/json',
            },
            json={"prompt": prompt} | params
        )

        response.raise_for_status()

        return response.json().get("content", "No content found in response.")
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the server: {e}")
    

def get_lora_adapters() -> List[Dict[str, str | float]]:
    """
    Get all available LoRA adapters.

    Returns
    -------
    List[Dict[str, str | float]]
        List of LoRA adapters.
    """

    try:
        response = requests.get(
            url=LLAMACPP_SERVER + "/lora-adapters",
            headers={
                'Content-Type': 'application/json',
            },
        )

        response.raise_for_status()

        # get all available adapters
        adapters = response.json()
    
        return adapters
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the server: {e}")
    

def get_current_lora_adapter(adapters: List[Dict[str, str | float]]) -> Dict[str, str | float]:
    """
    Returns current (with scale > 0) LoRA adapter (id, path and scale). 

    Returns
    -------
    List[Dict[str, str | float]]
        List of LoRA adapters
    """

    adapters = [adapter for adapter in adapters if adapter["scale"] > 0]

    if len(adapters) > 1:
        raise Exception("There are more than one LoRA adapter with scale > 0.")

    return adapters[0]
    
    
def change_current_lora_adapter(adapter_id: int) -> Dict[str, str | float]:
    """
    Change current LoRA adapter: set scale to adapter with **id** to 1.0 and 0.0 for others.

    Parameters
    ----------
    id : int
        ID of new current adapter.

    Returns
    -------
    Dict[str, str | float]
        New current adapter.
    """
    # get all available adapters
    adapters = get_lora_adapters()
    # set scale to 1.0 to adapter with id = adapter_id
    adapters = [
        {"id": adapter["id"], "scale": 1.0 if adapter["id"] == adapter_id else 0} for adapter in adapters
    ]

    # TODO: add if need logic
    
    # make a request to llama.cpp server
    try:
        response = requests.post(
            url=LLAMACPP_SERVER + "/lora-adapters",
            headers={
                'Content-Type': 'application/json',
            },
            json=adapters
        )

        response.raise_for_status()
    
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Failed to connect to the server: {e}")
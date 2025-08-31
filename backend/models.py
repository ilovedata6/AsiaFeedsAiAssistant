from pydantic import BaseModel
from typing import Literal


class GenerateRequest(BaseModel):
    """Request model for the generate endpoint."""
    model: Literal["llama3.2:3b", "qwen3:4b"] = "llama3.2:3b"
    prompt: str
    thinking: bool = False


class GenerateResponse(BaseModel):
    """Response model for the generate endpoint."""
    response: str


class OllamaRequest(BaseModel):
    """Request model for Ollama API."""
    model: str
    prompt: str
    stream: bool = False


class OllamaResponse(BaseModel):
    """Response model from Ollama API."""
    response: str
    done: bool = True

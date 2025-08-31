import httpx
from typing import Dict, Any
from .services import AIModelService
from .models import OllamaRequest, OllamaResponse


class OllamaService(AIModelService):
    """Service to interact with Ollama API."""
    
    def __init__(self, base_url: str = "http://localhost:11434"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/api/generate"
    
    async def generate_response(self, prompt: str, model: str) -> str:
        """
        Generate response from Ollama model.
        
        Args:
            prompt: User prompt
            model: Model name to use
            
        Returns:
            Generated response text
            
        Raises:
            httpx.RequestError: If request fails
            ValueError: If response is invalid
        """
        request_data = OllamaRequest(
            model=model,
            prompt=prompt,
            stream=False
        )
        
        async with httpx.AsyncClient(timeout=60.0) as client:
            try:
                response = await client.post(
                    self.generate_url,
                    json=request_data.model_dump(),
                    headers={"Content-Type": "application/json"}
                )
                response.raise_for_status()
                
                response_data = response.json()
                
                if "response" not in response_data:
                    raise ValueError("Invalid response format from Ollama")
                
                return response_data["response"]
                
            except httpx.RequestError as e:
                raise httpx.RequestError(f"Failed to connect to Ollama: {e}")
            except ValueError as e:
                raise ValueError(f"Invalid response from Ollama: {e}")

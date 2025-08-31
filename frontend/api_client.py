import requests
from typing import Dict, Any, Optional
import logging

logger = logging.getLogger(__name__)


class APIClient:
    """Client to interact with the FastAPI backend."""
    
    def __init__(self, base_url: str = "http://localhost:8000"):
        self.base_url = base_url
        self.generate_url = f"{base_url}/generate"
    
    def generate_response(
        self, 
        prompt: str, 
        model: str = "llama3.2:3b", 
        thinking: bool = False
    ) -> Dict[str, Any]:
        """
        Send request to FastAPI backend to generate response.
        
        Args:
            prompt: User prompt
            model: Model to use
            thinking: Whether to use thinking mode
            
        Returns:
            Response from API
            
        Raises:
            requests.RequestException: If request fails
        """
        payload = {
            "model": model,
            "prompt": prompt,
            "thinking": thinking
        }
        
        try:
            response = requests.post(
                self.generate_url,
                json=payload,
                headers={"Content-Type": "application/json"},
                timeout=60
            )
            response.raise_for_status()
            return response.json()
            
        except requests.RequestException as e:
            logger.error(f"API request failed: {e}")
            raise
    
    def health_check(self) -> bool:
        """
        Check if the API backend is healthy.
        
        Returns:
            True if healthy, False otherwise
        """
        try:
            response = requests.get(f"{self.base_url}/health", timeout=5)
            return response.status_code == 200
        except requests.RequestException:
            return False

from abc import ABC, abstractmethod
from typing import Dict, Any
from config import DEFAULT_MODEL, THINKING_MODEL


class AIModelService(ABC):
    """Abstract base class for AI model services."""
    
    @abstractmethod
    async def generate_response(self, prompt: str, model: str) -> str:
        """Generate response from AI model."""
        pass


class ModelSelector:
    """Service to select appropriate model based on thinking mode."""
    
    @staticmethod
    def select_model(thinking: bool, requested_model: str | None = None) -> str:
        """
        Select the appropriate model based on thinking mode.
        
        Args:
            thinking: Whether thinking mode is enabled
            requested_model: Explicitly requested model
            
        Returns:
            Selected model name
        """
        if thinking:
            return THINKING_MODEL

        if requested_model:
            return requested_model

        return DEFAULT_MODEL

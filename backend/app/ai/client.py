from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Type

from app.ai.exceptions import LLMError


class LLMClient(ABC):
    """Abstract base class for LLM clients."""

    def __init__(
        self,
        model: str,
        temperature: float = 0,
        max_tokens: int = 4000,
        timeout: int = 30,
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        self.timeout = timeout

    @abstractmethod
    async def generate_structured(
        self,
        system_prompt: str,
        user_prompt: str,
        response_schema: type,
    ) -> Any:
        """
        Generate structured output from the LLM.

        Args:
            system_prompt: System prompt to guide the LLM
            user_prompt: User prompt with the actual input
            response_schema: Pydantic schema for validation

        Returns:
            Validated instance of response_schema

        Raises:
            LLMError: If generation fails
            StructuredOutputError: If output cannot be parsed
        """
        pass

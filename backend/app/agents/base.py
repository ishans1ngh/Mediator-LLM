from abc import ABC, abstractmethod
from typing import Any, Generic, TypeVar

from app.core.exceptions import AgentError
from app.core.logging import get_logger

TIn = TypeVar("TIn")
TOut = TypeVar("TOut")

logger = get_logger(__name__)


class BaseAgent(ABC, Generic[TIn, TOut]):
    """Shared async agent interface. LLM implementations replace `_run` later."""

    name: str = "base"

    async def run(self, payload: TIn) -> TOut:
        try:
            return await self._run(payload)
        except AgentError:
            raise
        except Exception as exc:
            logger.exception("agent_failed", extra={"step": self.name})
            raise AgentError(f"{self.name} failed.") from exc

    @abstractmethod
    async def _run(self, payload: TIn) -> TOut:
        raise NotImplementedError

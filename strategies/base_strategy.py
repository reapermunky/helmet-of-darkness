# strategies/base_strategy.py
from abc import ABC, abstractmethod
from typing import List, Tuple, Any

class BaseStrategy(ABC):
    """Abstract Base Class for all encoding strategies."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique, user-facing name of the strategy."""
        pass

    @abstractmethod
    def encode(self, bit_runs: List[Tuple[str, int]]) -> Any:
        """Encodes universal bit runs into the strategy-specific payload."""
        pass

    @abstractmethod
    def decode(self, payload: Any) -> List[Tuple[str, int]]:
        """Decodes a strategy-specific payload back into universal bit runs."""
        pass

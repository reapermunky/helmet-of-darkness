# strategies/rle.py
from typing import List, Tuple, Any
from .base_strategy import BaseStrategy

class RleStrategy(BaseStrategy):
    @property
    def name(self) -> str:
        return "rle"

    def encode(self, bit_runs: List[Tuple[str, int]]) -> Any:
        # For RLE, the universal format is already the payload.
        return bit_runs

    def decode(self, payload: Any) -> List[Tuple[str, int]]:
        # The payload is expected to be in the universal format.
        return [(str(bit), int(count)) for bit, count in payload]

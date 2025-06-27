# strategies/power.py
import re
from typing import List, Tuple, Any
from .base_strategy import BaseStrategy

class PowerStrategy(BaseStrategy):
    @property
    def name(self) -> str:
        return "power"

    def encode(self, bit_runs: List[Tuple[str, int]]) -> Any:
        return [f"{bit}^{count}" for bit, count in bit_runs]

    def decode(self, payload: Any) -> List[Tuple[str, int]]:
        runs = []
        for item in payload:
            match = re.match(r"(\d)\^(\d+)", item)
            if not match:
                raise ValueError(f"Invalid power notation item: {item}")
            runs.append((match.group(1), int(match.group(2))))
        return runs

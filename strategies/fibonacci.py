# strategies/fibonacci.py
from typing import List, Tuple, Any
from .base_strategy import BaseStrategy

def to_fib_representation(n: int) -> List[int]:
    """Converts a number to its Zeckendorf representation."""
    if n == 0: return [0]
    fib = [1, 2]
    while fib[-1] <= n:
        fib.append(fib[-1] + fib[-2])
    
    result = []
    i = len(fib) - 2
    while n > 0 and i >= 0:
        if fib[i] <= n:
            result.append(fib[i])
            n -= fib[i]
            # Zeckendorf's theorem implies no two consecutive Fibonacci numbers are used
            i -= 1 
        i -= 1
    return sorted(result, reverse=True)

class FibonacciStrategy(BaseStrategy):
    @property
    def name(self) -> str:
        return "fibonacci"

    def encode(self, bit_runs: List[Tuple[str, int]]) -> Any:
        return [[bit, to_fib_representation(count)] for bit, count in bit_runs]

    def decode(self, payload: Any) -> List[Tuple[str, int]]:
        return [(item[0], sum(item[1])) for item in payload]

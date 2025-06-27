# utils/display.py
from typing import Any, List, Tuple

def pretty_print_payload(strategy_name: str, payload: Any):
    """Prints the symbolic payload in a human-readable format."""
    print("--- HoD Symbolic Payload ---")
    print(f"Strategy: {strategy_name}")
    
    # This is a simplified view; a real implementation might decode
    # the strategy-specific payload to the universal ('bit', count) format first.
    if isinstance(payload, list) and payload:
        limit = 15
        for i, item in enumerate(payload[:limit]):
            print(f"  Run {i+1:03d}: {item}")
        if len(payload) > limit:
            print(f"  ... and {len(payload) - limit} more runs.")
    else:
        print(f"  Payload: {str(payload)[:200]}...")
    print("----------------------------")


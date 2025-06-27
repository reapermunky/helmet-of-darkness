# utils/core.py
from typing import Iterator, Tuple, BinaryIO

def generate_bit_runs(file_handle: BinaryIO) -> Iterator[Tuple[str, int]]:
    """
    Reads a file byte by byte and yields tuples of ('bit', run_length).
    This is the core symbolic representation generator.
    """
    current_run_bit = None
    current_run_length = 0

    while (byte := file_handle.read(1)):
        for i in range(8):
            bit = '1' if (byte[0] >> (7 - i)) & 1 else '0'
            
            if bit == current_run_bit:
                current_run_length += 1
            else:
                if current_run_bit is not None:
                    yield (current_run_bit, current_run_length)
                current_run_bit = bit
                current_run_length = 1
                
    if current_run_bit is not None:
        yield (current_run_bit, current_run_length)


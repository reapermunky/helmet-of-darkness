# utils/meta.py
import os
from datetime import datetime, timezone
from typing import Optional, Dict, Any

def create_metadata(
    input_filename: str,
    input_size: int,
    strategy_name: str,
    hash_algo: Optional[str] = None,
    file_hash: Optional[str] = None
) -> Dict[str, Any]:
    """Constructs the standard metadata dictionary for a keymap."""
    return {
        "hod_version": "2.0",
        "hod_created_utc": datetime.now(timezone.utc).isoformat(),
        "strategy": strategy_name,
        "original_filename": os.path.basename(input_filename),
        "input_size_bytes": input_size,
        "integrity": {
            "file_hash_algorithm": hash_algo,
            "file_hash": file_hash,
            "payload_hmac_signature": None, # To be filled in later if used
        },
    }


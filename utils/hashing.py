# utils/hashing.py
import hashlib
import hmac
import json
from typing import Any, Dict

def calculate_file_hash(filepath: str, algorithm: str = 'sha256') -> str:
    """Calculates the hash of a file's content."""
    h = hashlib.new(algorithm)
    with open(filepath, 'rb') as f:
        while chunk := f.read(8192):
            h.update(chunk)
    return h.hexdigest()

def sign_payload(payload: Any, passphrase: str) -> str:
    """Generates an HMAC signature for the payload."""
    # Canonicalize payload by sorting keys to ensure consistent JSON string
    payload_bytes = json.dumps(payload, sort_keys=True).encode('utf-8')
    passphrase_bytes = passphrase.encode('utf-8')
    
    signature = hmac.new(passphrase_bytes, payload_bytes, hashlib.sha256)
    return signature.hexdigest()

def verify_payload(payload: Any, signature: str, passphrase: str) -> bool:
    """Verifies the HMAC signature of the payload."""
    expected_signature = sign_payload(payload, passphrase)
    return hmac.compare_digest(expected_signature, signature)


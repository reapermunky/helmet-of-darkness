# formats/json_format.py
import json
from typing import Dict, Any, IO
from .base_format import BaseFormat

class JsonFormat(BaseFormat):
    @property
    def name(self) -> str: return "json"
    
    @property
    def extension(self) -> str: return ".hod"

    def serialize(self, data: Dict[str, Any], stream: IO[str]):
        json.dump(data, stream, indent=2)

    def deserialize(self, stream: IO[str]) -> Dict[str, Any]:
        return json.load(stream)

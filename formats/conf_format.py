# formats/conf_format.py
import configparser
import json
from typing import Dict, Any, IO
from .base_format import BaseFormat

class ConfFormat(BaseFormat):
    @property
    def name(self) -> str: return "conf"

    @property
    def extension(self) -> str: return ".conf"

    def serialize(self, data: Dict[str, Any], stream: IO[str]):
        config = configparser.ConfigParser()
        config.add_section('hod_metadata')
        
        for key, value in data.items():
            if key not in ['payload', 'integrity']:
                config.set('hod_metadata', str(key), str(value))
        
        # Serialize complex nested objects as JSON strings
        config.set('hod_metadata', 'integrity', json.dumps(data['integrity']))

        config.add_section('hod_payload')
        # Serialize the entire payload as a JSON string for robustness
        config.set('hod_payload', 'data', json.dumps(data['payload']))
        
        config.write(stream)

    def deserialize(self, stream: IO[str]) -> Dict[str, Any]:
        config = configparser.ConfigParser()
        config.read_file(stream)
        
        data = {}
        meta = config['hod_metadata']
        for key in meta:
            # Safely evaluate literals, e.g., numbers, bools
            try:
                data[key] = json.loads(meta[key])
            except (json.JSONDecodeError, TypeError):
                data[key] = meta[key]
        
        # Correctly parse the integrity and payload JSON strings
        data['integrity'] = json.loads(meta['integrity'])
        data['payload'] = json.loads(config['hod_payload']['data'])
        
        # Coerce types back
        data['input_size_bytes'] = int(data['input_size_bytes'])
        return data

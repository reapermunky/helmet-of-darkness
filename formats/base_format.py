# formats/base_format.py
from abc import ABC, abstractmethod
from typing import Dict, Any, IO

class BaseFormat(ABC):
    """Abstract Base Class for all output format serializers."""
    
    @property
    @abstractmethod
    def name(self) -> str:
        """The unique name of the format (e.g., 'json', 'csv')."""
        pass
        
    @property
    @abstractmethod
    def extension(self) -> str:
        """The default file extension (e.g., '.hod', '.csv')."""
        pass

    @abstractmethod
    def serialize(self, data: Dict[str, Any], stream: IO[str]):
        """Serializes the keymap dictionary to a stream."""
        pass

    @abstractmethod
    def deserialize(self, stream: IO[str]) -> Dict[str, Any]:
        """Deserializes a stream into the keymap dictionary."""
        pass

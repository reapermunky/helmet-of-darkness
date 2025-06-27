# strategies/__init__.py
import pkgutil
import importlib
from .base_strategy import BaseStrategy

# Dictionary to hold all discovered strategies, keyed by name
STRATEGIES = {}

def load_strategies():
    """Dynamically loads all strategies from this package."""
    if STRATEGIES:
        return
        
    package_path = __path__
    prefix = __name__ + "."
    
    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        module = importlib.import_module(name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, BaseStrategy) and attribute is not BaseStrategy:
                strategy_instance = attribute()
                STRATEGIES[strategy_instance.name] = strategy_instance

load_strategies()

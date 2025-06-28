# formats/__init__.py
import pkgutil
import importlib
from .base_format import BaseFormat

# Dictionary to hold all discovered formats, keyed by name
FORMATS = {}
FORMATS_BY_EXT = {}

def load_formats_by_name():
    """Dynamically loads all formats from this package, keyed by name."""
    if FORMATS:
        return

    package_path = __path__
    prefix = __name__ + "."
    for _, name, _ in pkgutil.iter_modules(package_path, prefix):
        module = importlib.import_module(name)
        for attribute_name in dir(module):
            attribute = getattr(module, attribute_name)
            if isinstance(attribute, type) and issubclass(attribute, BaseFormat) and attribute is not BaseFormat:
                format_instance = attribute()
                FORMATS[format_instance.name] = format_instance

def load_formats_by_ext():
    """Dynamically loads all formats from this package, keyed by extension."""
    if FORMATS_BY_EXT and FORMATS: # Ensure name-based formats are loaded first
        return

    # Ensure formats are loaded by name first if not already
    load_formats_by_name()

    for name, format_instance in FORMATS.items():
        FORMATS_BY_EXT[format_instance.extension] = format_instance

# Initial load when the package is imported
load_formats_by_name()
load_formats_by_ext()
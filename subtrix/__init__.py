"""
Subtrix - Advanced templating engine with pattern substitution.
"""

# Import improved mechanism for backward compatibility
try:
    from .subtrix_improved import ImprovedMechanism as Mechanism
except ImportError:
    # Fallback to original if dependencies are missing
    from .subtrix import Mechanism

from .errors import (
    SubtrixError,
    PatternNotFoundError,
    InvalidDataTypeError,
    ConfigurationError,
    TemplateProcessingError,
    DependencyError,
)

from .utilities import now, today, uuid_generator, get_doc

__version__ = "0.2.0"
__all__ = [
    "Mechanism",
    "SubtrixError",
    "PatternNotFoundError",
    "InvalidDataTypeError",
    "ConfigurationError",
    "TemplateProcessingError",
    "DependencyError",
    "now",
    "today",
    "uuid_generator",
    "get_doc",
]

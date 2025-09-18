# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	    Custom exceptions for Subtrix templating engine.
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

# ======================================3rd Party Library Modules=====================================================||

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class SubtrixError(Exception):
    """Base exception for all Subtrix operations."""

    pass


class PatternNotFoundError(SubtrixError):
    """Raised when a pattern cannot be found in template."""

    pass


class InvalidDataTypeError(SubtrixError):
    """Raised when data type is not supported for processing."""

    pass


class ConfigurationError(SubtrixError):
    """Raised when configuration is invalid or missing."""

    pass


class TemplateProcessingError(SubtrixError):
    """Raised when template processing fails."""

    pass


class DependencyError(SubtrixError):
    """Raised when required dependencies are not available."""

    pass


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

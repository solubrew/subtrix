# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	    Configuration management for Subtrix templating engine.
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from pathlib import Path
from typing import Dict, Any, Optional

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

from .errors import ConfigurationError

# ======================================3rd Party Library Modules=====================================================||

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


class ConfigurationManager:
    """Manages configuration loading and validation for Subtrix."""

    def __init__(self, config_path: str):
        """
        Initialize configuration manager.

        Args:
            config_path: Path to the configuration file
        """
        self.config_path = Path(config_path)
        self._config = None

    def load_config(self, override_cfg: Optional[Dict] = None) -> Dict[str, Any]:
        """
        Load and validate configuration.

        Args:
            override_cfg: Optional configuration overrides

        Returns:
            Validated configuration dictionary

        Raises:
            ConfigurationError: If configuration is invalid
        """
        try:
            # Try to load with condor if available
            try:
                from condor import condor

                self._config = condor.Instruct(str(self.config_path))
                if override_cfg:
                    self._config = self._config.override(override_cfg)
                config_dict = self._config.dikt
            except ImportError:
                # Fallback to basic YAML loading
                config_dict = self._load_yaml_fallback()
                if override_cfg:
                    config_dict.update(override_cfg)

            self._validate_config_structure(config_dict)
            return config_dict

        except Exception as e:
            raise ConfigurationError(f"Failed to load configuration: {e}")

    def _load_yaml_fallback(self) -> Dict[str, Any]:
        """Fallback YAML loading when condor is not available."""
        try:
            import yaml

            with open(self.config_path, "r") as f:
                return yaml.safe_load(f)
        except ImportError:
            # Final fallback - basic JSON structure
            return {
                "sequence": ["varr", "sub", "loop", "sub"],
                "processors": {
                    "sub": {
                        "base": {
                            "pattern": {
                                "initialize": [{"symbol": "<["}],
                                "finalize": [{"symbol": "]>"}],
                                "processors": {},
                            }
                        }
                    },
                    "loop": {
                        "base": {
                            "pattern": {
                                "initialize": [{"symbol": "<["}],
                                "finalize": [{"symbol": "]>"}],
                                "processors": {},
                            }
                        }
                    },
                    "varr": {
                        "base": {
                            "pattern": {
                                "initialize": [{"symbol": "<("}],
                                "finalize": [{"symbol": ")>"}],
                                "processors": {},
                            }
                        }
                    },
                },
            }

    def _validate_config_structure(self, config: Dict[str, Any]) -> None:
        """
        Validate that required configuration sections exist.

        Args:
            config: Configuration dictionary to validate

        Raises:
            ConfigurationError: If required sections are missing
        """
        required_sections = ["sequence", "processors"]
        for section in required_sections:
            if section not in config:
                raise ConfigurationError(f"Missing required config section: {section}")

        # Validate processor structure
        for processor in config["processors"].values():
            if "base" not in processor or "pattern" not in processor["base"]:
                raise ConfigurationError("Invalid processor configuration structure")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

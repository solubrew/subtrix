# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name:
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from typing import Dict, List, Tuple, Any

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

from .errors import PatternNotFoundError

# ======================================3rd Party Library Modules=====================================================||

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")

"""
Template parsing functionality for Subtrix.
"""


class TemplateParser:
    """Handles template parsing and pattern extraction."""

    def __init__(self, template: str, config: Dict[str, Any]):
        """
        Initialize template parser.

        Args:
            template: Template string to parse
            config: Configuration dictionary
        """
        self.template = template
        self.config = config
        self._pattern_cache = {}

    def collect_symbols(self, symcfg: Dict[str, Any]) -> List[str]:
        """
        Collect symbols from configuration.

        Args:
            symcfg: Symbol configuration dictionary

        Returns:
            List of symbols found in configuration
        """
        find_patterns = []
        for fix in symcfg.keys():
            if symcfg[fix] is None:
                continue
            for i in range(len(symcfg[fix])):
                find_patterns.append(symcfg[fix][i]["symbol"])
        return find_patterns

    def find_pattern(self, cfg: Dict[str, Any], i: int, offset: int = 0) -> Tuple[int, int, Dict, str, str]:
        """
        Find and extract pattern information from template.

        Args:
            cfg: Configuration dictionary
            i: Pattern index
            offset: Offset in template

        Returns:
            Tuple of (start_loc, end_loc, fix_map, key, code)

        Raises:
            PatternNotFoundError: If pattern configuration is invalid
        """
        try:
            start_pattern = cfg["base"]["pattern"]["initialize"][i]["symbol"]
            end_pattern = cfg["base"]["pattern"]["finalize"][i]["symbol"]
        except (KeyError, IndexError) as e:
            raise PatternNotFoundError(f"Invalid pattern configuration: {e}")

        # Use cached pattern if available
        cache_key = f"{start_pattern}_{end_pattern}_{offset}"
        if cache_key in self._pattern_cache:
            return self._pattern_cache[cache_key]

        tmplt = self.template[offset:]

        start_loc = tmplt.find(start_pattern)
        if start_loc == -1:
            result = (-1, -1, {}, "", "")
            self._pattern_cache[cache_key] = result
            return result

        end_loc = tmplt.find(end_pattern, start_loc + len(start_pattern))
        if end_loc == -1:
            result = (-1, -1, {}, "", "")
            self._pattern_cache[cache_key] = result
            return result

        end_loc += len(end_pattern)

        # Extract and process the pattern
        key = tmplt[start_loc:end_loc]
        fix_map = {}
        code = f"{start_pattern}{key}{end_pattern}" if start_pattern not in key else key

        # Process fix symbols if present
        fix_symbols = self.collect_symbols(cfg["base"]["pattern"]["processors"])
        if any(symbol in key for symbol in fix_symbols):
            key, fix_map = self._process_fixes(key, fix_symbols, start_pattern, end_pattern)

        # Adjust for offset
        start_loc += offset
        end_loc += offset

        result = (start_loc, end_loc, fix_map, key, code)
        self._pattern_cache[cache_key] = result
        return result

    def _process_fixes(self, term: str, fix_symbols: List[str], start_pat: str, end_pat: str) -> Tuple[str, Dict]:
        """
        Process fix symbols in a term.

        Args:
            term: Term to process
            fix_symbols: List of fix symbols
            start_pat: Start pattern
            end_pat: End pattern

        Returns:
            Tuple of (clean_term, fix_map)
        """
        clean_term = term
        fixmap = {}
        fpats = [start_pat] + fix_symbols + [end_pat]

        # Find clean term
        for symbols in [[".:", ":."], [start_pat, ".:"], [start_pat, ":."], [start_pat, end_pat]]:
            start_pos = term.find(symbols[0])
            if start_pos != -1:
                remaining = term[start_pos:]
                end_pos = remaining.find(symbols[1])
                if end_pos != -1:
                    clean_term = f"{start_pat}{term[start_pos + len(symbols[0]):start_pos + end_pos]}{end_pat}"
                    break

        # Process fix patterns
        for i in range(len(fpats) - 1):
            fpat, lpat = fpats[i], fpats[i + 1]
            start_pos = term.find(fpat)
            if start_pos == -1:
                continue

            n = start_pos + len(fpat)
            end_pos = term.find(lpat, n)
            if end_pos == -1:
                continue

            fixmap[fpat] = {"final_term": term[n:end_pos], "pos": [n, end_pos]}

        return clean_term, fixmap


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

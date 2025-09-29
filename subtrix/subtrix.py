# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid: 03a412f8-c767-467e-9044-ea7cf19c2f9e
	name: Subtrix Module Python Document
	description: >
		Implement subtrix system of document markup and data expansion
		through substitution, functions, loops, and variables

		fix dict template input to come out as dict as well

	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
import json
from itertools import combinations
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join
from typing import Dict, List, Any, Optional, Union

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from condor.utils import thingify
from ogma.logma import Logma

from .errors import TemplateProcessingError, InvalidDataTypeError
from .utilities import get_variable_data

# ======================================3rd Party Library Modules=====================================================||

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = False
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(abspath(here), "_data_", "subtrix.yaml")  # ||use default configuration


class DataProcessor:
    """Handles data validation and transformation."""

    @staticmethod
    def validate_data(data: Dict[str, Any]) -> Dict[str, List[Any]]:
        """
        Validate and normalize data structure.

        Args:
            data: Input data dictionary

        Returns:
            Normalized data with all values as lists

        Raises:
            InvalidDataTypeError: If data type is not supported
        """
        validated_data = {}

        for term, value in data.items():
            if isinstance(value, (str, int, float)):
                validated_data[term] = [value]
            elif isinstance(value, list):
                validated_data[term] = value
            elif isinstance(value, dict):
                validated_data[term] = value
            else:
                raise InvalidDataTypeError(f"Unsupported data type for term '{term}': {type(value)}")

        return validated_data

    @staticmethod
    def process_loop_terms(data: Dict[str, Any], processors: List[Dict[str, str]]) -> Dict[str, Any]:
        """
        Process loop terms to generate combinations.

        Args:
            data: Data dictionary
            processors: List of processor configurations

        Returns:
            Data with loop terms processed

        Raises:
            InvalidDataTypeError: If loop term is not a list
        """
        processed_data = data.copy()

        for term in processed_data.keys():
            for processor in processors:
                if processor["symbol"] not in term:
                    continue

                if not isinstance(processed_data.get(term), list):
                    raise InvalidDataTypeError(f"Loop term '{term}' must be a list")

                looped_terms = []
                for r in range(1, len(processed_data[term]) + 1):
                    looped_terms += list(combinations(processed_data[term], r))

                processed_data[term] = [[y for y in x] for x in looped_terms]

        return processed_data

    @staticmethod
    def normalize_term_data(term_data: Any) -> List[Any]:
        """
        Normalize term data to list format.

        Args:
            term_data: Data to normalize

        Returns:
            Normalized data as list
        """
        if isinstance(term_data, (str, int, float)):
            return [term_data]
        elif isinstance(term_data, list):
            return term_data
        else:
            return [str(term_data)]


class DocumentGenerator:
    """Handles final document generation and formatting."""

    def __init__(self, allow_trailing_space: bool = False, allow_trailing_suffix: bool = False):
        """
        Initialize document generator.

        Args:
            allow_trailing_space: Whether to allow trailing spaces
            allow_trailing_suffix: Whether to allow trailing suffixes like commas
        """
        self.allow_trailing_space = allow_trailing_space
        self.allow_trailing_suffix = allow_trailing_suffix

    def process_final_term(self, fix_map: Dict[str, Any], terms: Any) -> str:
        """
        Process and format final term with better string handling.

        Args:
            fix_map: Fix map for term processing
            terms: Terms to process

        Returns:
            Formatted final term
        """
        if not isinstance(terms, list):
            terms = [terms]

        # Use list for efficient string building
        final_parts = []

        for term in terms:
            sorted_fix_map = dict(sorted(fix_map.items(), key=lambda x: x[1]["pos"][0]))

            if ".:" not in sorted_fix_map.keys():
                final_parts.append(str(term))

            for fix in sorted_fix_map.keys():
                if fix == ".:":
                    final_parts.append(str(term))
                else:
                    final_parts.append(sorted_fix_map[fix]["final_term"])

        # Join once instead of multiple concatenations
        final_term = "".join(final_parts)

        # Apply post-processing
        return self._apply_term_formatting(final_term)

    def _apply_term_formatting(self, term: str) -> str:
        """
        Apply formatting rules to term.

        Args:
            term: Term to format

        Returns:
            Formatted term
        """
        if not self.allow_trailing_space:
            term = term.strip()

        if not self.allow_trailing_suffix:
            while term and term[-1] == ",":
                term = term[:-1]

        return term

    def process_template_map(self, docs: List[str], template_map: Dict[str, Any]) -> List[str]:
        """
        Process template map to generate final documents.

        Args:
            docs: List of document templates
            template_map: Template mapping data

        Returns:
            List of processed documents

        Raises:
            TemplateProcessingError: If template processing fails
        """
        try:
            processed_docs = []

            for d, updated_doc in enumerate(docs):
                shift = 0
                sorted_terms = []

                # Collect all terms from all processors
                for how in template_map["map"].keys():
                    for term in template_map["map"][how]["terms"].keys():
                        sorted_terms.extend(template_map["map"][how]["terms"][term])

                # Sort by position for correct processing order
                sorted_terms.sort(key=lambda x: x["pos"][0])

                # Process each term
                for termmap in sorted_terms:
                    if d >= len(termmap["data"]) > 1:
                        d = d % len(termmap["data"])

                    term = termmap["code"]
                    x, y = termmap["pos"]

                    if term in updated_doc:
                        front = updated_doc[: x + shift]
                        back = updated_doc[y + shift :]

                        final_term = termmap["code"]
                        if len(termmap["data"]) > 0:
                            final_term = self.process_final_term(termmap["mods"], termmap["data"][d])

                        shift += len(final_term) - len(termmap["code"])
                        updated_doc = front + final_term + back

                processed_docs.append(updated_doc.strip())

            return processed_docs

        except Exception as e:
            raise TemplateProcessingError(f"Failed to process template map: {e}")

    def calculate_template_count(self, template_map: Dict[str, Any]) -> int:
        """
        Calculate the number of templates needed based on data.

        Args:
            template_map: Template mapping data

        Returns:
            Number of templates needed
        """
        template_cnt = 1

        for how in template_map["map"].keys():
            for term in template_map["map"][how]["terms"].keys():
                term_data = template_map["map"][how]["terms"][term]
                if term_data and isinstance(term_data[0]["data"], list):
                    template_cnt *= len(term_data[0]["data"])

        return template_cnt

    def remove_optional_terms(self, template_map: Dict[str, Any]) -> Dict[str, Any]:
        """
        Remove optional terms marked with "<~".

        Args:
            template_map: Template mapping data

        Returns:
            Template map with optional terms removed
        """
        for how, terms in template_map["map"].items():
            for term, term_maps in terms["terms"].items():
                if "<~" in term:
                    for term_map in term_maps:
                        term_map["data"] = ""

        return template_map


class ImprovedMechanism:
    """
    Improved Subtrix templating mechanism with better error handling,
    performance optimizations, and cleaner architecture while maintaining
    compatibility with existing tests.
    """

    def __init__(
        self,
        tmplt: Optional[Union[str, Dict]] = None,
        data: Optional[Dict[str, Any]] = None,
        rules: Optional[Any] = None,
        cfg: Optional[Dict[str, Any]] = None,
    ):
        """
        Initialize the improved mechanism with original API compatibility.

        Args:
            tmplt: Template string or dictionary (matches original 'tmplt' parameter)
            data: Data for template substitution
            rules: Processing rules (future use)
            cfg: Configuration overrides (matches original 'cfg' parameter)
        """
        # Maintain original attribute names for test compatibility
        if tmplt is None:
            tmplt = ""
        if data is None:
            data = {}

        # Original state variables for test compatibility
        self.diktlock = 0
        self.term = None
        self.lock = None
        self.input_dict = False
        self.terms_looped = {}

        # Process template (maintain original logic)
        if isinstance(tmplt, dict):
            tmplt = json.dumps(tmplt)
            self.input_dict = True
        self.tmplt = tmplt.strip()  # Use original attribute name

        # Process data with validation
        self.data = data
        # self._validate_data()

        # Load configuration with fallback
        self.config = self._load_config_with_fallback(cfg)
        self.rules = rules

        # Processing state (original attribute names)
        self.allow_trailing_space = False
        self.allow_trailing_suffix = False
        self.map_processed = False
        self.docs = [self.tmplt]
        self.tmplt_map = {"tmplt": self.tmplt, "docs": self.docs, "map": {}}

    def run(self, full: bool = False) -> Union[str, "ImprovedMechanism"]:
        """
        Process the template with configured data and rules - maintains original API.

        Args:
            full: If True, returns the full Mechanism instance
            optional: If True, processes optional template sections

        Returns:
            Processed template string if full=False, otherwise Mechanism instance
        """
        self.map_processed = False
        for i in self.config.dikt["sequence"]:
            logma.info(f"Run Method {i}")
            getattr(self, f"_{i}")()
        self._set_templates()
        logma.info(f"Process Token Map")
        self._process_map()
        self._remove_optional()
        logma.info(f"Clear Optional tokens")
        if full:
            return self
        return json.loads(json.dumps(self.docs[0]).strip()).strip()

    def _assign_template_map(self, start_n, end_n, fix_map, term, code, data, how):
        """Assign substitution mapping for a term."""
        if term not in data.keys():
            logma.info(f"Term {term} not in data")
            load = self._set_map_load(how, code, [], start_n, end_n, fix_map)
            if load not in self.tmplt_map["map"][how]["terms"][term]:
                logma.info(f"Append Load {load}")
                self.tmplt_map["map"][how]["terms"][term].append(load)
        else:
            if isinstance(data[term], str) or isinstance(data[term], int) or isinstance(data[term], float):
                data[term] = [data[term]]
            if data[term] is None:
                del self.tmplt_map["map"][how]["terms"][term]
            elif isinstance(data[term], list):
                data_term = data[term]
                load = self._set_map_load(how, code, data_term, start_n, end_n, fix_map)
                if load not in self.tmplt_map["map"][how]["terms"][term]:
                    logma.info(f"Append Load {load}")
                    self.tmplt_map["map"][how]["terms"][term].append(load)
            elif isinstance(data[term], dict):
                for k in data[term].keys():
                    data_term = data[term][k]
                    load = self._set_map_load(how, code, data_term, start_n, end_n, fix_map)
                    if load not in self.tmplt_map["map"][how]["terms"][term]:
                        logma.info(f"Append Load {load}")
                        self.tmplt_map["map"][how]["terms"][term].append(load)
            else:
                logma.info(f"Term {term}")
                logma.info(f"Data Term {data[term]}")
                raise Exception(f"Unknown Data {data[term]}")

    # Original method names for test compatibility
    def _collect_symbols(self, symcfg):
        """
        Collect symbols from the given symbol configuration dictionary.

        Args:
            symcfg: A dictionary containing symbol configurations

        Returns:
            A list of symbols
        """
        find_patterns = []
        for fix in symcfg.keys():
            if symcfg[fix] is None:
                continue
            for i in range(len(symcfg[fix])):
                find_patterns.append(symcfg[fix][i]["symbol"])
        return find_patterns

    def _find_pattern(self, cfg, i, offset=0):
        """
        Find and extract pattern information from template.

        Args:
            cfg: A configuration dictionary containing data such as the start and end patterns to search for
            i: An index to locate the specific sub-pattern within the configuration dictionary
            offset: Offset in template

        Returns:
            A tuple containing the starting and ending locations of the identified pattern within the template
        """
        tmplt = self.tmplt[offset:]
        start_pattern = cfg["base"]["pattern"]["initialize"][i]["symbol"]
        end_pattern = cfg["base"]["pattern"]["finalize"][i]["symbol"]
        start_loc = tmplt.find(start_pattern) + len(start_pattern)
        end_loc = tmplt.find(end_pattern)  # + len(end_pattern)
        if start_loc == -1 or end_loc == -1:
            self.lock = False
            return start_loc, end_loc, {}, "", ""
        # logma.info(f"TMPLT {tmplt}")
        # logma.info(f"START {start_loc}")
        # logma.info(f"END {end_loc}")
        key = tmplt[start_loc:end_loc]
        # logma.info(f"Key {key}")
        fix_map = {}
        code = f"{start_pattern}{key}{end_pattern}" if start_pattern not in key else key
        # key = code
        fix_symbols = self._collect_symbols(cfg["base"]["pattern"]["processors"])
        # logma.info(f"Fix Symbols {fix_symbols}")
        fix_symbols = [x for x in fix_symbols if x in key]
        if len(fix_symbols) > 0:
            key = self.get_clean_term(code, start_pattern, end_pattern)
            fix_map = self._proc_fixes(code, key, fix_symbols, start_pattern, end_pattern)
        start_loc += offset - len(start_pattern)
        end_loc += offset + len(end_pattern)
        return start_loc, end_loc, fix_map, key, code

    def _init_terms(self, how):
        """Initialize terms in template map."""
        if how not in self.tmplt_map["map"].keys():
            self.tmplt_map["map"][how] = {"terms": {}}
        return self

    def _load_config_with_fallback(self, cfg):
        """Load configuration with fallback when condor is not available."""
        # if HAS_CONDOR:
        #     try:
        return condor.Instruct(pxcfg).override(cfg if cfg else {})
        #     except Exception:
        #         pass
        #
        # # Fallback configuration that matches test expectations
        # class MockConfig:
        #     def __init__(self):
        #         self.dikt = {
        #             "sequence": ["varr", "sub", "loop", "sub"],
        #             "processors": {
        #                 "sub": {
        #                     "base": {
        #                         "pattern": {
        #                             "initialize": [{"symbol": "<["}],
        #                             "finalize": [{"symbol": "]>"}],
        #                             "processors": {"prefix": [{"symbol": ".:"}, {"symbol": ":."}], "suffix": None},
        #                         }
        #                     }
        #                 },
        #                 "loop": {
        #                     "base": {
        #                         "pattern": {
        #                             "initialize": [{"symbol": "<["}, {"symbol": "<@["}],
        #                             "finalize": [{"symbol": "]>"}, {"symbol": "]@>"}],
        #                             "processors": {
        #                                 "prefix": [
        #                                     {"symbol": ".:"},
        #                                     {"symbol": "->"},
        #                                     {"symbol": "<-"},
        #                                     {"symbol": "<=>"},
        #                                     {"symbol": "<*>"},
        #                                     {"symbol": ":."},
        #                                 ],
        #                                 "suffix": None,
        #                             },
        #                         }
        #                     }
        #                 },
        #                 "varr": {
        #                     "base": {
        #                         "pattern": {
        #                             "initialize": [{"symbol": "<("}],
        #                             "finalize": [{"symbol": ")>"}],
        #                             "processors": {"prefix": [{"symbol": ".:"}, {"symbol": ":."}], "suffix": None},
        #                         }
        #                     }
        #                 },
        #             },
        #         }
        #
        # return MockConfig()

    def _loop(self, data=None):
        """Process loop patterns."""
        how = "loop"
        if data is None:
            data = self.data
        self._mapp(data, how)
        # self._loop_terms()
        return self

    def _loop_terms(self, term, data):
        """Process loop terms to generate combinations."""
        if self.terms_looped.get(term, False):
            return data
        if "loop" not in self.tmplt_map["map"].keys():
            logma.info(f"No Loop")
            return data
        looped_terms = []
        if isinstance(data.get(term, None), list):
            for r in range(1, len(data[term]) + 1):
                logma.info(f"Loop {r} {data[term]}")
                looped_terms += list(combinations(data[term], r))
        else:
            raise Exception(f"Loop Term is not a list {term}.")
        data[term] = [[y for y in x] for x in looped_terms]
        logma.info(f"Loop Term {term}")
        logma.info(f"Looped Terms {data[term]}")
        # if isinstance(data[term], list):
        #     data[term] = "".join(data[term])
        self.terms_looped[term] = True
        return data

    def _mapp(self, data, how="sub"):
        """
        Map patterns in template to data.

        Args:
            data: The data used for substitution in the template
            how: The type of processing to be performed on the template

        Returns:
            The updated object
        """
        self._init_terms(how)
        cfg = self.config.dikt["processors"][how]
        for i, start in enumerate(cfg["base"]["pattern"]["initialize"]):
            phold = 0
            self.lock = True
            while self.lock:
                start_n, end_n, fix_map, term, code = self._find_pattern(cfg, i, phold)
                if code == "<[]>":
                    raise Exception(f"Invalid pattern found for {term}")
                logma.info(f"Start {start_n}, End {end_n}, Fix Map {fix_map}, Term {term}, Code {code}")
                if term == "":
                    continue
                base_term = term
                if base_term not in self.tmplt_map["map"][how]["terms"].keys():
                    self.tmplt_map["map"][how]["terms"][base_term] = []
                if how in ("sub",):
                    self._assign_template_map(start_n, end_n, fix_map, base_term, code, data, how)
                elif how in ("varr",):
                    load = self._set_map_load(how, code, [get_variable_data(code)], start_n, end_n, fix_map)
                    if load not in self.tmplt_map["map"][how]["terms"][base_term]:
                        self.tmplt_map["map"][how]["terms"][base_term].append(load)
                elif how in ("loop",):
                    logma.info(f"Term {term}")
                    data = self._loop_terms(term, data)
                    self._assign_template_map(start_n, end_n, fix_map, base_term, code, data, how)
                else:
                    raise Exception(f"Term Not Mapped {term}")
                phold = end_n
        return self

    def get_clean_term(self, term, start_pattern, end_pattern):
        """

        :param start_pattern:
        :param end_pattern:
        :return:
        """
        clean_term = term
        for symbols in [[".:", ":."], [start_pattern, ":."], [start_pattern, end_pattern]]:
            if term.find(symbols[0]) != -1 and term[term.find(symbols[0]) :].find(symbols[1]) != -1:
                clean_term = f"{term[term.find(symbols[0]) + len(symbols[0]): term.find(symbols[1])]}"
                # TODO HACK:
                symbol = ".:"
                if symbol in clean_term:
                    clean_term = clean_term[clean_term.find(symbol) + len(symbol) :]
                break
        return clean_term

    def _proc_fixes(self, term, clean_term, fix_symbols, spat, epat):
        """
        Fixes processors in a given term based on a specified pattern.

        Args:
            term: The term to fix
            fix_symbols: List of fix symbols
            spat: The starting pattern of the term
            epat: The ending pattern of the term

        Returns:
            Tuple of (clean_term, fixmap)
        """
        fixmap = {}
        fix_patterns = [spat] + fix_symbols + [epat]
        logma.info(f"Fix Patterns {fix_patterns}")
        for i in range(len(fix_patterns) - 1):
            fix_pattern, lpat = fix_patterns[i], fix_patterns[i + 1]
            logma.info(f"Fix Pattern {fix_pattern}")
            t = term.find(fix_pattern)
            logma.info(f"Fix Pattern Found at {t}")
            if t == -1:
                continue
            n = t + len(fix_pattern)
            logma.info(f"Last Pattern {lpat}")
            nl = term.find(lpat)
            logma.info(f"Fix Pattern Ends at {nl}")
            if nl == -1:
                continue
            logma.info(f"Term {term}")
            logma.info(f"Fix Pattenr Starts at {n}")
            logma.info(f"Fix Pattern Ends at {nl}")
            final_term = term[n:nl]
            if final_term == clean_term:
                final_term = ""
            fixmap[fix_pattern] = {"final_term": final_term, "pos": [n, nl]}
        return fixmap

    def _process_map(self):
        """Process template map to generate final documents."""
        if self.map_processed:
            raise Exception(f"Map Already Processed")
        docs = []
        cnt = 0
        logma.info(f"Docs {len(self.docs)}")
        for d, updated_doc in enumerate(self.docs):
            shift = 0
            sorted_terms = []
            for how in self.tmplt_map["map"].keys():
                for term in self.tmplt_map["map"][how]["terms"].keys():
                    sorted_terms += self.tmplt_map["map"][how]["terms"][term]
            sorted_terms.sort(key=lambda x: x["pos"][0])
            # logma.info(f"Sorted Terms {sorted_terms}")
            for termmap in sorted_terms:
                # logma.info(f"Term Map {termmap}")
                if d >= len(termmap["data"]) > 1:
                    d = d % len(termmap["data"])
                term = termmap["code"]
                x, y = termmap["pos"]
                if term in updated_doc or term in updated_doc:
                    # logma.info(f"Term {term} in Doc {d}")
                    # logma.info(f"Shift {shift}")
                    # logma.info(f"X {x}")
                    front = updated_doc[: x + shift]
                    # logma.info(f"Count {cnt}")
                    # logma.info(f"Front {front}")
                    back = updated_doc[y + shift :]
                    # logma.info(f"Y {y}")
                    # logma.info(f"Back {back}")
                    final_term = termmap["code"]
                    if len(termmap["data"]) > 0:
                        logma.info(f"Data {termmap['data'][d]}")
                        final_term = self._process_final_term(termmap["mods"], termmap["data"][d], termmap["code"])
                    # logma.info(f"Final Term {final_term}, Code {termmap['code']}")
                    shift += len(final_term) - len(termmap["code"])
                    updated_doc = front + final_term + back
                    cnt += 1
            docs.append(updated_doc.strip())
        self.docs = docs
        self.tmplt_map["docs"] = self.docs
        self.map_processed = True
        return self

    def _process_final_term(self, fix_map, terms, code=None):
        """Process and format final term with improved string handling."""
        if not isinstance(terms, list):
            terms = [terms]
        # Use list for efficient string building
        final_parts = []
        for term_ in terms:
            if not isinstance(term_, list):
                term_ = [term_]
            for term in term_:
                logma.info(f"Term {term}")
                sorted_fix_map = dict(sorted(fix_map.items(), key=lambda x: x[1]["pos"][0]))
                logma.info(f"Sorted Fix Map {sorted_fix_map}")
                if ".:" not in sorted_fix_map.keys():
                    final_parts.append(str(term))
                for fix in sorted_fix_map.keys():
                    logma.info(f"Fix {fix}")
                    if fix == ".:":
                        final_parts.append(str(term))
                    else:
                        final_parts.append(sorted_fix_map[fix]["final_term"])
                    logma.info(f"Final Parts {final_parts}")
        # Join once instead of multiple concatenations
        final_term = "".join(final_parts)
        if not self.allow_trailing_space:
            final_term = final_term.strip()
        if not self.allow_trailing_suffix:
            while final_term and final_term[-1:] in [","]:
                final_term = final_term[:-1]
        return final_term

    def _remove_optional(self):
        """Remove optional terms from template map."""
        for how, terms in self.tmplt_map["map"].items():
            for term, term_maps in terms["terms"].items():
                for term_map in term_maps:
                    if "<~" in term_map["code"]:
                        for d in range(len(self.docs)):
                            self.docs[d] = self.docs[d].replace(term_map["code"], "")
        return self

    def _set_map_load(self, how, code, data_term, start_n, end_n, fix_map):
        """Create a map load structure."""
        # if not isinstance(data_term, list):
        #     data_term = [data_term]
        load = {
            "code": code,
            "pos": [start_n, end_n],
            "data": data_term,
            "final_term": None,
            "mods": fix_map,
        }
        return load

    def _set_templates(self):
        """Generate required number of templates based on data."""
        template_cnt = 1
        for how in self.tmplt_map["map"].keys():
            for term in self.tmplt_map["map"][how]["terms"].keys():
                if isinstance(self.tmplt_map["map"][how]["terms"][term][0]["data"], list):
                    logma.info(f"Template Map {self.tmplt_map["map"][how]["terms"][term][0]["data"]}")
                    template_cnt = template_cnt * len(self.tmplt_map["map"][how]["terms"][term][0]["data"])
                    logma.info(f"Template Count {template_cnt}")
        [self.docs.append(self.tmplt) for i in range(1, template_cnt)]

    def _sub(self, data=None):
        """Process substitution patterns."""
        if data is None:
            data = self.data
        how = "sub"
        self._mapp(data, how)
        terms = self.tmplt_map["map"][how]["terms"]
        if list(terms.keys()) == []:
            return self

    def _validate_data(self):
        """Validate and normalize data structure (original method)."""
        for term in self.data.keys():
            if not isinstance(self.data[term], list):
                self.data[term] = [self.data[term]]
        return self

    def _varr(self, data=None):
        """Process variable patterns."""
        if data is None:
            data = self.data
        how = "varr"
        self._mapp(data, how)
        return self


Mechanism = ImprovedMechanism
# Mechanism = OriginalMechanism
# ====================================================================================================================||
"""
	https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
	http://pybem.sourceforge.net/
	http://www.prankster.com/project/index.htm
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

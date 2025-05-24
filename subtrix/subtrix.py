# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid: 03a412f8-c767-467e-9044-ea7cf19c2f9e
	name: Subtrix Module Python Document
	description: >
		Implement subtrix system of document markup and data expansion
		through substitution, functions, loops and variables

		fix dict template input to come out as dict as well

	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
import datetime as dt
import json
from itertools import combinations
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import abspath, dirname, join

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from condor.utils import thingify
from ogma.logma import Logma
# ======================================3rd Party Library Modules=====================================================||
from uuid_extensions import uuid7

# ====================================================================================================================||
here = join(dirname(__file__), "")
log = False
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(abspath(here), "_data_", "subtrix.yaml")  # ||use default configuration


class Mechanism(object):
    """
    class Mechanism:
        A class designed to provide a flexible and configurable mechanism for managing templates, data, rules, and
        configurations.

        The class handles one template with various data configurations to generate one ore more versions of the
        provided template.
    """

    def __init__(self, tmplt=None, data=None, rules=None, cfg=None):
        """
        :param tmplt: A template that can be passed as a string or a dictionary. If a dictionary is provided, it is
        converted into a JSON string.
        :param data: A list to hold data objects. Defaults to an empty list if not provided.
        :param rules: A set of rules or constraints associated with the object. Default is None if not provided.
        :param cfg: Configuration object or dictionary to override default settings. Used to customize the behavior
        of the application or system.
        """
        if tmplt is None:
            tmplt = """"""
        if data is None:
            data = {}
        self.diktlock = 0
        self.term = None
        self.lock = None
        self.input_dict = False
        self.terms_looped = False
        if isinstance(tmplt, dict):
            tmplt = json.dumps(tmplt)
            self.input_dict = True
        self.tmplt = tmplt.strip()
        self.data = data
        self._validate_data()
        self.config = condor.Instruct(pxcfg).override(cfg)
        self.rules = rules
        self.allow_trailing_space = False
        self.allow_trailing_suffix = False
        self.map_processed = False
        self.docs = [self.tmplt]
        self.tmplt_map = {"tmplt": self.tmplt, "docs": self.docs, "map": {}}

    def run(self, full=False, optional=True):  # ||=>Define method
        """
        :param full: a boolean indicating whether to include only a subset of data or the full data. Default is False.
        :param optional: a boolean indicating whether to include optional data. Default is False.
        :return:
            - a list of templates if full is False and optional is False
            - a list of dictionaries if full is False and optional is True
            - the current instance if full is True
        """
        for i in self.config.dikt["sequence"]:  # get the sequence for processing substitution variables
            # select the process runner self.sub, self.func, self.loop, self.matrix, self.varr
            if log:
                logma.info(f"Run Method {i}")
            getattr(self, f"_{i}")()
        #        logma.info(f"Populate Template Docs")
        self._set_templates()
        #       logma.info(f"Process Template Map")
        self._process_map()
        if optional:
            self._remove_optional()  # ||=>Run method
        if full:
            return self
        return json.loads(json.dumps(self.docs[0]).strip()).strip()

    def _assign_template_map(self, start_n, end_n, fix_map, term, code, data, how):
        """"""
        if term not in data.keys():
            load = self._set_map_load(how, code, [], start_n, end_n, fix_map)
            if load not in self.tmplt_map["map"][how]["terms"][term]:
                self.tmplt_map["map"][how]["terms"][term].append(load)
        else:
            if isinstance(data[term], str) or isinstance(data[term], int) or isinstance(data[term], float):
                data[term] = [data[term]]
            if isinstance(data[term], list):
                data_term = data[term]
                load = self._set_map_load(how, code, data_term, start_n, end_n, fix_map)
                if load not in self.tmplt_map["map"][how]["terms"][term]:
                    self.tmplt_map["map"][how]["terms"][term].append(load)
            elif isinstance(data[term], dict):
                for k in data[term].keys():
                    data_term = data[term][k]
                    load = self._set_map_load(how, code, data_term, start_n, end_n, fix_map)
                    if load not in self.tmplt_map["map"][how]["terms"][term]:
                        self.tmplt_map["map"][how]["terms"][term].append(load)
            else:
                raise Exception("Unknown Data")

    def _collect_symbols(self, symcfg):
        """
        :param symcfg: A dictionary containing symbol configurations
        :return: A list of symbols

        This method collects symbols from the given symbol configuration dictionary. It iterates through each key in
        the dictionary and checks if the corresponding value is not None. If the value is not None, it appends the
        symbol value to the `fpats` list. Finally, it returns the `fpats` list containing all the collected symbols.
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
        :param key: The key used to identify a specific configuration or pattern.
        :param cfg: A configuration dictionary containing data such as the start and end patterns to search for.
        :param i: An index to locate the specific sub-pattern within the configuration dictionary.
        :param tmplt: A string template in which the patterns are searched for and processed.
        :return: A tuple containing the starting and ending locations of the identified pattern within the template.
        """
        tmplt = self.tmplt[offset:]
        start_pattern = cfg["base"]["pattern"]["initialize"][i]["symbol"]
        end_pattern = cfg["base"]["pattern"]["finalize"][i]["symbol"]
        start_loc = tmplt.find(start_pattern)
        end_loc = tmplt.find(end_pattern) + len(end_pattern)
        if start_loc == -1 or end_loc == -1:
            self.lock = False
            return start_loc, end_loc, {}, "", ""
        key = tmplt[start_loc:end_loc]
        fix_map = {}
        code = f"{start_pattern}{key}{end_pattern}" if start_pattern not in key else key
        key = code
        fix_symbols = self._collect_symbols(cfg["base"]["pattern"]["processors"])
        if len([x for x in fix_symbols if x in key]) > 0:
            key, fix_map = self._proc_fixes(key, fix_symbols, start_pattern, end_pattern)
        start_loc += offset
        end_loc += offset
        return start_loc, end_loc, fix_map, key, code

    def _init_terms(self, how):
        """"""
        if how not in self.tmplt_map["map"].keys():
            self.tmplt_map["map"][how] = {"terms": {}}
        return self

    def _loop(self, data=None):
        """
        :param data: Data dictionary
        :return: The current instance of the object
        Method to loop through terms in the template and map patterns in the configuration.
        """
        how = "loop"
        if data is None:
            data = self.data
        self._loop_terms()
        self._mapp(data, how)
        return self

    def _loop_terms(self):
        """"""
        if self.terms_looped:
            return self.data
        processors = self.config.dikt["processors"]["loop"]["base"]["pattern"]["initialize"]
        for term in self.data.keys():
            for processor in processors:
                if processor["symbol"] not in term:
                    continue
                looped_terms = []
                if isinstance(self.data.get(term, None), list):
                    for r in range(1, len(self.data[term]) + 1):
                        looped_terms += list(combinations(self.data[term], r))
                else:
                    raise Exception(f"Loop Term is not a list {term}")
                self.data[term] = [[y for y in x] for x in looped_terms]
        self.terms_looped = True
        return self.data

    def _mapp(self, data, how="sub"):  # ||=>Define module
        """
        :param tmplt: The template name. Specifies the template to be processed.
        :param data: The data used for substitution in the template.
        :param spat: The pattern to identify the start of a term in the template. Defaults to '<['.
        :param epat: The pattern to identify the end of a term in the template. Defaults to ']>'.
        :param how: The type of processing to be performed on the template. Defaults to 'sub'.
        :return: The updated object.
        This method processes the given template by performing term substitution based on the provided data. It uses
        the specified start and end patterns to identify terms in the template.
        The processed template is then mapped to the terms in the data and stored in the object's `tmplt_map` attribute.

        """
        self._init_terms(how)
        cfg = self.config.dikt["processors"][how]
        for i, start in enumerate(cfg["base"]["pattern"]["initialize"]):
            phold = 0
            self.lock = True
            while self.lock:
                start_n, end_n, fix_map, term, code = self._find_pattern(cfg, i, phold)
                if term == "":
                    continue
                if term not in self.tmplt_map["map"][how]["terms"].keys():
                    self.tmplt_map["map"][how]["terms"][term] = []
                if how in ("sub",):
                    self._assign_template_map(start_n, end_n, fix_map, term, code, data, how)
                elif how in ("varr",):
                    load = self._set_map_load(how, code, [get_variable_data(term)], start_n, end_n, fix_map)
                    if load not in self.tmplt_map["map"][how]["terms"][term]:
                        self.tmplt_map["map"][how]["terms"][term].append(load)
                elif how in ("loop",):
                    self._assign_template_map(start_n, end_n, fix_map, term, code, data, how)
                else:
                    raise Exception(f"Term Not Mapped {term}")
                phold = end_n
        return self

    def _proc_fixes(self, term, fix_symbols, spat, epat):
        """
        Fixes processors in a given term based on a specified pattern.

        :param term: The term to fix.
        :param spat: The starting pattern of the term. Default is an empty string.
        :param epat: The ending pattern of the term. Default is an empty string.
        :param cfg: The configuration settings. Default is None.
        :return: The updated instance of the class.

        """
        clean_term = term
        fixmap = {}
        fpats, lpat = [spat] + fix_symbols + [epat], spat
        for symbols in [[".:", ":."], [spat, ".:"], [spat, ":."], [spat, epat]]:
            if term.find(symbols[0]) != -1 and term[term.find(symbols[0]) :].find(symbols[1]) != -1:
                clean_term = f"{spat}{term[term.find(symbols[0]) + len(symbols[0]): term.find(symbols[1])]}{epat}"
                # logma.info(f"Clean Term {clean_term}")
                break
        n = 0
        for i in range(len(fpats) - 1):
            fpat, lpat = fpats[i], fpats[i + 1]
            # logma.info(f"Fix Patterns {fpat} {lpat}")
            t = term.find(fpat)
            if t == -1:
                continue
            # logma.info(f"T {t}")
            n = t + len(fpat)
            nl = term.find(lpat)
            # logma.info(f"NL {nl}")
            if nl == -1:
                continue
            fixmap[fpat] = {"final_term": term[n:nl], "pos": [n, nl]}
        return clean_term, fixmap

    def _process_map(self):
        """"""
        if self.map_processed:
            raise Exception()
        docs = []
        cnt = 0
        for d, updated_doc in enumerate(self.docs):
            shift = 0
            sorted_terms = []
            for how in self.tmplt_map["map"].keys():
                for term in self.tmplt_map["map"][how]["terms"].keys():
                    sorted_terms += self.tmplt_map["map"][how]["terms"][term]
            sorted_terms.sort(key=lambda x: x["pos"][0])
            for termmap in sorted_terms:
                if d >= len(termmap["data"]) > 1:
                    d = d % len(termmap["data"])
                # logma.info(f"Data {termmap} D {d}")
                term = termmap["code"]
                x, y = termmap["pos"]
                if term in updated_doc or term in updated_doc:
                    front = updated_doc[: x + shift]
                    if log:
                        logma.info(f"Count {cnt}")
                    if log:
                        logma.info(f"Front {front}")
                    back = updated_doc[y + shift :]
                    if log:
                        logma.info(f"Back {back}")
                    final_term = termmap["code"]
                    # remove optional may need to be placed in here
                    if len(termmap["data"]) > 0:
                        final_term = self._process_final_term(termmap["mods"], termmap["data"][d])
                    shift += len(final_term) - len(termmap["code"])
                    updated_doc = front + final_term + back
                    # if cnt >= 7:
                    #     raise Exception(updated_doc)
                    cnt += 1
            docs.append(updated_doc.strip())
        self.docs = docs
        self.tmplt_map["docs"] = self.docs
        self.map_processed = True
        return self

    def _process_final_term(self, fix_map, terms):
        """"""
        if not isinstance(terms, list):
            terms = [terms]
        final_term = ""
        for term in terms:
            fix_map = dict(sorted(fix_map.items(), key=lambda x: x[1]["pos"][0]))
            if ".:" not in fix_map.keys():
                final_term += str(term)
            for fix in fix_map.keys():
                if fix == ".:":
                    final_term += str(term)
                else:
                    final_term += fix_map[fix]["final_term"]
        # TODO: trim trailing commas I think will go here
        if not self.allow_trailing_space:
            final_term = final_term.strip()
        if not self.allow_trailing_suffix:
            while True:
                if final_term[-1:] in [","]:
                    final_term = final_term[:-1]
                    continue
                else:
                    break
        return final_term

    def _set_map_load(self, how, code, data_term, start_n, end_n, fix_map):
        """"""
        if not isinstance(data_term, list):
            data_term = [data_term]
        load = {
            "code": code,
            "pos": [start_n, end_n],
            "data": data_term,
            "final_term": None,
            "mods": fix_map,
        }
        return load

    def _set_templates(self):
        """"""
        template_cnt = 1
        for how in self.tmplt_map["map"].keys():
            for term in self.tmplt_map["map"][how]["terms"].keys():
                if isinstance(self.tmplt_map["map"][how]["terms"][term][0]["data"], list):
                    template_cnt = template_cnt * len(self.tmplt_map["map"][how]["terms"][term][0]["data"])
                    if log:
                        logma.info(f"Template Count {template_cnt}")
        [self.docs.append(self.tmplt) for i in range(1, template_cnt)]

    def _sub(self, data=None):
        """
        :param data: The data to be processed. If None, it defaults to the instance's `self.data` attribute.
        :return: None. This method executes data mapping and processing with the operation "sub".
        """
        if data is None:
            data = self.data
        how = "sub"
        self._mapp(data, how)
        terms = self.tmplt_map["map"][how]["terms"]
        if list(terms.keys()) == []:
            return self

    def _remove_optional(self):
        """
        Processes and removes optional terms in a template map marked with "<~".

        For entries in the "map" attribute of the `tmplt_map` dictionary, identifies terms that contain
        "<~" (optional terms).
        It clears the "data" field in each associated term map for the identified optional terms.
        Finally, triggers further processing on each 'how' key by passing it to the `_process_map` method.

        :return: Updated instance of the class after processing optional terms.
        """
        for how, terms in self.tmplt_map["map"].items():
            for term, term_maps in terms["terms"].items():
                if "<~" in term:
                    for term_map in term_maps:
                        term_map["data"] = ""
            # self._process_map() - running process map twice creates issues due to offset
        return self

    def _varr(self, data=None):
        """
        Handles the processing of a data map with variable expansion.

        The function retrieves the 'data' attribute, defines the operation type
        as "varr", and applies mapping and variable expansion operations using
        helper methods. Finally, it returns an instance of the current object.

        :return: The current instance after mapping and variable expansion operations.
        """
        if data is None:
            data = self.data
        how = "varr"
        self._mapp(data, how)
        return self

    def _validate_data(self):
        """"""
        for term in self.data.keys():
            if not isinstance(self.data[term], list):
                self.data[term] = [self.data[term]]
        return self


def get_variable_data(term):
    """"""
    cfg = condor.Instruct(join(here, "_data_", "varr.yaml")).load().dikt["knowns"]
    if "<(" in term:
        # found, within = search(cfg, [], [], [term])
        # varobj = found[0]
        varobj = cfg[term]
        if varobj.get("object", None):
            data_function = thingify(varobj["object"])
            if varobj.get("outs", None):
                function_data = getattr(data_function(), varobj["outs"])
            else:
                function_data = data_function()
            data_term = function_data
        elif varobj.get("tmplt", None):
            data_term = varobj["tmplt"]
        else:
            data_term = term
    return data_term


def now():
    """"""
    return dt.datetime.now().strftime("%Y%m%d%H%M%S")


def today():
    """"""
    return dt.date.today().strftime("%Y%m%d")


def uuid(n=None):
    """"""
    uuid_ = str(uuid7())
    if n is None:
        return uuid_
    return uuid_[len(uuid_) - n :]


# ====================================================================================================================||
"""
	https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
	http://pybem.sourceforge.net/
	http://www.prankster.com/project/index.htm
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

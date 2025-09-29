# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: '6705b527-60ca-48a8-9d67-357b22afd1fe'
    name: Subtrix Module Python Testing Document
	description: >
	version: 0.0.0.0.0.0
	authority: filesystem
	security: seclvl2
	<(WT)>: -32
"""
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
import datetime as dt
from copy import deepcopy
from os.path import dirname, join

# ======================================Solutions Brewer Library Modules==============================================||
from condor import condor
from ogma.logma import Logma

from subtrix import subtrix
from subtrix.subtrix import Mechanism

# ======================================3rd Party Library Modules=====================================================||

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
subtrix.log = True
log = subtrix.log
logma = Logma(__name__)

# ====================================================================================================================||
pxcfg = join(here, "_data_", "subtrixTEST.yaml")
cfg = condor.Instruct(pxcfg).load().dikt

test_000 = 1  # --verified - 2025/09/29
test_001 = 1  # --verified - 2025/09/29
test_002 = 1  # --verified - 2025/09/29
test_003 = 1  # --verified - 2025/09/29
test_004 = 1  # --verified - 2025/09/29
test_005 = 1  # --verified - 2025/09/29
test_006 = 1  # --verified - 2025/09/29
test_007 = 0  # --verified - 2025/09/
test_008 = 1  # --verified - 2025/09/29

fixtures = condor.Instruct(join(here, "..", "fixtures", "fixtures.yaml")).load().dikt


class Test_Mechanism:
    """
    This module defines a `Test_Mechanism` class containing test cases for the `Mechanism` class.

    The `Test_Mechanism` class includes setup and teardown methods for initializing
    and cleaning up test resources. It provides multiple test methods to validate
    the functionality of various `Mechanism` methods such as initialization, symbol
    collection, pattern finding, mapping, looping, and other processes.

    The module leverages various fixtures as input data and makes use of assertions
    to validate the expected output. Logging is used to provide information about
    test completion.
    """

    @classmethod
    def setup_class(cls):
        """
        Initializes the class with predefined test mechanisms and other configurations.
        Sets up a mechanism object for each test scenario using template and data provided
        in the respective fixture.

        :return: An instance of the class with all test mechanisms and configurations initialized.
        """
        cls.tipe = "SUBTRIX"
        cls.diktlock = 0
        if test_000:
            cls.fixture000 = deepcopy(fixtures["fixture_000"])
            cls.test_Mechanism_000 = Mechanism(deepcopy(cls.fixture000["tmplt"]), deepcopy(cls.fixture000["data"]))
        if test_001:
            cls.fixture001 = deepcopy(fixtures["fixture_001"])
            cls.test_Mechanism_001 = Mechanism(deepcopy(cls.fixture001["tmplt"]), deepcopy(cls.fixture001["data"]))
        if test_002:
            cls.fixture002 = deepcopy(fixtures["fixture_002"])
            cls.test_Mechanism_002 = Mechanism(deepcopy(cls.fixture002["tmplt"]), deepcopy(cls.fixture002["data"]))
        if test_003:
            cls.fixture003 = deepcopy(fixtures["fixture_003"])
            cls.test_Mechanism_003 = Mechanism(deepcopy(cls.fixture003["tmplt"]), deepcopy(cls.fixture003["data"]))
        if test_004:
            cls.fixture004 = deepcopy(fixtures["fixture_004"])
            cls.test_Mechanism_004 = Mechanism(deepcopy(cls.fixture004["tmplt"]), deepcopy(cls.fixture004["data"]))
        if test_005:
            cls.fixture005 = deepcopy(fixtures["fixture_005"])
            cls.test_Mechanism_005 = Mechanism(deepcopy(cls.fixture005["tmplt"]), deepcopy(cls.fixture005["data"]))
        if test_006:
            cls.fixture006 = deepcopy(fixtures["fixture_006"])
            cls.test_Mechanism_006 = Mechanism(deepcopy(cls.fixture006["tmplt"]), deepcopy(cls.fixture006["data"]))
        if test_007:
            cls.fixture007 = deepcopy(fixtures["fixture_007"])
            cls.test_Mechanism_007 = Mechanism(deepcopy(cls.fixture007["tmplt"]), deepcopy(cls.fixture007["data"]))
        if test_008:
            cls.fixture008 = deepcopy(fixtures["fixture_008"])
            cls.test_Mechanism_008 = Mechanism(deepcopy(cls.fixture008["tmplt"]), deepcopy(cls.fixture008["data"]))
        return cls()

    @classmethod
    def teardown_class(cls):
        """ """

    def reset(self):
        """"""
        if test_000:
            self.fixture000 = deepcopy(fixtures["fixture_000"])
            self.test_Mechanism_000 = Mechanism(deepcopy(self.fixture000["tmplt"]), deepcopy(self.fixture000["data"]))
        if test_001:
            self.fixture001 = deepcopy(fixtures["fixture_001"])
            self.test_Mechanism_001 = Mechanism(deepcopy(self.fixture001["tmplt"]), deepcopy(self.fixture001["data"]))
        if test_002:
            self.fixture002 = deepcopy(fixtures["fixture_002"])
            self.test_Mechanism_002 = Mechanism(deepcopy(self.fixture002["tmplt"]), deepcopy(self.fixture002["data"]))
        if test_003:
            self.fixture003 = deepcopy(fixtures["fixture_003"])
            self.test_Mechanism_003 = Mechanism(deepcopy(self.fixture003["tmplt"]), deepcopy(self.fixture003["data"]))
        if test_004:
            self.fixture004 = deepcopy(fixtures["fixture_004"])
            self.test_Mechanism_004 = Mechanism(deepcopy(self.fixture004["tmplt"]), deepcopy(self.fixture004["data"]))
        if test_005:
            self.fixture005 = deepcopy(fixtures["fixture_005"])
            self.test_Mechanism_005 = Mechanism(deepcopy(self.fixture005["tmplt"]), deepcopy(self.fixture005["data"]))
        if test_006:
            self.fixture006 = deepcopy(fixtures["fixture_006"])
            self.test_Mechanism_006 = Mechanism(deepcopy(self.fixture006["tmplt"]), deepcopy(self.fixture006["data"]))
        if test_007:
            self.fixture007 = deepcopy(fixtures["fixture_007"])
            self.test_Mechanism_007 = Mechanism(deepcopy(self.fixture007["tmplt"]), deepcopy(self.fixture007["data"]))
        if test_008:
            self.fixture008 = deepcopy(fixtures["fixture_008"])
            self.test_Mechanism_008 = Mechanism(deepcopy(self.fixture008["tmplt"]), deepcopy(self.fixture008["data"]))
        return self

    def test_all(self):
        """
        Executes a series of test functions sequentially.

        :return: None
        """
        self.test_init()
        self.test_collect_symbols()
        self.test_find_pattern()
        self.test_mapp()
        self.test_proc_fixes()
        self.test_procss_map()
        self.test_sub()
        self.test_varr()
        self.reset()
        self.test_loop()
        self.test__remove_optional()
        self.reset()
        self.test_run()

    def test_init(self):
        """
        Tests the initialization of the test_Mechanism_000 object.

        :return: None
        """
        if test_000:
            assert self.test_Mechanism_000.tmplt == self.fixture000["tmplt"].strip(), self.test_Mechanism_000.tmplt
            assert self.test_Mechanism_000.diktlock == self.diktlock, self.test_Mechanism_000.diktlock
            logma.info(f"Data {self.fixture000['data']}")
            assert self.test_Mechanism_000.data == self.fixture000["data"], self.test_Mechanism_000.data
        if test_003:
            assert self.test_Mechanism_003.tmplt == self.fixture003["tmplt"].strip(), self.test_Mechanism_003.tmplt
            assert self.test_Mechanism_003.diktlock == self.diktlock, self.test_Mechanism_003.diktlock
            assert self.test_Mechanism_003.data == self.fixture003["data"], self.test_Mechanism_003.data
        if test_006:
            assert self.test_Mechanism_006.tmplt == self.fixture006["tmplt"].strip(), self.test_Mechanism_006.tmplt
            assert self.test_Mechanism_006.diktlock == self.diktlock, self.test_Mechanism_006.diktlock
            assert self.test_Mechanism_006.data == self.fixture006["data"], self.test_Mechanism_006.data
        if test_008:
            assert self.test_Mechanism_008.tmplt == self.fixture008["tmplt"].strip(), self.test_Mechanism_008.tmplt
            assert self.test_Mechanism_008.diktlock == self.diktlock, self.test_Mechanism_008.diktlock
            logma.info(f"Data {self.fixture008['data']}")
            assert self.test_Mechanism_008.data == self.fixture008["data"], self.test_Mechanism_008.data
        logma.info(f"Complete Mechanism Init method Test")

    def test_collect_symbols(self):
        """
        Verifies the `_collect_symbols` method's ability to accurately extract and return pattern symbols from various configuration sections in the `test_Mechanism_000` object's configuration.

        :return: Pass condition of the assertions verifying extracted pattern symbols match the expected results for each configuration section.
        """
        if test_000:
            cfg = self.test_Mechanism_000.config.dikt["processors"]["sub"]["base"]["pattern"]["processors"]
            patterns = self.test_Mechanism_000._collect_symbols(cfg)
            assert patterns == [".:", ":."], patterns
            cfg = self.test_Mechanism_000.config.dikt["processors"]["loop"]["base"]["pattern"]["processors"]
            patterns = self.test_Mechanism_000._collect_symbols(cfg)
            assert patterns == [".:", "->", "<-", "<=>", "<*>", ":."], patterns

            cfg = self.test_Mechanism_000.config.dikt["processors"]["varr"]["base"]["pattern"]["processors"]
            patterns = self.test_Mechanism_000._collect_symbols(cfg)
            assert patterns == [".:", ":."], patterns
        # if test_006:
        #     cfg = self.test_Mechanism_006.config.dikt["processors"]["sub"]["base"]["pattern"]["processors"]
        #     patterns = self.test_Mechanism_006._collect_symbols(cfg)
        #     assert patterns == [".:", ":."], patterns
        #     cfg = self.test_Mechanism_006.config.dikt["processors"]["loop"]["base"]["pattern"]["processors"]
        #     patterns = self.test_Mechanism_006._collect_symbols(cfg)
        #     assert patterns == [".:", "->", "<-", "<=>", "<*>", ":."], patterns
        #
        #     cfg = self.test_Mechanism_000.config.dikt["processors"]["varr"]["base"]["pattern"]["processors"]
        #     patterns = self.test_Mechanism_000._collect_symbols(cfg)
        #     assert patterns == [".:", ":."], patterns
        if test_008:
            cfg = self.test_Mechanism_008.config.dikt["processors"]["sub"]["base"]["pattern"]["processors"]
            patterns = self.test_Mechanism_008._collect_symbols(cfg)
            assert patterns == [".:", ":."], patterns
            cfg = self.test_Mechanism_008.config.dikt["processors"]["loop"]["base"]["pattern"]["processors"]
            patterns = self.test_Mechanism_008._collect_symbols(cfg)
            assert patterns == [".:", "->", "<-", "<=>", "<*>", ":."], patterns
            cfg = self.test_Mechanism_008.config.dikt["processors"]["varr"]["base"]["pattern"]["processors"]
            patterns = self.test_Mechanism_008._collect_symbols(cfg)
            assert patterns == [".:", ":."], patterns
        logma.info(f"Complete Mechanism Collect Symbols method Test")

    def test_find_pattern(self):
        """
        This method tests the correctness of the `_find_pattern` method in a specific mechanism implementation.
        It ensures that the method correctly identifies patterns, start and end locations, fixed mappings,
        and terms within a provided template. The test validates multiple situations using different configurations,
        templates, and mock data.

        :return: None
        """
        if test_000:
            tmplt = "anomdetect.pot<[year]>.ReportingSeriesCode,"
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_000.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_000._find_pattern(cfg, i)
            assert term == "year", term
            assert start_loc == 7, start_loc
            assert end_loc == 15, end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_000.lock is None, self.test_Mechanism_000.lock

            data = self.fixture000["output"]["tmplt_map"]["map"]
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_000.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_000._find_pattern(cfg, i)
            assert term == "year", term
            logma.info(f"{data[how]["terms"][term][0]["pos"][0]}")
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_000.lock is None, self.test_Mechanism_000.lock

            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_000._find_pattern(cfg, i, end_loc)
            assert term == "from", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_000.lock is None, self.test_Mechanism_000.lock
        if test_001:
            data = self.fixture001["output"]["tmplt_map"]["map"]
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_001.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_001._find_pattern(cfg, i)
            assert term == "year", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_001.lock is None, self.test_Mechanism_001.lock

            self.test_Mechanism_001.data = {"<[from]>": "DATA_TABLE"}
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_001._find_pattern(cfg, i, end_loc)
            assert term == "from", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_001.lock is None, self.test_Mechanism_001.lock
            self.test_Mechanism_001.data = {"<[from]>": "DATA_TABLE", "<[year]>": "2015"}
        if test_003:
            tmplt = self.fixture003["tmplt"]
            data = self.fixture003["output"]["tmplt_map"]["map"]
            self.test_Mechanism_003.data = {"<[table]>": "DATA_TABLE"}
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_003._find_pattern(cfg, i, end_loc)
            assert term == "table", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            result = data["sub"]["terms"][term][0]["mods"]
            logma.info(f"Result {result}")
            assert fix_map == result, fix_map
            assert self.test_Mechanism_003.lock is None, self.test_Mechanism_003.lock
        # if test_006:
        #     tmplt = fixture006["tmplt"]
        #     data = fixture006["output"]["tmplt_map"]["map"]
        #     self.test_Mechanism_006.data = {"table": "DATA_TABLE"}
        #     start_loc, end_loc, fix_map, term, code = self.test_Mechanism_006._find_pattern(cfg, i, end_loc)
        #     assert term == "table", term
        #     assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
        #     assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
        #     result = data["sub"]["terms"][term][0]["mods"]
        #     assert fix_map == result, fix_map
        #     assert self.test_Mechanism_006.lock is None, self.test_Mechanism_006.lock
        if test_008:
            tmplt = "anomdetect.pot<[year]>.ReportingSeriesCode,"
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_008.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_008._find_pattern(cfg, i)
            logma.info(f"Fix Map {fix_map}")
            logma.info(f"Code {code}")
            logma.info(f"Term {term}")
            assert term == "year", term
            assert start_loc == 7, start_loc
            assert end_loc == 18, end_loc
            # assert fix_map == {}, fix_map
            assert self.test_Mechanism_008.lock is None, self.test_Mechanism_008.lock
            data = self.fixture008["output"]["tmplt_map"]["map"]
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_008.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_008._find_pattern(cfg, i)
            assert term == "year", term
            logma.info(f"{data[how]["terms"][term][0]["pos"][0]}")
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            # assert fix_map == {}, fix_map
            assert self.test_Mechanism_008.lock is None, self.test_Mechanism_008.lock
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_008._find_pattern(cfg, i, end_loc)
            assert term == "from", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            # assert fix_map == {}, fix_map
            assert self.test_Mechanism_008.lock is None, self.test_Mechanism_008.lock
        logma.info(f"Complete Mechanism Find Pattern method Test")

    def test_loop(self):
        """"""
        if test_002:
            data = self.fixture002["data"]
            self.test_Mechanism_002._loop(data)
            assert len(self.test_Mechanism_002.tmplt_map["docs"]) == 1, len(self.test_Mechanism_002.tmplt_map["docs"])
            result = self.fixture002["output"]["tmplt_map"]["map"]["loop"]
            output = self.test_Mechanism_002.tmplt_map["map"]["loop"]
            for key in output["terms"].keys():
                assert len(output["terms"][key]) == 2, f"{len(output['terms'][key])}\n{output['terms'][key]}"
            assert output == result, output
            result = self.fixture002["output"]["tmplt_map"]["tmplt"]
            assert self.test_Mechanism_002.tmplt.strip() == result.strip(), self.test_Mechanism_002.tmplt
            self.reset()
            logma.info(f"Data {self.fixture002["data"]}")
            assert self.test_Mechanism_002.data == self.fixture002["data"], self.test_Mechanism_002.data
            assert len(self.test_Mechanism_002.docs) == 1, len(self.test_Mechanism_002.docs)
        logma.info(f"Complete Mechanism Loop method Test")

    # def test_loop_terms(self):
    #     """"""
    #     if test_002:
    #         output = self.test_Mechanism_002._loop_terms("controlfield", self.fixture001["data"])
    #         result = {
    #             "controlfield": [
    #                 [
    #                     "p.buddyid",
    #                 ],
    #                 [
    #                     "p.facility_id",
    #                 ],
    #                 ["p.buddyid", "p.facility_id"],
    #             ],
    #             "qp": ["eQP", "QP"],
    #             "year": ["2015", "2016", "2017", "2018"],
    #         }
    #         assert output == result, output

    def test_mapp(self):
        """"""
        if test_000:
            how = "sub"
            self.test_Mechanism_000._mapp(self.fixture000["data"], how)
            assert self.test_Mechanism_000.lock is False, self.test_Mechanism_000.lock
            result = self.fixture000["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_000.tmplt_map["map"][how]
            assert test == result, test

        if test_003:
            how = "sub"
            self.test_Mechanism_003._mapp(self.fixture003["data"], how)
            assert self.test_Mechanism_003.lock is False, self.test_Mechanism_003.lock
            result = self.fixture003["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_003.tmplt_map["map"][how]
            assert test == result, test
        if test_001:
            how = "sub"
            self.test_Mechanism_001._mapp(self.fixture001["data"], how)
            assert self.test_Mechanism_001.lock is False, self.test_Mechanism_001.lock
            result = self.fixture001["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_001.tmplt_map["map"][how]
            logma.info(result)
            assert test == result, test

            how = "varr"
            self.test_Mechanism_001._mapp(self.fixture001["data"], how)
            assert self.test_Mechanism_001.lock is False, self.test_Mechanism_001.lock
            result = self.fixture001["output"]["tmplt_map"]["map"][how]
            result["terms"]["TODAY"][0]["data"] = [dt.datetime.today().strftime("%Y%m%d")]
            test = self.test_Mechanism_001.tmplt_map["map"][how]
            logma.info(result)
            assert test == result, test
        if test_002:
            how = "loop"
            self.test_Mechanism_002._mapp(self.fixture002["data"], how)
            assert self.test_Mechanism_002.lock is False, self.test_Mechanism_002.lock
            result = self.fixture002["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_002.tmplt_map["map"][how]
            logma.info(result)
            assert test == result, test
        if test_008:
            how = "sub"
            self.test_Mechanism_008._mapp(self.fixture008["data"], how)
            assert self.test_Mechanism_008.lock is False, self.test_Mechanism_008.lock
            result = self.fixture008["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_008.tmplt_map["map"][how]
            logma.info(result)
            assert test == result, test
        logma.info(f"Complete Mechanism Mapp method Test")

    def test__process_final_term(self):
        """"""

    def test_proc_fixes(self):
        """"""
        if test_000:
            term = "<[pre.:term:.suf]>"
            spat = "<["
            epat = "]>"
            symbols = [".:", ":."]
            key = "term"
            fix_map = self.test_Mechanism_000._proc_fixes(term, key, symbols, spat, epat)
            result = {
                "<[": {"final_term": "pre", "pos": [2, 5]},
                ".:": {"final_term": "", "pos": [7, 11]},
                ":.": {"final_term": "suf", "pos": [13, 16]},
            }
            assert key == "term", key
            assert fix_map == result, fix_map
        if test_008:
            term = "<[pre.:term]>"
            spat = "<["
            epat = "]>"
            symbols = [".:"]
            key = "term"
            fix_map = self.test_Mechanism_008._proc_fixes(term, key, symbols, spat, epat)
            result = {
                "<[": {"final_term": "pre", "pos": [2, 5]},
                ".:": {"final_term": "", "pos": [7, 11]},
            }
            assert key == "term", key
            assert fix_map == result, fix_map
        logma.info(f"Complete Mechanism Fix Map method Test")

    def test_procss_map(self):
        """"""
        if test_000:
            self.test_Mechanism_000._process_map()
            text = self.fixture000["output"]["text"].strip()
            logma.info(f"Text {text}")
            assert self.test_Mechanism_000.docs[0] == text, self.test_Mechanism_000.docs[0]
        if test_003:
            logma.info(self.test_Mechanism_003.tmplt_map)
            self.test_Mechanism_003._process_map()
            result = self.fixture003["output"]["tmplt_map"]["docs"][0].strip()
            logma.info(result)
            assert self.test_Mechanism_003.docs[0] == result, self.test_Mechanism_003.docs[0]
        logma.info(f"Complete Mechanism Process Map method Test")

    def test_sub(self):
        """"""
        if test_000:
            data = self.fixture000["data"]
            self.test_Mechanism_000._sub(data)
            logma.info(self.fixture000["output"]["tmplt_map"])
            assert (
                self.test_Mechanism_000.tmplt_map == self.fixture000["output"]["tmplt_map"]
            ), self.test_Mechanism_000.tmplt_map
            assert (
                self.test_Mechanism_000.docs[0] == self.fixture000["output"]["text"].strip()
            ), self.test_Mechanism_000.docs[0]
        if test_006:
            data = self.fixture006["data"]
            self.test_Mechanism_006._sub(data)
            logma.info(self.fixture006["output"]["tmplt_map"])
            # assert (
            #     self.test_Mechanism_006.tmplt_map == fixture006["output"]["tmplt_map"]
            # ), self.test_Mechanism_006.tmplt_map
            # assert (
            #     self.test_Mechanism_006.docs[0] == fixture006["output"]["text"].strip()
            # ), self.test_Mechanism_006.docs[0]
        logma.info(f"Complete Mechanism Sub method Test")

    def test__remove_optional(self):
        """"""
        if test_000:
            self.test_Mechanism_000._remove_optional()
        logma.info(f"Complete Mechanism Init method Test")

    def test_run(self):
        """
        Executes the test case `test_Mechanism_000` and verifies if its output matches the expected output stored in `fixture000["output"]`.

        :return: None
        """
        if test_000:
            logma.info(f"Run Test 000")
            result = self.fixture000["output"]["tmplt_map"]
            assert self.test_Mechanism_000.run() == result["docs"][0].strip(), self.test_Mechanism_000.run()
        if test_001:
            logma.info(f"Run Test 001")
            result = self.fixture001["output"]["tmplt_map"]
            result["docs"][0] = result["docs"][0].replace("{today}", dt.datetime.today().strftime("%Y%m%d"))
            logma.info(result["docs"][0])
            assert self.test_Mechanism_001.run() == result["docs"][0].strip(), self.test_Mechanism_001.run()
        if test_005:
            logma.info(f"Run Test 005")
            result = self.fixture005["output"]["tmplt_map"]
            assert self.test_Mechanism_005.run() == result["docs"][0].strip(), self.test_Mechanism_005.run()
        if test_002:
            logma.info(f"Run Test 002")
            result = self.fixture002["output"]["tmplt_map"]
            output = self.test_Mechanism_002.run(True)
            logma.info(len(result["docs"]))
            assert len(output.docs) == len(result["docs"]), len(output.docs)
            logma.info(f"Doc {result['docs'][0].strip()}")
            assert output.docs[0] == result["docs"][0].strip(), output.docs[0]
        if test_004:
            logma.info(f"Run Test 004")
            result = self.fixture004["output"]["tmplt_map"]
            # output = codecs.decode(self.test_Mechanism_004.run().strip('"'), "unicode_escape")
            output = self.test_Mechanism_004.run().strip('"')
            logma.write(output)
            # output_result = codecs.decode(result["docs"][0].strip().strip('"'), "unicode_escape")
            output_result = result["docs"][0].strip().strip('"')
            logma.write(output_result)
            assert output == output_result, output
        if test_005:
            logma.info(f"Run Test 005")
            result = self.fixture005["output"]["tmplt_map"]
            # output = codecs.decode(self.test_Mechanism_004.run().strip('"'), "unicode_escape")
            output = self.test_Mechanism_005.run().strip('"')
            logma.write(output)
            # output_result = codecs.decode(result["docs"][0].strip().strip('"'), "unicode_escape")
            output_result = result["docs"][0].strip().strip('"')
            logma.write(output_result)
            assert output == output_result, output
        if test_006:
            logma.info(f"Run Test 006")
            result = self.fixture006["output"]["tmplt_map"]
            # output = codecs.decode(self.test_Mechanism_004.run().strip('"'), "unicode_escape")
            output = self.test_Mechanism_006.run().strip('"')
            logma.write(output)
            # output_result = codecs.decode(result["docs"][0].strip().strip('"'), "unicode_escape")
            output_result = result["docs"][0].strip().strip('"')
            logma.write(output_result)
            assert output == output_result, output
        if test_007:
            logma.info(f"Run Test 007")
            result = self.fixture007["output"]["tmplt_map"]
            output = self.test_Mechanism_007.run(True)
            logma.info(len(result["docs"]))
            assert len(output.docs) == len(result["docs"]), len(output.docs)
            assert output.docs[0] == result["docs"][0].strip(), output.docs[0]
        if test_008:
            logma.info(f"Run Test 008")
            result = self.fixture008["output"]["tmplt_map"]
            assert self.test_Mechanism_008.run() == result["docs"][0].strip(), self.test_Mechanism_008.run()
        logma.info(f"Complete Mechanism Run method Test")

    def test_varr(self):
        """"""
        if test_001:
            self.test_Mechanism_001._varr(self.fixture001["data"])
            result = self.fixture001["output"]["test_varr"]["tmplt_map"]
            result["map"]["varr"]["terms"]["TODAY"][0]["data"] = [dt.datetime.today().strftime("%Y%m%d")]
            logma.info(result)
            result = result["map"]["varr"]
            assert self.test_Mechanism_001.tmplt_map["map"]["varr"] == result, self.test_Mechanism_001.tmplt_map
        logma.info(f"Complete Mechanism Init method Test")


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
    docid: '6705b527-60ca-48a8-9d67-357b22afd1fe'
    name: Subtrix Module Python Testing Document
    description: >
    expiry: <[expiration]>
    version: <[version]>
    outline: <[outline]>
    authority: document|this
    security: sec|lvl2
    <(WT)>: -32
"""
import datetime as dt
# -*- coding: utf-8 -*-
# ===============================================================================||
from os.path import dirname, join

import crow

crow.crowLoad("Subtrix", "DELTA")
from condor import condor
from subtrix.subtrix import Mechanism
from subtrix import subtrix
from ogma.logma import Logma

# ========================Common Globals=========================================||
here = join(dirname(__file__), "")  # ||
subtrix.log = True
log = subtrix.log
logma = Logma(__name__)

# ===============================================================================||
pxcfg = join(here, "_data_", "subtrixTEST.yaml")
cfg = condor.Instruct(pxcfg).load().dikt

test_000 = False
test_001 = False
test_002 = True
test_003 = False
test_004 = False
test_005 = False

fixtures = condor.Instruct(join(here, "..", "fixtures", "fixtures.yaml")).load().dikt
fixture000 = fixtures["fixture_000"]
fixture001 = fixtures["fixture_001"]
fixture002 = fixtures["fixture_002"]
fixture003 = fixtures["fixture_003"]
fixture004 = fixtures["fixture_004"]
fixture005 = fixtures["fixture_005"]


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
            cls.test_Mechanism_000 = Mechanism(fixture000["tmplt"], fixture000["data"])
        if test_001:
            cls.test_Mechanism_001 = Mechanism(fixture001["tmplt"], fixture001["data"])
        if test_002:
            cls.test_Mechanism_002 = Mechanism(fixture002["tmplt"], fixture002["data"])
        if test_003:
            cls.test_Mechanism_003 = Mechanism(fixture003["tmplt"], fixture003["data"])
        if test_004:
            cls.test_Mechanism_004 = Mechanism(fixture004["tmplt"], fixture004["data"])
        if test_005:
            cls.test_Mechanism_005 = Mechanism(fixture005["tmplt"], fixture005["data"])
        return cls()

    @classmethod
    def teardown_class(cls):
        """ """

    def test_all(self):
        """
        Executes a series of test functions sequentially.

        :return: None
        """
        self.test_init()
        # self.test_collect_symbols()
        # self.test_find_pattern()
        # self.test_loop_terms()
        # self.test_mapp()
        # self.test_proc_fixes()
        # self.test_procss_map()
        # self.test_sub()
        # self.test_varr()
        # self.test_loop()
        # self.test_rmvOptional()
        self.test_run()

    def test_init(self):
        """
        Tests the initialization of the test_Mechanism_000 object.

        :return: None
        """
        if test_000:
            assert self.test_Mechanism_000.tmplt == fixture000["tmplt"].strip(), self.test_Mechanism_000.tmplt
            assert self.test_Mechanism_000.diktlock == self.diktlock, self.test_Mechanism_000.diktlock
            assert self.test_Mechanism_000.data == fixture000["data"], self.test_Mechanism_000.data
        if test_003:
            assert self.test_Mechanism_003.tmplt == fixture003["tmplt"].strip(), self.test_Mechanism_003.tmplt
            assert self.test_Mechanism_003.diktlock == self.diktlock, self.test_Mechanism_003.diktlock
            assert self.test_Mechanism_003.data == fixture003["data"], self.test_Mechanism_003.data
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
            assert term == "<[year]>", term
            assert start_loc == 7, start_loc
            assert end_loc == 15, end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_000.lock is None, self.test_Mechanism_000.lock

            data = fixture000["output"]["tmplt_map"]["map"]
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_000.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_000._find_pattern(cfg, i)
            assert term == "<[year]>", term
            logma.info(f"{data[how]["terms"][term][0]["pos"][0]}")
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_000.lock is None, self.test_Mechanism_000.lock

            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_000._find_pattern(cfg, i, end_loc)
            assert term == "<[from]>", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_000.lock is None, self.test_Mechanism_000.lock
        if test_001:
            data = fixture001["output"]["tmplt_map"]["map"]
            i = 0
            how = "sub"
            cfg = self.test_Mechanism_001.config.dikt["processors"][how]
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_001._find_pattern(cfg, i)
            assert term == "<[year]>", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_001.lock is None, self.test_Mechanism_001.lock

            self.test_Mechanism_001.data = {"<[from]>": "DATA_TABLE"}
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_001._find_pattern(cfg, i, end_loc)
            assert term == "<[from]>", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            assert fix_map == {}, fix_map
            assert self.test_Mechanism_001.lock is None, self.test_Mechanism_001.lock
            self.test_Mechanism_001.data = {"<[from]>": "DATA_TABLE", "<[year]>": "2015"}

        if test_003:
            tmplt = fixture003["tmplt"]
            data = fixture003["output"]["tmplt_map"]["map"]
            self.test_Mechanism_003.data = {"<[table]>": "DATA_TABLE"}
            start_loc, end_loc, fix_map, term, code = self.test_Mechanism_003._find_pattern(cfg, i, end_loc)
            assert term == "<[table]>", term
            assert start_loc == data[how]["terms"][term][0]["pos"][0], start_loc
            assert end_loc == data[how]["terms"][term][0]["pos"][1], end_loc
            result = data["sub"]["terms"][term][0]["mods"]
            assert fix_map == result, fix_map
            assert self.test_Mechanism_003.lock is None, self.test_Mechanism_003.lock

        logma.info(f"Complete Mechanism Find Pattern method Test")

    def test_loop(self):
        """"""
        if test_002:
            data = fixture002["data"]
            self.test_Mechanism_002._loop(data)
            assert len(self.test_Mechanism_002.tmplt_map["docs"]) == 1, len(self.test_Mechanism_002.tmplt_map["docs"])
            result = fixture002["output"]["tmplt_map"]["map"]["loop"]
            output = self.test_Mechanism_002.tmplt_map["map"]["loop"]
            for key in output["terms"].keys():
                assert len(output["terms"][key]) == 2, f"{len(output['terms'][key])}\n{output['terms'][key]}"
            assert output == result, output
            result = fixture002["output"]["tmplt_map"]["tmplt"]
            assert self.test_Mechanism_002.tmplt.strip() == result.strip(), self.test_Mechanism_002.tmplt
            assert self.test_Mechanism_002.data == fixture002["data"], self.test_Mechanism_002.data
            assert len(self.test_Mechanism_002.docs) == 1, len(self.test_Mechanism_002.docs)
        logma.info(f"Complete Mechanism Loop method Test")

    def test_loop_terms(self):
        """"""
        if test_002:
            output = self.test_Mechanism_002._loop_terms()
            result = {
                "<@[controlfield]@>": [
                    [
                        "p.buddyid",
                    ],
                    [
                        "p.facility_id",
                    ],
                    ["p.buddyid", "p.facility_id"],
                ],
                "<[qp]>": ["eQP", "QP"],
                "<[year]>": ["2015", "2016", "2017", "2018"],
            }
            assert output == result, output

    def test_mapp(self):
        """"""
        if test_000:
            how = "sub"
            self.test_Mechanism_000._mapp(fixture000["data"], how)
            assert self.test_Mechanism_000.lock is False, self.test_Mechanism_000.lock
            result = fixture000["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_000.tmplt_map["map"][how]
            assert test == result, test

        if test_003:
            how = "sub"
            self.test_Mechanism_003._mapp(fixture003["data"], how)
            assert self.test_Mechanism_003.lock is False, self.test_Mechanism_003.lock
            result = fixture003["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_003.tmplt_map["map"][how]
            assert test == result, test
        if test_001:
            how = "sub"
            self.test_Mechanism_001._mapp(fixture001["data"], how)
            assert self.test_Mechanism_001.lock is False, self.test_Mechanism_001.lock
            result = fixture001["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_001.tmplt_map["map"][how]
            logma.info(result)
            assert test == result, test

            how = "varr"
            self.test_Mechanism_001._mapp(fixture001["data"], how)
            assert self.test_Mechanism_001.lock is False, self.test_Mechanism_001.lock
            result = fixture001["output"]["tmplt_map"]["map"][how]
            result["terms"]["<(TODAY)>"][0]["data"] = [dt.datetime.today().strftime("%Y%m%d")]
            test = self.test_Mechanism_001.tmplt_map["map"][how]
            logma.info(result)
            assert test == result, test
        if test_002:
            how = "loop"
            self.test_Mechanism_002._mapp(fixture002["data"], how)
            assert self.test_Mechanism_002.lock is False, self.test_Mechanism_002.lock
            result = fixture002["output"]["tmplt_map"]["map"][how]
            test = self.test_Mechanism_002.tmplt_map["map"][how]
            assert test == result, test
        logma.info(f"Complete Mechanism Mapp method Test")

    def test_proc_fixes(self):
        """"""
        if test_000:
            term = "<[pre.:term:.suf]>"
            spat = "<["
            epat = "]>"
            symbols = [".:", ":."]
            key, fix_map = self.test_Mechanism_000._proc_fixes(term, symbols, spat, epat)
            result = {
                "<[": {"final_term": "pre", "pos": [2, 5]},
                ".:": {"final_term": "term", "pos": [7, 11]},
                ":.": {"final_term": "suf", "pos": [13, 16]},
            }
            assert key == "<[term]>", key
            assert fix_map == result, fix_map
        logma.info(f"Complete Mechanism Fix Map method Test")

    def test_procss_map(self):
        """"""
        if test_000:
            self.test_Mechanism_000._process_map()
            text = fixture000["output"]["text"].strip()
            assert self.test_Mechanism_000.docs[0] == text, self.test_Mechanism_000.docs[0]
        if test_003:
            logma.info(self.test_Mechanism_003.tmplt_map)
            self.test_Mechanism_003._process_map()
            result = fixture003["output"]["tmplt_map"]["docs"][0].strip()
            logma.info(result)
            assert self.test_Mechanism_003.docs[0] == result, self.test_Mechanism_003.docs[0]
        logma.info(f"Complete Mechanism Process Map method Test")

    def test_sub(self):
        """"""
        if test_000:
            data = fixture000["data"]
            self.test_Mechanism_000._sub(data)
            logma.info(fixture000["output"]["tmplt_map"])
            assert (
                self.test_Mechanism_000.tmplt_map == fixture000["output"]["tmplt_map"]
            ), self.test_Mechanism_000.tmplt_map
            assert (
                self.test_Mechanism_000.docs[0] == fixture000["output"]["text"].strip()
            ), self.test_Mechanism_000.docs[0]
        logma.info(f"Complete Mechanism Sub method Test")

    def test_rmvOptional(self):
        """"""
        if test_000:
            self.test_Mechanism_000.rmvOptional()
        logma.info(f"Complete Mechanism Init method Test")

    def test_run(self):
        """
        Executes the test case `test_Mechanism_000` and verifies if its output matches the expected output stored in `fixture000["output"]`.

        :return: None
        """
        if test_000:
            logma.info(f"Run Test 000")
            result = fixture000["output"]["tmplt_map"]
            assert self.test_Mechanism_000.run() == result["docs"][0].strip(), self.test_Mechanism_000.run()
        if test_001:
            logma.info(f"Run Test 001")
            result = fixture001["output"]["tmplt_map"]
            result["docs"][0] = result["docs"][0].replace("{today}", dt.datetime.today().strftime("%Y%m%d"))
            logma.info(result["docs"][0])
            assert self.test_Mechanism_001.run() == result["docs"][0].strip(), self.test_Mechanism_001.run()
        if test_005:
            logma.info(f"Run Test 005")
            result = fixture005["output"]["tmplt_map"]
            assert self.test_Mechanism_005.run() == result["docs"][0].strip(), self.test_Mechanism_005.run()
        if test_002:
            logma.info(f"Run Test 002")
            result = fixture002["output"]["tmplt_map"]
            output = self.test_Mechanism_002.run(True)
            logma.info(len(result["docs"]))
            assert len(output.docs) == len(result["docs"]), len(output.docs)
            assert output.docs[0] == result["docs"][0].strip(), output.docs[0]
        if test_004:
            logma.info(f"Run Test 004")
            result = fixture004["output"]["tmplt_map"]
            output = self.test_Mechanism_004.run()
            assert output == result["docs"][0].strip(), output
        logma.info(f"Complete Mechanism Run method Test")

    def test_varr(self):
        """"""
        if test_001:
            self.test_Mechanism_001._varr(fixture001["data"])
            result = fixture001["output"]["test_varr"]["tmplt_map"]
            result["map"]["varr"]["terms"]["<(TODAY)>"][0]["data"] = [dt.datetime.today().strftime("%Y%m%d")]
            logma.info(result)
            result = result["map"]["varr"]
            assert self.test_Mechanism_001.tmplt_map["map"]["varr"] == result, self.test_Mechanism_001.tmplt_map
        logma.info(f"Complete Mechanism Init method Test")

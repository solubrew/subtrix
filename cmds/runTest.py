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

import datetime as dt

# -*- coding: utf-8 -*-
# -*- coding: utf-8 -*
# ======================================Standard Library Modules======================================================||
from os.path import dirname, join
from sys import argv

# ======================================Solutions Brewer Library Modules==============================================||
import crow

# ======================================3rd Party Library Modules=====================================================||

crow.crowLoad("Subtrix", "DELTA")
from ogma.logma import Logma
from test_subtrix.subtrix.subtrixTEST import Test_ImprovedMechanism

# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
logma = Logma(__name__)
log = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")


def run(args):
    """Run individual tabs with mock data for development purposes"""
    if args[1] == "class" or args[1] == "all":
        test = Test_ImprovedMechanism.setup_class()
        test.test_all()
        test.teardown_class()

    # if args[1] == "examples" or args[1] == "all":
    #     test_functionSubstition()
    #     test_incrementSubstition()
    #     test_loopingSubstitution()
    #     test_matrixSubstition()
    #     test_prefixSubstitution()
    #     test_simpleSubstitution()
    #     test_suffixSubstitution()
    #     test_variableSubstition()


if __name__ == "__main__":
    start = dt.datetime.now()
    logma.info(f"Start {start}")
    run(argv)
    end = dt.datetime.now()
    logma.info(f"Start {start}")
    logma.info(f"End {end}")
    logma.info(f"End Duration {end - start}")

# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

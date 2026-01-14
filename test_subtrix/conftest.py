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
import crow

crow.crowLoad("Subtrix", "DELTA")
from os.path import dirname, join

# ======================================3rd Party Library Modules=====================================================||

# ======================================Solutions Brewer Library Modules==============================================||


# ====================================================================================================================||
here = join(dirname(__file__), "")  # ||
log = True

# ====================================================================================================================||
pxcfg = join(here, "_data_", ".yaml")

# pytest_plugins = [
#     "test_subtrix.fixtures.my_fixture_file",
# ]


def pytest_sessionstart(session):
    """"""
    print("\n[BOOT] Initializing Crow environment for recursive imports...")
    crow.crowLoad("Subtrix", "DELTA")


def pytest_configure(config):
    """
    Allows plugins and conftest files to perform initial configuration.
    This hook is called for every test session.
    """
    pass


# ====================================================================================================================||

# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

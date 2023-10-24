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
# -*- coding: utf-8 -*-
# ===============================================================================||
from os.path import abspath, dirname, join

import Pytest

# ===============================================================================||

# ========================Common Globals=========================================||
here = join(dirname(__file__), '')  # ||
there = abspath(join('../../..'))  # ||set path at pheonix level
version = '0.0.0.0.0.0'  # ||
log = False
# ===============================================================================||
pxcfg = f'{here}/_data_/t_subtrix.yaml'


@Pytest.fixture
def template_fixture():
	"""

	:return:
	"""


def fixture_000():
	""" """
	fixture_cfg = cfg['fixture_000']
	data = fixture_cfg['data']
	tmplt = fixture_cfg['tmplt']
	output = fixture_cfg['output']

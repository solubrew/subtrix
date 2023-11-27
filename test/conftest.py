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

# ===============================================================================||
import pytest
# ===============================================================================||
from condor import condor

# ========================Common Globals=========================================||
here = join(dirname(__file__), '')  # ||
there = abspath(join('../../..'))  # ||
version = '0.0.0.0.0.0'  # ||
log = False
# ===============================================================================||
pxcfg = join(here, '_data_', 'fixtures.yaml')


@pytest.fixture
class SubtrixFixture(object):
	"""
	:return:
	"""
	
	def __init__(self, name):
		"""

		:param name:
		"""
		self.config = condor.condor.instruct(pxcfg).load().dikt
		self.data = self.config[name]['data']
		self.tmplt = self.config[name]['tmplt']
		self.output = self.config[name]['output']


class ThingFixture(object):
	"""

	"""
	
	def __init__(self, name):
		"""

		:param name:
		"""
	
	def WhatFixture(self):
		"""

		:return:
		"""

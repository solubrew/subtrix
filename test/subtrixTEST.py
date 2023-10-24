#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
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

from subtrix import Mechanism

# ===============================================================================||
#========================Common Globals=========================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = f'{here}/_data_/t_subtrix.yaml'


class Test_Mechanism(unittest.TestCase):
	"""

	"""

	@classmethod
	def setup_class(cls):
		""" """
		cls.tmplts = []
		cls.data = []
		cls.tipe = []
		cls.test_Mechanism = Mechanism(cls.tmplts, cls.data)

	@classmethod
	def teardown_class(cls):
		"""
		"""

	def test_All(self):

	def test_init(self):
		"""

		:return:
		"""
		assert hasattr(self, 'spat')
		assert self.tmplts == self.test_Mechanism.tmplts
		assert self.data == self.test_Mechanism.data
		assert self.tipe == self.test_Mechanism.tipe

	def test_run(self):
		"""

		:return:
		"""
		self.test_Mechanism.run(fixture000)
		assert self.

	def functionSubstition(self):
		''' '''
		input = cfg['functionSubstition']['input']
		output = cfg['functionSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def incrementSubstition(self):
		''' '''
		input = cfg['simpleSubstition']['input']
		output = cfg['simpleSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def loopingSubstitution(self):
		''' '''
		input = cfg['loopingSubstition']['input']
		output = cfg['loopingSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def matrixSubstition(self):
		''' '''
		input = cfg['matrixSubstition']['input']
		output = cfg['matrixSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def prefixSubstitution(self):
		''' '''
		input = cfg['simpleSubstition']['input']
		output = cfg['simpleSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def simpleSubstitution(self):
		''' '''
		input = cfg['simpleSubstition']['input']
		output = cfg['simpleSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def suffixSubstitution(self):
		''' '''
		input = cfg['simpleSubstition']['input']
		output = cfg['simpleSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

	def variableSubstition(self):
		''' '''
		input = cfg['variableSubstition']['input']
		output = cfg['variableSubstition']['output']
		assert output = subtrix(*input['args'], **input['kwargs'])

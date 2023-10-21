#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: '6705b527-60ca-48a8-9d67-357b22afd1fe'
	name: Subtrix Module Python Testing Document
	description: >
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/subtrix/subtrix.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
#===============================================================================||
#========================Common Globals=========================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = f'{here}/_data_/t_subtrix.yaml'
cfg = condor.instruct(pxcfg).load().dikt
def functionSubstition():
	''' '''
	input = cfg['functionSubstition']['input']
	output = cfg['functionSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def incrementSubstition():
	''' '''
	input = cfg['simpleSubstition']['input']
	output = cfg['simpleSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def loopingSubstitution():
	''' '''
	input = cfg['loopingSubstition']['input']
	output = cfg['loopingSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def matrixSubstition():
	''' '''
	input = cfg['matrixSubstition']['input']
	output = cfg['matrixSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def prefixSubstitution():
	''' '''
	input = cfg['simpleSubstition']['input']
	output = cfg['simpleSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def simpleSubstitution():
	''' '''
	input = cfg['simpleSubstition']['input']
	output = cfg['simpleSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def suffixSubstitution():
	''' '''
	input = cfg['simpleSubstition']['input']
	output = cfg['simpleSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

def variableSubstition():
	''' '''
	input = cfg['variableSubstition']['input']
	output = cfg['variableSubstition']['output']
	assert output = subtrix(*input['args'], **input['kwargs'])

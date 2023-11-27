# @@@@@@@@@@@@@@@@@@@Config.Config@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid:
	name: Module Python Document
	description: >
	expirary: <[expiration]>
	version: '0.0.0.0.0.0'
	authority: document|this
	security: seclvl2
	<(WT)>: -32
"""
import traceback
from importlib import import_module
# -*- coding: utf-8 -*-
# ===============================================================================||
from os.path import abspath, dirname, expanduser, exists, join

# ===============================================================================||
from subtrix.thing import What

# ========================Common Globals=========================================||
here = join(dirname(__file__), '')
home = expanduser('~')
log = True
# ===============================================================================||
pxcfg = join(abspath(here), '_data_', 'config.yaml')  # use default configuration


def funcify(thing):
	""" """
	method_name = thing  # set by the command line options
	possibles = globals().copy()
	possibles.update(locals())
	method = possibles.get(method_name)
	if not method:
		raise NotImplementedError("Method %s not implemented" % method_name)
	return method


def includify(thing):
	""" """
	text = What(thing).get().text
	# if log: print('TEXT', text)
	fnl = thing.rfind('/')  # ||
	base_path = thing[:fnl + 1]  # ||
	startpt, depth, fstart, fend = 0, 0, '<(INCL)>', '.yaml'  # ||
	while True:  # ||
		fspl = text[startpt:].find(fstart) + startpt  # ||
		linepos = text[:fspl].rfind('\n')  # ||
		depth = text[linepos:fspl].find('  ')  # ||
		if depth == -1:  # ||
			depth = 0  # ||
		depth += 1  # ||
		if fspl == startpt - 1:  # ||
			break  # ||
		fspl = fspl  # ||
		fepl = text[fspl:].find(fend) + fspl + len(fend)  # ||
		pattern = text[fspl:fepl]  # ||
		# if pattern == '':  # ||
		# 	startpt = fepl + len(ntext) - len(pattern)  # ||
		# 	continue  # ||
		path = pattern.replace(fstart, '')  # ||
		# if log: print('Pattern', path, 'basepath', base_path)
		path = join(abspath(base_path), path)
		# if log: print('Pattern', path, 'basepath', base_path)
		if exists(path):  # ||
			# print('Path Exists', path)
			ntext = What(path).get().text.replace('---', ' ').replace('\n', '\n' + '  ' * depth)  # ||
		# print('NTEXT', '\n', ntext)
		else:  # ||
			ntext = path  # ||
		depth = '\n' + '  ' * depth  # ||
		text = f'{text[:fspl]}{depth}{ntext}{text[fepl:]}'  # ||
		startpt = fepl + len(ntext) - len(path)  # ||
		path = ''  # ||
	print('Text', text)
	dikt = What(text).get().dikt
	print('DIKT', dikt)
	return dikt


def modulize(thing):
	"""Import dotted path text and return the attribute/class"""
	if '.' in thing:
		try:
			module_path, class_name = thing.rsplit('.', 1)
		except Exception as e:
			print(e, 'Config.Modulize', thing)
	module = import_module(module_path)
	try:
		obj = getattr(module, class_name)
	except AttributeError as e:
		print('config modulize', e)
		traceback.print_exc()
		raise e
	return obj


def thingify(thing, module=None, path=None, test=False):
	"""Import dotted path text and return the attribute/class"""
	if log: print(f'Thing {thing}')
	if test:
		if module == None:
			module_path, thing = thing.rsplit('.', 1)
			module = import_module(module_path)
		obj = getattr(module, thing)
		return obj
	else:
		if module == None:
			try:
				module_path, thing = thing.rsplit('.', 1)
				module = import_module(module_path)
			except Exception as e:
				print(f'Thingify Module Path {thing} Failed {e}')
				if path: print('From this Path', path)
				traceback.print_exc()
				raise e
		# return None
		try:
			obj = getattr(module, thing)
		except AttributeError as e:
			print('Thingification Failed due to ', e)
			traceback.print_exc()
			raise e
		return obj


# ==============================Source Materials=================================||
"""

"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

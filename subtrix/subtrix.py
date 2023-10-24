# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
"""
---
<(META)>:
	docid: 03a412f8-c767-467e-9044-ea7cf19c2f9e
	name: Subtrix Module Python Document
	description: >
		Implement subtrix system of document markup and data expansion
		through substitution, functions, loops and variables

		fix dict template input to come out as dict as well

	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>subtrix/subtrix.py
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
"""
import json  # ||
# -*- coding: utf-8 -*-
# ===============================================================================||
from os.path import abspath, dirname, join

# ===============================================================================||
from subtrix import thing, thingifier

# ========================Common Globals=========================================||
here = join(dirname(__file__), '')  # ||
there = abspath(join('../../..'))  # ||set path at pheonix level
version = '0.0.0.0.0.0'  # ||
log = False
# ===============================================================================||
pxcfg = join(abspath(here), '_data_/subtrix.yaml')  # ||use default configuration


class Mechanism(object):  # ||
	"""
	Perform replacement in templates from given data
	Substitution is performed in various ways based on the coding system of various methods

	Prexfix: :.term
	Suffix: term.:

	Varr: A set of predefined known variables that can be set globablly
		codes: <(: standard, <^(: template update, <~(: optional, <o(: stop override

	Sub: A simple string replacement with both prefix and suffix
		codes: <[: standard, <^[: template update, <~[: optional, <o[: stop override

	Matrix:
		codes: <#[: Matrix Substitution, <#{: Matrix Functions

	Loop:
		codes: <@[: Loop Substitution, <@{: Loop Function

	Func:
		codes: <{: standard, <^{: template update, <~{: optional, <o{: stop override

	"""
	version = '0.0.0.0.0.0'  # ||=>Set version

	def __init__(self, tmplts=[], data={}, rules=None, cfg=None):  # ||
		self.spat = None
		self.tmplts, self.diktlock = tmplts, 0
		if isinstance(tmplts, str):  # ||
			tmplts = [tmplts, ]  # ||
		elif isinstance(tmplts, dict):  # ||
			tmplts = [json.dumps(tmplts)]  # ||
			self.diktlock = 1
		self.data = data  # ||
		if cfg != None:  # ||
			config = thing.What().get(cfg).dikt  # ||
		self.config = thing.What().get(pxcfg).dikt  # ||load configuration file
		if rules != None:  # ||
			cfg = join(abspath(here), '_data_')  # ||set folder path
		# rules = next(store.stuff(cfg).read())#								||read files in directory
		self.tmpltmap = {'tmplts': tmplts, 'docs': tmplts}  # ||set vars
		self.tipe = self.config['system']['name']  # ||

	# @classmethod  # ||
	# def from_stream(cls, data):  # ||=>alt class input  unsure why this is in subtrix
	# 	"""Group data from a stream...turn a stream into frames"""  # ||=>describe method
	# 	data = pd.DataFrame(data)  # ||set data into frame
	# 	return cls(data)  # ||

	def findPattern(self, spat, epat, tmplt, inclusive=True):  # ||=>Define module
		"""check text for patterns"""  # ||=>Describe module
		self.lock, self.term = False, ''  # ||Set the cycle lock to open
		snum = tmplt.find(spat)  # ||find start pattern
		enum = snum + tmplt[snum:].find(epat) + len(epat)  # ||find end patter after start
		if snum > enum:  # ||
			if log: print('rule.findPattern Failed')  # ||
		if snum != -1 and enum != -1:  # ||chk both patterns found
			self.term = tmplt[snum:enum]  # ||clip term from template code
			if spat in tmplt[enum:]:  # ||verify the need to keep working
				self.lock = True  # ||Set the cycle lock to closed
		return snum, enum  # ||

	def func(self, tmplt, j, data, cfg={}):  # ||
		"""process all functions"""  # ||
		self.mapPattern(cfg, tmplt, data, 'func')  # ||map patterns in config
		terms = self.tmpltmap[j]['func']['terms']  # ||
		if len(terms.keys()) == 0:  # ||
			return self  # ||
		for i in range(len(terms.keys())):  # ||cycle terms
			term, sterm = list(terms.keys())[i], ''  # ||
			termmap = terms[term]  # ||map of each term
			try:  # ||
				found, within = search(cfg, [], [], [term])
				varobj = found[0]
			except Exception as e:  # ||
				break  # ||
			fdata = thingifier.modulize(varobj['object'])  # ||This is leveraging condors functionality to turn text into functions and then pull
			# the attributes of that function into the data for mapping
			fdata = getattr(fdata(), varobj['outs'])  # ||
			for l in range(len(termmap)):  # ||
				k = termmap[l]  # ||
				sdata = {term: fdata}  # ||
				ksub = {'sub': {'terms': {term: [k]}}}  # ||
				self.tmpltmap[j] = ksub  # ||
				self.sub(tmplt, j, sdata, cfg)  # ||
				self.tmpltmap['docs'].insert(0, tmplt)  # ||
			self.tmpltmap['docs'].pop(0)  # ||
			self.tmpltmap[i]['sub']['terms'][term][l]['data'] = fdata  # ||
		return self  # ||

	def getDterm(self, data, cterm, scode, sterm):  # ||
		'Get term from data'  # ||
		dterm = ''  # ||
		if isinstance(data, dict):  # ||
			if sterm in data.keys():  # ||substitution term
				dterm = data[sterm]  # ||
			elif scode in data.keys():  # ||
				dterm = data[scode]  # ||substitution code
			else:  # ||
				dterm = ''  # ||
		elif isinstance(data, list):  # ||
			dterm = data[cterm]  # ||count term
		return dterm  # ||

	def getFterm(self, fmap, dterm, spat, how='sub'):  # ||
		fterm = ''  # ||
		if spat in fmap.keys():  # ||
			fterm += str(fmap[spat]['fterm'])  # ||
		fterm += str(dterm)  # ||
		if ':.' in fmap.keys():  # ||
			fterm += str(fmap['.:']['fterm'])  # ||
		return fterm  # ||

	def loop(self, tmplt, j, data, cfg={}):  # ||
		'Load loop data and combine with tmplt data'  # ||
		self.mapPattern(cfg, tmplt, data, 'loop')  # ||map patterns in config
		terms = self.tmpltmap[j]['loop']['terms']  # ||
		if list(terms.keys()) == []:  # ||
			return self  # ||
		ndata, shift, lterm = {}, 0, ''  # ||
		for term in terms.keys():  # ||
			if lterm == term:
				continue
			termmap = terms[term]  # ||map of each term
			for i in range(len(terms[term])):  # ||
				code = terms[term][i]['code']  # ||
				ndata = ''  # ||
				ldata = len(terms[term][i]['data'])  # ||
				lock = 0  # ||
				if ldata == 0:
					continue
				for d in range(ldata):  # ||
					lmod = len(terms[term][i]['mods'].keys())  # ||
					for l in range(lmod):  # ||
						mod = list(terms[term][i]['mods'].keys())[l]  # ||
						r = str(terms[term][i]['mods'][mod]['fterm'])  # ||
						if r in term:  # ||
							ndata += terms[term][i]['data'][d]  # ||
						else:  # ||
							if lock != 0:  # ||
								ndata += r  # ||
						lock = 1  # ||
				self.sub(tmplt, j, {term: ndata[:-len(r)]}, cfg)  # ||
				break  # this is a hack that should come out with better handling
			# of multi loop templates
			lterm = term
			tmplt = self.tmpltmap['docs'][j]  # ||
		return self  # ||

	def mapp(self, tmplt, data, spat='<[', epat=']>', how='sub'):  # ||=>Define module
		"""Create Dictionary of all rule mechanisms in given document"""  # ||
		self.spat, self.epat = spat, epat  # ||set bookend patterns
		self.lock, self.fixmap, cterm = True, {}, 0  # ||set variables
		tmpltDEX = self.tmpltmap['docs'].index(tmplt)  # ||
		ntmplt, pl, tterms = tmplt, 0, {}  # ||
		while self.lock:  # ||lock until all patterns are removed
			snum, enum = self.findPattern(spat, epat, ntmplt)  # ||find the next term
			if self.term != '':  # ||
				self.fixmap = {}  # ||prefix,suffix map
				self.procFix(self.term, spat, epat)  # ||call prefix/suffix processer
				if ':.' in self.fixmap.keys():  # ||
					sterm = self.fixmap[':.']['fterm']  # ||
				else:  # ||
					sterm = self.fixmap['.:']['fterm']  # ||
				cterm += 1  # ||
				scode = spat + sterm + epat  # ||
				dterm = self.getDterm(data, cterm, scode, sterm)  # ||
				fterm = self.getFterm(self.fixmap, dterm, spat, epat)  # ||
				if scode not in tterms.keys():  # ||
					tterms[scode] = []  # ||
				load = {'code': self.term, 'pos': [pl + snum, pl + enum],
						'data': dterm, 'fterm': fterm, 'mods': self.fixmap}  # ||
				tterms[scode].append(load)  # ||
				pl += enum  # ||
				ntmplt = ntmplt[enum:]  # ||
		if tterms != {}:  # ||
			# i really think this will need to be a merge of the tterms dicts in order to handle multiple patterns
			self.tmpltmap[tmpltDEX][how]['terms'].update(tterms)  # ||
		return self  # ||

	def mapPattern(self, cfg, tmplt, data, how):  # ||
		''
		strts = cfg['base']['pattern']['initialize']  # ||
		ends = cfg['base']['pattern']['finalize']  # ||
		cnt = 0  # ||
		for strt in strts:  # ||
			spat, epat = strt['symbol'], ends[cnt]['symbol']  # ||
			self.mapp(tmplt, data, spat, epat, how)  # ||=>Run method
			cnt += 1  # ||
		return self  # ||

	def matrix(self, tmplt, j, data, cfg={}):  # ||
		'Load matrix data and combine with tmplt data'  # ||
		terms = self.tmpltmap[j]['matrix']['terms']  # ||
		self.mapPattern(cfg, tmplt, data, 'matrix')  # ||map patterns in config
		if list(terms.keys()) == []:  # ||
			return self  # ||
		sdata = {}  # ||
		numTMPLTs = len(terms[list(terms.keys())[0]][0]['data'])  # ||use the first term data to control the loop
		for n in range(numTMPLTs):  # ||create num tmplts
			if n not in sdata.keys():  # ||
				sdata = {n: {}}  # ||
			for term in terms.keys():  # ||proc term
				sdata[n][term] = terms[term][0]['data'][n]  # ||
			self.sub(tmplt, j, sdata[n], cfg)  # ||
			self.tmpltmap['docs'].insert(0, tmplt)  # ||
		self.tmpltmap['docs'].pop(0)  # ||
		return self  # ||

	def procFix(self, term, spat='', epat='', cfg=None):  # ||
		"""Set Prefix and Suffix of the Active Term"""  # ||
		if cfg is None:  # ||
			cfg = thing.What(join(abspath(here), '_data_', 'sub.yaml')).get().dikt  # ||
		prcsrs = cfg['base']['pattern']['processors']  # ||
		symbols = self._collectSymbols(prcsrs)  # ||
		fpats, lpat = [spat] + symbols + [epat], spat  # ||
		n = 0  # ||
		for i in range(len(fpats) - 1):  # ||
			fpat, lpat = fpats[i], fpats[i + 1]  # ||
			t = term.find(fpat)  # ||
			if t != -1:  # ||
				n = t + len(fpat)  # ||
			nl = term.find(lpat)  # ||
			if nl == -1:  # ||
				continue  # ||
			self.fixmap[fpat] = {'fterm': term[n:nl], 'pos': [n, nl]}  # ||
		return self  # ||

	def run(self, full=False, optional=False):  # ||=>Define method
		'process mapp rules based on type allow for depth of rules'  # ||
		if isinstance(self.tmplts, int):
			return [self.tmplts]
		seq = self.config['sequence']  # ||
		cfgs = list(self.config['processors'].keys())  # ||
		for i in seq:  # ||
			cfgp = self.config['processors'][i]['path']  # ||
			cfg = thing.What(join(abspath(here), cfgp)).get().dikt  # ||load config file
			cfgn = self.config['processors'][i]['fx']  # ||
			runner = getattr(self, cfgn)  # ||
			x, shift = 0, 0  # ||
			for j in range(len(self.tmpltmap['docs'])):  # ||cycle templates
				if j not in self.tmpltmap.keys():  # ||
					self.tmpltmap[j] = {cfgn: {'terms': {}}}  # ||
				if cfgn not in self.tmpltmap[j].keys():  # ||
					self.tmpltmap[j][cfgn] = {'terms': {}}  # ||
				tmplt = self.tmpltmap['docs'][j]  # ||
				runner(tmplt, j, self.data, cfg)  # ||
		if optional == True:  # ||
			self.rmvOptional()  # ||=>Run method
		if full == False:  # ||
			if self.diktlock == 1:
				r = []
				for t in self.tmpltmap['docs']:
					st = json.loads(json.dumps(t))
					# print('TMPLT',st)
					r.append(st)
			else:
				r = self.tmpltmap['docs']
			if self.diktlock == 1:
				if not isinstance(r[0], dict):
					print('FAIL')
			return r  # ||
		return self  # ||

	def sub(self, tmplt, j, data, cfg={}):  # ||
		"""Subsitute Template Codes for Data from Template Map"""  # ||
		self.mapPattern(cfg, tmplt, data, 'sub')  # ||map patterns in config
		terms = self.tmpltmap[j]['sub']['terms']  # ||
		for term in list(terms.keys()):  # ||cycle terms
			shift = 0
			self.mapPattern(cfg, tmplt, data, 'sub')  # ||map patterns in confi
			termmap = self.tmpltmap[j]['sub']['terms'][term]  # ||map of each term
			for i in termmap:  # ||
				x, y = i['pos']  # ||position of term
				if term in tmplt or i['code'] in tmplt:  # ||
					front = tmplt[:x + shift]  # ||clip front of term
					back = tmplt[y + shift:]  # ||clip back of term
					if i['data'] == '':  # ||
						continue
					else:  # ||
						sdata = str(i['fterm'])  # ||
					shift += len(sdata) - len(i['code'])  # ||
					tmplt = front + sdata + back  # ||
			self.tmpltmap['docs'].pop(j)  # ||
			self.tmpltmap['docs'].append(tmplt)  # ||
		return self  # ||

	def rmvOptional(self):  # ||
		""" """
		return self  # ||

	def varr(self, tmplt, j, data, cfg={}, optn='incr'):  # ||
		"""
		Define Standard Variables for Lookup and Generation
		:param tmplt: 
		:param j: 
		:param data: 
		:param cfg: 
		:param optn: 
		:return: 
		"""  # ||
		self.mapPattern(cfg, tmplt, data, 'varr')  # ||map patterns in config
		terms = self.tmpltmap[j]['varr']['terms']  # ||
		if len(terms.keys()) == 0:  # ||
			return self  # ||
		for i in range(len(terms.keys())):  # ||cycle terms
			term, sterm = list(terms.keys())[i], ''  # ||
			termmap = terms[term]  # ||map of each term
			try:  # ||
				found, within = search(cfg, [], [], [term])
				varobj = found[0]  # ||
			except Exception as e:  # ||
				break  # ||
			fdata = thingifier.modulize(varobj['object'])  # ||
			fdata = getattr(fdata(), varobj['outs'])  # ||
			for l in range(len(termmap)):  # ||
				k = termmap[l]  # ||
				sdata = {term: fdata}  # ||
				ksub = {'sub': {'terms': {term: [k]}}}  # ||
				self.tmpltmap[j] = ksub  # ||
				self.sub(tmplt, j, sdata, cfg)  # ||
				self.tmpltmap['docs'].insert(0, tmplt)  # ||
			self.tmpltmap['docs'].pop(0)  # ||
			self.tmpltmap[i]['sub']['terms'][term][l]['data'] = fdata  # ||
		return self  # ||

	def _collectSymbols(self, symcfg):  # ||
		fpats = []  # ||
		for fix in symcfg.keys():  # ||
			if symcfg[fix] == None:  # ||
				continue  # ||
			for i in range(len(symcfg[fix])):  # ||
				fpats.append(symcfg[fix][i]['symbol'])  # ||
		return fpats  # ||

def search(this, within, found, keys, recur=False):
	"""find list of keys in tree given a single or multiple set of keys
		switch between searching top level or allowing for crawling down the
		tree branches.  allow for an override of the tree to be searched
		using the inthis variable"""  # ||
	if not isinstance(keys, list):
		keys = list(keys)
	for key in keys:  # ||
		key = str(key)
		if isinstance(this, dict):  # ||
			if key in this.keys():  # ||
				if this[key] not in found:
					found.append(this[key])  # ||
				within.append({key: this})
				if recur == True:  # ||
					load = [this[key], within, found, keys, recur]
					found, within = search(*load)  # ||
			else:
				for val in inthis.values():
					if not isinstance(val, (dict, list)):
						if key in str(val):
							if val not in found:
								found.append(val)
					else:
						found, within = search(val, within, found, keys, recur)
		elif isinstance(this, list):
			for val in this:
				if not isinstance(val, (dict, list)):
					if key in str(val):
						within.append(this)
						if val not in found:
							found.append(val)
				if recur == True:
					found, within = search(val, within, found, keys, recur)
	return found, within | |
# ==============================Source Materials=================================||
"""
	https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
	http://pybem.sourceforge.net/
	http://www.prankster.com/project/index.htm
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

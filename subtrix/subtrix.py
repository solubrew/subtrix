#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	DOCid: 03a412f8-c767-467e-9044-ea7cf19c2f9e
	name: Element Level Rule Module Python Document
	description: >
		Implement rule system of document markup and data expansion
		through substitution, functions, loops
	expirary: <[expiration]>
	version: <[version]>
	path: <[LEXIvrs]>pheonix/elements/rule/rule.py
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#=======================================================================||
import os, datetime as dt, json#										||
import multiprocessing as mp#											||
from yaml import load as yload, dump as ydump#							||
try:#																	||
	from yaml import CLoader as Loader, CDumper as Dumper#				||
except:#																||
	from yaml import Loader, Dumper#									||
#=======================================================================||
#from pheonix.elements.calcgen import tree as calctr#					||
#from pheonix.elements.config import config#								||
#from pheonix.elements.store import store#								||
#from pheonix.elements.thing import thing#								||
from util import calctr
#================Common Globals=========================================||
here = os.path.join(os.path.dirname(__file__),'')#						||
there = os.path.abspath(os.path.join('../../..'))#						||set path at pheonix level
version = '0.0.0.0.0.0'#												||
#=======================================================================||
class mechanism:#														||
	'Perform simple replacement in templates'#							||=>Describe class
	version = '0.0.0.0.0.0'#											||=>Set version
	def __init__(self, tmplts=[], data={}, rules=None, cfg=None):#		||
		self.tmplts, self.diktlock = tmplts, 0
		if isinstance(tmplts, str):#									||
			tmplts = [tmplts,]#											||
		elif isinstance(tmplts, dict):#									||
			tmplts = [json.dumps(tmplts)]#								||
			self.diktlock = 1
		self.data = data#												||
		if cfg != None:#												||
			config = getYAML(cfg)#						||
		pxcfg = '{0}z-data_/rule.yaml'.format(here)#								||use default configuration
		self.config = getYAML(pxcfg)#						||load configuration file
		if rules != None:#												||
			cfg = '{0}z-data_/rules'.format(here)#									||set folder path
			rules = getYAML(cfg)#						||read files in directory
		self.tmpltmap = {'tmplts': tmplts, 'docs': tmplts}#				||set vars
		self.tipe = self.config['system']['name']#						||
	def findPattern(self, spat, epat, tmplt, inclusive=True):#			||=>Define module
		'check text for patterns'#										||=>Describe module
		self.lock, self.term = False, ''#								||Set the cycle lock to open
		snum = tmplt.find(spat)#										||find start pattern
		enum = snum+tmplt[snum:].find(epat)+len(epat)#					||find end patter after start
		if snum > enum:#												||
			comm.see('rule.findPattern Failed')#						||
		if snum != -1 and enum != -1:#									||chk both patterns found
			self.term = tmplt[snum:enum]#								||clip term from template code
			if spat in tmplt[enum:]:#									||verify the need to keep working
				self.lock = True#										||Set the cycle lock to closed
		return snum, enum#												||
	def func(self, tmplt, j, data, cfg={}):#							||
		'process all functions'#										||
		self.mapPattern(cfg, tmplt, data, 'func')#						||map patterns in config
		terms = self.tmpltmap[j]['func']['terms']#						||
		tree = calctr(cfg)#										||
		termsLS = list(terms.keys())
		termsLS.sort()
		if len(termsLS) == 0:#										||
			return self#												||
		for i in range(len(termsLS)):#								||cycle terms
			term, sterm = termsLS[i], ''#					||
			termmap = terms[term]#										||map of each term
			try:#														||
				varobj = tree.search([term]).found[0]#					||
			except Exception as e:#										||
				break#													||
			fdata = config.instruct(varobj['object']).modulize().obj#	||
			fdata = getattr(fdata(), varobj['outs'])#					||
			for l in range(len(termmap)):#								||
				k = termmap[l]#											||
				sdata = {term: fdata}#									||
				ksub =  {'sub': {'terms': {term: [k]}}}#				||
				self.tmpltmap[j] = ksub#								||
				self.sub(tmplt, j, sdata, cfg)#							||
				self.tmpltmap['docs'].insert(0, tmplt)#					||
			self.tmpltmap['docs'].pop(0)#								||
			self.tmpltmap[i]['sub']['terms'][term][l]['data'] = fdata#	||
		return self#													||
	def getDterm(self, data, cterm, scode, sterm):#						||
		'Get term from data'#											||
		dterm = ''#														||
		if isinstance(data, dict):#										||
			if sterm in data.keys():#									||
				dterm = data[sterm]#									||
			elif scode in data.keys():#									||
				dterm = data[scode]#									||
			else:#														||
				dterm = ''#												||
		elif isinstance(data, list):#									||
			dterm = data[cterm]#										||
		return dterm#													||
	def getFterm(self, fmap, dterm, spat, how='sub'):#					||
		'Get '
		fterm = ''#														||
		if spat in fmap.keys():#										||
			fterm += str(fmap[spat]['fterm'])#							||
		fterm += str(dterm)#											||
		if ':.' in fmap.keys():#										||
			fterm += str(fmap['.:']['fterm'])#						||
		return fterm#													||
	def loop(self, tmplt, j, data, cfg={}):#							||
		'Load loop data and combine with tmplt data'#					||
		self.mapPattern(cfg, tmplt, data, 'loop')#						||map patterns in config
		terms = self.tmpltmap[j]['loop']['terms']#						||
		if list(terms.keys()) == []:#									||
			return self#												||
		ndata, shift, lterm, r = {}, 0, '', ''#							||
		for term in sorted(terms.keys()):#								||Cycle list of loop terms
			if lterm == term:
				continue
			termmap = terms[term]#										||map of each term
			termmap.sort()
			for iterm in termmap:#								||
				code = iterm['code']#								||
				ndata = ''#												||
				lock = 0#												||
				iterm['data'].sort()
				for d in range(len(iterm['data'])):#				||
					for mod in sorted(iterm['mods'].keys(), reverse=True):#	||
						r =  str(iterm['mods'][mod]['fterm'])#		||
						if r in term:#									||
							ndata += iterm['data'][d]#				||
						else:#											||
							if lock != 0:#								||
								ndata += r#								||
						lock = 1#										||
				ndata = ndata[:-len(r)]
				self.sub(tmplt, j, {term: ndata}, cfg)#		||
				break#this is a hack that should come out with better handling of multi loop templates
			lterm = term
			tmplt = self.tmpltmap['docs'][j]#							||
		return self#													||
	def mapp(self, tmplt, data, spat='<[', epat=']>', how='sub'):#		||=>Define module
		'Create Dictionary of all rule pattern found in template document'#	||
		self.spat, self.epat = spat, epat#								||set bookend patterns
		self.lock, self.fixmap, cterm = True, {}, 0#					||set variables
		tmpltDEX = self.tmpltmap['docs'].index(tmplt)#					||
		ntmplt, pl, tterms = tmplt, 0, {}#								||
		while self.lock:#												||lock until all patterns are removed
			snum, enum = self.findPattern(spat, epat, ntmplt)#			||find the next term
			if self.term != '':#										||
				self.fixmap = {}#										||prefix,suffix map
				self.procFix(self.term, spat, epat)#					||call prefix/suffix processer
				if ':.' in self.fixmap.keys():#							||
					sterm = self.fixmap[':.']['fterm']#					||
				else:#													||
					sterm = self.fixmap['.:']['fterm']#					||
				cterm += 1#												||
				scode = spat+sterm+epat#								||
				dterm = self.getDterm(data, cterm, scode, sterm)#		||
				fterm = self.getFterm(self.fixmap, dterm, spat, epat)#	||
				if scode not in tterms.keys():#							||
					tterms[scode] = []#									||
				tterms[scode].append({'code': self.term,#				||
											'pos': [pl+snum, pl+enum],#	||add simple term and full term to mapp dikt
											'data': dterm,#	 			||
											'fterm': fterm,#			||
											'mods': self.fixmap})#		||
				pl += enum#												||
				ntmplt = ntmplt[enum:]#									||
		if tterms != {}:#												||
			#i really think this will need to be a merge of the tterms dicts in order to handle multiple patterns
			self.tmpltmap[tmpltDEX][how]['terms'].update(tterms)#		||
		return self#													||
	def mapPattern(self, cfg, tmplt, data, how):#						||
		''
		strts = cfg['base']['pattern']['initialize']#					||
		ends = cfg['base']['pattern']['finalize']#						||
		ends = sorted(ends, key=lambda i: i['symbol'])
		cnt = 0#														||
		for strt in sorted(strts, key=lambda i: i['symbol']):#			||
			spat, epat = strt['symbol'], ends[cnt]['symbol']#			||
			self.mapp(tmplt, data, spat, epat, how)#					||=>Run method
			cnt += 1#													||
		return self#													||
	def matrix(self, tmplt, j, data, cfg={}):#							||
		'Load matrix data and combine with tmplt data'#					||
		terms = self.tmpltmap[j]['matrix']['terms']#					||
		self.mapPattern(cfg, tmplt, data, 'matrix')#					||map patterns in config
		if list(terms.keys()) == []:#									||
			return self#												||
		sdata = {}#														||
		numTMPLTs = len(terms[list(terms.keys())[0]][0]['data'])#		||use the first term data to control the loop
		for n in range(numTMPLTs):#										||create num tmplts
			if n not in sdata.keys():#									||
				sdata = {n: {}}#										||
			for term in sorted(terms.keys()):#										||proc term
				sdata[n][term] = terms[term][0]['data'][n]#				||
			self.sub(tmplt, j, sdata[n], cfg)#							||
			self.tmpltmap['docs'].insert(0, tmplt)#						||
		self.tmpltmap['docs'].pop(0)#									||
		return self#													||
	def procFix(self, term, spat='', epat='', cfg=None):#				||
		'Set Prefix and Suffix of the Active Term'#						||
		if cfg == None:#												||
			cfg = '{0}z-data_/rule/sub.yaml'.format(here)#				||
			cfg = getYAML(cfg)#						||
		prcsrs = cfg['base']['pattern']['processors']#					||
		symbols = self._collectSymbols(prcsrs)#							||
		fpats, lpat = [spat]+symbols+[epat], spat#						||
		n = 0#															||
		for i in range(len(fpats)-1):#									||
			fpat, lpat = fpats[i], fpats[i+1]#							||
			t = term.find(fpat)#										||
			if t != -1:#												||
				n = t+len(fpat)#										||
			nl = term.find(lpat)#										||
			if nl == -1:#												||
				continue#												||
			self.fixmap[fpat] = {'fterm': term[n:nl], 'pos': [n, nl]}#	||
		self.fixmap = {k: self.fixmap[k] for k in sorted(self.fixmap.keys(), reverse=True)}
		return self#													||
	def run(self, full=False, optional=False):#							||=>Define method
		'process mapp rules based on type allow for depth of rules'#	||
		if isinstance(self.tmplts, int):
			return [self.tmplts]
		seq = self.config['sequence']#									||
		for i in seq:#													||
			cfgp = self.config['processors'][i]['path']#				||
			cfg = getYAML('{0}{1}'.format(here, cfgp))
			cfgn = self.config['processors'][i]['fx']#					||
			runner = getattr(self, cfgn)#								||
			x, shift = 0, 0#											||
			for j in range(len(self.tmpltmap['docs'])):#				||cycle templates
				if j not in self.tmpltmap.keys():#						||
					self.tmpltmap[j] = {cfgn: {'terms': {}}}#			||
				if cfgn not in self.tmpltmap[j].keys():#				||
					self.tmpltmap[j][cfgn] = {'terms': {}}#				||
				tmplt = self.tmpltmap['docs'][j]#						||
				runner(tmplt, j, self.data, cfg)#						||
		if optional == True:#											||
			self.rmvOptional()#											||=>Run method
		if full == False:#												||
			if self.diktlock == 1:
				r = []
				for t in self.tmpltmap['docs']:
					st = json.loads(json.dumps(t))
					r.append(st)
			else:
				r = self.tmpltmap['docs']
			if self.diktlock ==1:
				if not isinstance(r[0], dict):
					print('FAIL')
			return r#													||
		return self#													||
	def sub(self, tmplt, j, data, cfg={}):#								||
		'Subsitute Template Codes for Data from Template Map'#			||
		data = {k: data[k] for k in sorted(data.keys())}
		self.mapPattern(cfg, tmplt, data, 'sub')#						||map patterns in config
		terms = self.tmpltmap[j]['sub']['terms']#						||
		for term in sorted(terms.keys()):#										||cycle terms
			shift = 0
			termmap = self.tmpltmap[j]['sub']['terms'][term]#			||map of each term
			termmap.sort()
			for i in termmap:#											||
				x, y = i['pos']#										||position of term
				if term in tmplt or i['code'] in tmplt:#				||
					front = tmplt[:x+shift]#							||
					back = tmplt[y+shift:]#								||clip term
					if i['data'] == '':#								||
						continue
					else:#												||
						#TODO: Fix the below##################################
						i['fterm'] = i['fterm'].replace('[', '').replace(']','')
						if isinstance(i['fterm'], list):
							sdata = list2str(i['fterm'])
						######################################################
						else:
							sdata = str(i['fterm'])#						||
					shift += len(sdata)-len(i['code'])#					||
					tmplt = front+sdata+back#							||
			self.tmpltmap['docs'].pop(j)#								||
			self.tmpltmap['docs'].append(tmplt)#						||
		return self#													||
	def rmvOptional(self):#												||
		''
		return self#													||
	def varr(self, tmplt, j, data, cfg={}, optn='incr'):#				||
		'Define Standard Variables for Lookup and Generation'#			||
		self.mapPattern(cfg, tmplt, data, 'varr')#						||map patterns in config
		terms = self.tmpltmap[j]['varr']['terms']#						||
		tree = calctr(cfg)#										||
		if len(terms.keys()) == 0:#										||
			return self#												||
		for i in range(len(terms.keys())):#								||cycle terms
			term, sterm = list(terms.keys())[i], ''#					||
			termmap = terms[term]#										||map of each term
			try:#														||
				varobj = tree.search([term]).found[0]#					||
			except Exception as e:#										||
				break#													||
			fdata = config.instruct(varobj['object']).modulize().obj#	||
			fdata = getattr(fdata(), varobj['outs'])#					||
			for l in range(len(termmap)):#								||
				k = termmap[l]#											||
				sdata = {term: fdata}#									||
				ksub =  {'sub': {'terms': {term: [k]}}}#				||
				self.tmpltmap[j] = ksub#								||
				self.sub(tmplt, j, sdata, cfg)#							||
				self.tmpltmap['docs'].insert(0, tmplt)#					||
			self.tmpltmap['docs'].pop(0)#								||
			self.tmpltmap[i]['sub']['terms'][term][l]['data'] = fdata#	||
		return self#													||
	def _collectSymbols(self, symcfg):#									||
		fpats = []#														||
		for fix in sorted(symcfg.keys()):#								||
			if symcfg[fix] == None:#									||
				continue#												||
			symcfg[fix].sort()
			for i in range(len(symcfg[fix])):#						||
				fpats.append(symcfg[fix][i]['symbol'])#					||
		return fpats#													||
	def identify(self, code=None, how='incr'):#							||
		'how->[incr,uuid,find,date,tuuid]'#								||
		if code == None:#												||
			code = 'GENRL'#												||
		if how == 'incr':#												||
			db = self.config['data']['things']['ID']#					||
			verse = acct.prime().verse#									||
			data = {'verse': verse}#									||
			db = tmplt.thing(db, data).ran()#							||
			idnt = grab.stuff(db).nextrecord(code)#						||
#			print('idnt rule returned',idnt)#							||
		elif how == 'uuid':#											||
			pass#														||
		elif how == 'find':#											||
			pass#														||
		return idnt#													||
#	def incid(self, name):#												||
#		table = name[2:-len(name)+len(':.incid]>')-1]#					||
#		inc = mechanism([name]).identify(table)#					||lookup identity and increment name
#		name = tmplt.thing(name, {'incid':inc}).ran()#					||fill template
#		return name#													||
def getYAML(path):
	with open(path, 'r') as doc:#										||
		dikt = yload(doc.read().replace('\t','  '), Loader=Loader)#		||
	return dikt
def list_2_str(ls=None, quote=0):#							||
	''
	if ls == None:
		ls = self.it
	if quote != 2:
		quote = 0#													||
		for l in ls:#												||
			if not isinstance(l, int):#								||
				quote = 1#											||
	if quote == 1:#													||
		s = "'"#													||
		for l in ls:#												||
			s += str(l)+"', '"#										||
		s = s[:-3]#													||
	else:#															||
		s = ""#														||
		for l in ls:#												||
			s += str(l)+","#										||
		s = s[:-1]#													||
	it = s
	return it#													||
#==================Code Source Examples=================================||
#https://gist.github.com/angstwad/bf22d1822c38a92ec0a9
#http://pybem.sourceforge.net/
#http://www.prankster.com/project/index.htm
#============================:::DNA:::==================================||
'''
<(DNA)>:
	201906170059:
		refactored rule module
	201804101534:
		mechanism:
			version: 0.0.0.0.0.0
			test:
			description: >
				Compacted Rule, Template and Group rezeroing to Rule
			work:
			compaction:
				201804101534:
					coupling:
						version: <[active:.version]>
						test:
						description: >
							Couple tmplts and data with rule systems implicitally
							and explicitally
						work:
				201804101534:
					here:
						version: <[active:.version]>
						test:
						description: >
							Define Rule Routing for Utilization of Multiple Rule Systems
						work:
				201804101213:
					administer:
						version: <[active:.version]>
						test:
						description: >
							Administrate Tests of the Tmplt Classes
						work:
				201804101213:
					here:
						version: <[active:.version]>
						test:
						description: >
							Test Each Tmplt Class
						work:
				201811132207:
					thing:
						version: 0.0.0.0.2.0
						test: FAIL
						description: >
							rewrite template module to simplify logic
							created more extensive template map
						work:
				201804091305:
					thing:
						version: 0.0.0.0.1.1
						test: PASS
						description: >
							Correct for Full Test
						work:
				201804091231:
					thing:
						version: 0.0.0.0.1.1
						test: FAIL
						description: >
							update to map prefixes and suffixes properly
						work:
							- 201804091200
				201804091111:
					thing:
						version: 0.0.0.0.1.0
						test: PASS
						description: >
							rewrite to process template first and populate
							with given data alinearly
						work:
							- 201804091030
							- 201804082200
				201804051642:
					thing:
						version: 0.0.0.0.0.2
						test: PASS
						description: >
							added map_terms and rmvOptional methods to the class
						work:
							- 201804051536
				201804022117:
					thing:
						version: 0.0.0.0.0.1
						test: PASS
						description: >
							rewrite to process template first and populate
							with given data alinearly
						work:
'''

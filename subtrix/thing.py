# @@@@@@@@@@Thing.Thing - Thankless Thackisaur@@@@@@@@@@@||
"""
---
<(meta)>:
	DOCid: <^[uuid]^>
	name: Elements Level Thing Module Python Document
	description: >
	expirary: <[expiration]>
	version: <[Version]>
	path: <[LEXIvrs]>pheonix/elements/thing/thing.py
	outline: <[outline]>
	authority: document|this
	security: seclvl2
	<(wt)>: -32
"""
# -*- coding: utf-8 -*-
# =======================================================================||
import datetime as dt, uuid, socket, platform
from os import environ, name
from os.path import abspath, dirname, exists, join
import pytz
from dateutil.parser import parse
import urllib.request
try:  # ||
	from yaml import CLoader as Loader, CDumper as Dumper  # ||
except ImportError:  # ||
	print('YAML Failed')
try:
	from yaml import load as yload, dump as ydump, FullLoader  # ||
except:
	print('YAML Failed')
try:
	from yaml import Loader, Dumper  # ||
except:
	print('YAML Failed')
try:
	import simplejson as j
except:
	pass
try:
	from yamllint import linter as yamllinter
	from yamllint.config import YamlLintConfig
except:
	pass
from yamlinclude.constructor import YamlIncludeConstructor

try:
	import h5py
except:
	print('No h5py')
# ===============================================================================||
here = join(dirname(__file__), '')
there = abspath(join('../../..'))  # set path at pheonix level
version = '0.0.0.0.0.0'
log = True
# =======================================================================||
pxcfg = join(abspath(here), '_data_/thing.yaml')  # use default configuration

def getName():
    """build out a generalized name generation tool

		integrate with calcgen.text.name method
	"""
    return 'namesomething'


class What:
    """provide basic identifying data Load Basic Things for intial build
		blocks"""
    version = '0.0.0.0.0.2'

    def __init__(self, it=None, cfg=None):
        self.it = it
        self.dikt = {}
        self.config = self.get(pxcfg).dikt
        self.uuid()

    def gen(self, how='open', given=None):
        if given == None:
            out = self.uuid().ruuid
        yield out

    def get(self, thing=None):
        """ """
        if thing == None:
            thing = self.it
        self.text = ''
        # if not exists(thing):
        #     return self
        if exists(thing):
            try:
                with open(thing, 'r') as doc:
                    text = doc.read()
            except Exception as e:
                text = ''
                print('Couldnt Open', thing, 'due to', e)
        else:
            text = thing
        self.text = str(text)
        try:
            base_path = thing[:thing.rfind('/') + 1]  # ||
            text = text.replace('\t', '  ')  # correct yaml format
            doct = f'{text}'  # ||correct yaml format
            params = {'loader_class': FullLoader, 'base_dir': base_path}  # ||
            YamlIncludeConstructor.add_to_loader_class(**params)  # ||
            self.dikt = yload(doct, Loader=FullLoader)  # load yaml str to dikt
        except Exception as e:
            print('Couldnt Load YAML document ', thing, 'due to', e)
        return self

    def uuid(self):
        """"""
        self.ruuid = str(uuid.uuid4())
        self.hexid = uuid.UUID(self.ruuid).hex
        self.intid = uuid.UUID(self.ruuid).int  # need to fix uuid5 add namespace and name
        self.hostuuid = uuid.uuid1()  # hostID & cur time based UUID
        return self

    def symbols(self, language, tipe):
        symbols = self.get(self.config['symbols'])

class When:
    'get a basic time object'
    version = '0.0.0.0.0.0'  # =>Version Class

    def __init__(self, it=None, cfg=None):
        self.it = it
        self.its = []
        if cfg == 'type':
            self._type()
        if cfg != None:
            cfg = What().get(cfg).dikt
        self.config = What().get(pxcfg).dikt  # load configuration file
        self.now = dt.datetime.now()
        self.dtid = self.credtid()
        self.dtids = [self.dtid, ]
        self.start = ''
        self.today = self.now.strftime('%Y%m%d')
        self.today_dashed = self.now.strftime('%Y-%m-%d')
        self.it = it
        self.timestamp = self.now.timestamp()
        self.month = self.now.strftime('%m')
        self.year = self.now.strftime('%Y')
        self.day = self.now.strftime('%d')
        self.hour = self.now.strftime('%H')
        self.minute = self.now.strftime('%M')
        self.second = self.now.strftime('%S')

    def back(self, inc):
        """ """
        print('INC', inc[-1:])
        if inc[-1:] == 'h':
            incn = float(inc[:len(inc) - 1])
        elif inc[-1:] == 'd':
            incn = self.now - dt.timedelta(days=(1))
            incn = incn.strftime('%Y%m%d')
        print('INCN', incn)
        return self

    # def cast(self, phormats=None):
    # 	""" """
    # 	if not isinstance(phormats, list):
    # 		phormats = [phormats]
    # 	for phormat in phormats:
    # 		try:
    # 			self.day = makeDateTime(self.it, phormat)
    # 			break
    # 		except Exception as e:
    # 			pass
    # 		# print(f'Cast {self.it} using {phormat} failed due to {e}')
    # 	self._tzaware()
    # 	return self

    def credtid(self):
        'A Unique 5 digit hexidecimal padded to a time stamp'
        d = dt.datetime.now().strftime('%Y%m%d%H%M%S')
        dtid = f'{d}.' + What().uuid().ruuid[-5:]
        return dtid

    # def epoch(self):
    # 	""" """
    # 	t = time.mktime(date(y, m, d).timetuple()) / 86400
    # 	self.epoch = int(round(t, 0) * 86400)
    # 	return self

    def full(self, date=None):
        if date == None:
            self.now = dt.datetime.now()
            date = self.now
        if isinstance(date, (int, str)):
            if len(date) > 11:
                date = int(date) / 1000
            date = dt.datetime.fromtimestamp(int(date))
        self.dayofyear = date.strftime('%j')
        self.dayofweek = date.strftime('%A')
        self.a = date.strftime('%a')
        self.weekofyear = date.strftime('%W')
        self.month = date.strftime('%m')
        self.year = date.strftime('%Y')
        self.day = date.strftime('%d')
        self.hour = date.strftime('%H')
        self.minute = date.strftime('%M')
        self.second = date.strftime('%S')
        self.amrc_date = date.strftime('%m%d%Y')  # Standard american date format
        self.erp_date = date.strftime('%Y%m%d')  # European date format
        self.prg_date = date.strftime('%Y.%m.%d')  # program date format
        self.prg_datetime = date.strftime('%Y.%m.%d.%H.%M.%S')
        return self

    def gen(self, how='dtid', given=None):
        if given == None:
            given = What().uuid().ruuid[-5:]
        if how == 'print':
            phormat = '%Y-%m-%d %H:%M:%S'
            tipe = 1
        elif how == 'store':
            phormat = '%Y%m%d%H%M%S'
            tipe = 1
        elif how == 'dtid':
            tipe = 3  #:::todo:::#												||
        elif how == 'object':
            tipe = 2
        out = dt.datetime.now()
        if tipe == 1:
            out = dt.datetime.strftime(out, phormat)
        elif tipe == 2:
            out = out
        # elif tipe == 3:#														||
        # 	out = self.credtid()#												||
        elif tipe == 3:
            if given != None:
                self.dtid += 'a' + str(given)
            out = self.dtid
        yield out

    def getStr(self, phormat):
        """ """
        return dt.datetime.strftime(self.day, phormat)

    def last(self, gdate, gtime=None, gzone=None):
        week = ["monday", "tuesday", "wednesday", "thursday", "friday",
                "saturday", "sunday"]
        try:
            pos = week.index(gdate.lower())
            #			last = self.now + dt.timedelta(days=(pos - self.now.weekday()), time=(gtime-self.now.time()))#	||
            last = self.now + dt.timedelta(days=(pos - self.now.weekday()))
            if gtime != None:
                pass
            day = (last if last <= self.now else last - dt.timedelta(days=7))
            day = dt.datetime.strftime(day, '%Y%m%d')
        except Exception as e:
            print('When Last', e)
            day = None
        # build out
        # 'week':
        # 'month':
        # 'quarter':
        # 'year':
        if gtime != None:
            pass

        return day

    def uutc(self, u):
        ts = dt.datetime.fromtimestamp((u.time - '0x01b21dd213814000L') * 100 / 1e9)
        print(ts)
        return self

    def _type(self):
        if isinstance(self.it, str):
            self._parse(self.it)
        self._identify()
        return self

    def _parse(self, data, cfg=None):
        if cfg == None:
            self.it = data[:-9]
        dividers = ['/', '-', '.', ' ', ':', ' ']
        for div in dividers:
            if div in data:
                for i in data.split(div):
                    self.its.append(i)
                break
        return self

    def _identify(self):
        self.year, self.month, self.day = 0, 0, 0
        cnt = 0
        if log: print('Date Components', self.its)
        for i in self.its:
            if len(i) == 4:
                self.year = i
                if cnt == 0:
                    self.day = self.its[2]
                elif cnt == 2:
                    self.day = self.its[0]
            cnt += 1
        if int(self.its[1]) < 13 and int(self.its[1]) > 0:
            self.month = self.its[1]
        return self

# def _cast(self, known=None):
# 	try:
# 		if known != None:
# 			self.day = arrow.datetime.strptime(self.it, known).date()
# 		else:
# 			self.day = arrow.date(int(self.year), int(self.month),
# 								  int(self.day))
# 	except Exception as e:
# 		if log: print('When Date Construction Failed due to', e)
# 	#			self.day = arrow.date(int('1420'), int('01'), int('01'))#		||
# 	return self
#
# def _tzaware(self):
# 	"""Add a timezone aware attribute for each date attribute """
# 	try:
# 		self.day_tz_aware = pytz.utc.localize(self.day)  # tzaware
# 	except Exception as e:
# 		if log: print(f'TZ Awareness for {self.day} failed due to {e}')
# 		self.day_tz_aware = self.day
# 	return self


class Where:
    'Set connections to the controlling device by prime and concern'
    version = '0.0.0.0.0.0'

    def __init__(self, active='prime'):
        self.active = active
        self.verses = {}
        self.device()

    def device(self):
        'Get information about the interacting device'
        self.home = environ['HOME']
        if socket.gethostname().find('.') >= 0:
            self.name = socket.gethostname()
        else:
            self.name = socket.gethostbyaddr(socket.gethostname())[0]
        self.ip = self.getIP()
        self.ostype = name
        self.architecture = platform.machine()
        #		self.version = platform.linux_distribution()[0]#				||
        self.kernel = platform.release()
        self.sysname = platform.system
        self.verses['LEXIvrs'] = abspath(join('../../../..'))
        self.verses['DATAvrs'] = '{0}/data'.format(self.home)
        self.verses['WORKvrs'] = '{0}/DataWorkRepo'.format(self.home)
        self.verses['VEINvrs'] = '{0}/vein'.format(self.home)
        return self  # =>

    def getIP(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        try:  # doesn't even have to be reachable
            s.connect(('10.255.255.255', 1))
            IP = s.getsockname()[0]
        except:
            try:
                IP = socket.gethostbyname(socket.gethostname())
            except:
                IP = '127.0.0.1'
        finally:
            s.close()
        return IP

    def getExtIP(self):
        """ """
        services = ['https://ident.me']
        for serv in services:
            eIP = urllib.request.urlopen(serv).read().decode('utf8')
            return eIP


class Who:
    """	"""  # =>Describe class
    version = '0.0.0.0.0.0'  # =>Set version

    def __init__(self, it=None, cfg=None):
        self.config = What(pxcfg).get().dikt  # load configuration file
        self.it = it

    def prime(self, prime={}):
        """ """
        if isinstance(prime, str):
            pass  # TODO: need to lookup in afile somehwere
        else:
            self.accts = prime['accts']
            self.contacts = prime['contacts']
            self.devices = prime['devices']
            self.docs = prime['docs']
            self.ops = prime['OPs']
            self.reqs = prime['REQs']
            self.stores = prime['stores']
            self.tmplts = ['tmplts']
            asprime = What().get(prime).dikt['prime']
            # prime = '/home/solubrew/ActiveProjects/devLEXI/3_Work/1_DELTA/'.yaml'
            self.prime = What(prime).get().dikt
        return self


def makeDateTime(d, f=None):
    """identify given date format and return a properly formated time object
	"""
    if isinstance(d, dt.datetime):
        return d
    if d == None:
        return d
    if f == None:
        yearfirst = True
        if d[-1] in ('z', 'Z'):  # handle iso datetime ending with a Z charater
            try:
                return parse(d)
            except Exception as e:
                pass
        if log: print('D', d, len(d), d[0])
        if len(d) == 8 and d[0] in ('2', '1'):  # this should hack my needs but creates a huge
            if log: print('Date Hole')
            pass  # not sure how to dif, check each year
        else:
            # edge issue for all 8 digit timestamps
            try:  # this could trigger on un divided dates as well as actual timestamps
                return dt.datetime.fromtimestamp(int(d))
            except Exception as e:
                pass
        if len(d) == 24:
            f = '%Y/%m/%d %H:%M:%S+%T'
            return dt.datetime.strptime(d, f)
        elif len(d) == 25:  # need to verify its with colon? or not others
            f = '%Y-%m-%dT%H:%M:%S%z'
            return dt.datetime.strptime(d, f)
        dividers = ['/', '-']
        for div in dividers:
            if d.find(div) == 2:
                yearfirst = False
                break
        d = d.replace(div, '')
        if len(d) == 14:
            f = '%Y%m%d%H%M%S'
        elif len(d) == 12:
            f = '%Y%m%d%H%M'
        elif len(d) == 10:
            f = '%Y%m%d%H'
        elif len(d) == 8:
            f = '%d%m%Y' if yearfirst == False else '%Y%m%d'
        elif len(d) == 6:
            f = '%m%Y' if yearfirst == False else '%Y%m'
        else:
            print('Unknown Format', d, 'Length', len(d))
    return pytz.utc.localize(dt.datetime.strptime(d, f))


# ==========================Source Materials=============================||
"""
https://docs.python.org/3.6/library/hashlib.html
https://docs.python.org/3.6/library/uuid.html
https://stackoverflow.com/questions/3694487/in-python-how-do-you-convert-seconds-since-epoch-to-a-datetime-object

externalIP
https://www.ipify.org/
https://api.ipify.org/
https://ident.me/
20210902 - 69.27.55.138...I think I'm probably pretty static with BNS

"""
# ===========================:::DNA:::===================================||
"""
<(DNA)>:
	201811142009:
		thing:
			version: 0.0.0.0.0.0
			test:
			description: >
				Compacted subtrix, Template and Group rezeroing to subtrix
			work:
				compaction:
					201804111051:
						administer:
							version: <[active:.version]>
							test:
							description: >
								comment out sha1id needs namespace and name arguements
							work:
					201804111051:
						administer:
							version: 0.0.0.0.0.1
							test:
							description: >
								add additional uuid options
							work:
					201804101213:
						administer:
							version: 0.0.0.0.0.0
							test: PASS
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
"""
# @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@Controlled@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

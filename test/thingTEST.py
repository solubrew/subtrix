#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''
---
<(META)>:
	docid: '6705b527-60ca-48a8-9d67-357b22afd1fe'
	name: Subtrix Module Python Testing Document
	description: >
	expirary: <[expiration]>
	version: <[version]>
	outline: <[outline]>
	authority: document|this
	security: sec|lvl2
	<(WT)>: -32
'''
# -*- coding: utf-8 -*-
#===============================================================================||
from os.path import abspath, dirname, join
import unittest
from subtrix.thing import What, Where, When, Who, makeDateTime
#========================Common Globals=========================================||
here = join(dirname(__file__),'')#												||
there = abspath(join('../../..'))#												||set path at pheonix level
version = '0.0.0.0.0.0'#														||
log = False
#===============================================================================||
pxcfg = f'{here}/_data_/thingTEST.yaml'

class Test_Thing_What(unittest.TestCase):
    """ """
    def test_All(self):
        """ """
        self.test()
        self.test_What_gen()
        self.test_What_get()
        self.test_What_uuid()
        self.test_What_symbols()

    def test(self):
        """ """
        path = ''
        self.test_What = What(path)
        #Check It
        self.assertEqual(path, self.test_What.it)
        #Check Config
        self.assertEqual(isinstance({}, dict), isinstance(self.test_What.dikt, dict))
        #Check rUUID
        self.assertEqual(10, len(self.test_What.ruuid))
        #Check hexid

        #Check intid

        #Check hostuuid


    def test_What_gen(self):
        """ """
        uuid = self.test_What.gen()
        self.assertEqual(10, len(uuid))

    def test_What_get(self):
        """ """
        self.test_What.get()

    def test_What_uuid(self):
        """ """

    def test_What_symbols(self):
        """ """

class Test_Thing_When(unittest.TestCase):
    """ """
    def test_All(self):
        """ """

    def test(self):
        """ """
        self.test_When = When()

    def test_When_back(self):
        """ """

    def test_When_credtid(self):
        """ """
        pass

class Test_Thing_Where(unittest.TestCase):
    """ """
    def test_All(self):
        """ """

    def test(self):
        """ """

class Test_Thing_Who(unittest.TestCase):
    """ """
    def test_All(self):
        """ """

    def test(self):
        """ """

class Test_Thing_makeDateTime(unittest.TestCase):
    """ """
    def test_All(self):
        """ """

    def test(self):
        """ """

if __name__ == '__main__':
    unittest.main()



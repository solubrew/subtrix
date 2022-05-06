#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@            @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||
'''  #																			||
---  #																			||
<(META)>:  #																	||
	DOCid:   #																	||
	name: TIGR   #																||
	description: >  #															||
	expirary: <[expiration]>  #													||
	version: <[version]>  #														||
	path: <[LEXIvrs]>  #														||
	outline: <[outline]>  #														||
	authority: document|this  #													||
	security: sec|lvl2  #														||
	<(WT)>: -32  #																||
''' #																			||
# -*- coding: utf-8 -*-#														||
#==============================Core Modules=====================================||
from setuptools import setup, find_packages
from setuptools.command.test import test as TestCommand
import codecs, io, os, re, sys
#===============================================================================||
here = os.path.abspath(os.path.dirname(__file__))
version_file = open(os.path.join(here, '<[name]>', '__init__.py'), 'r')
__version__ = re.sub(r".*\b__version__\s+=\s+'([^']+)'.*", r'\1',
    [line.strip() for line in version_file if '__version__' in line].pop(0))
version_file.close()
def read(*filenames, **kwargs):
    encoding = kwargs.get('encoding', 'utf-8')
    sep = kwargs.get('sep', '\n')
    buf = []
    for filename in filenames:
        with io.open(filename, encoding=encoding) as f:
            buf.append(f.read())
    return sep.join(buf)
short_description = """"""
try:
    long_description = read('README.md')
except IOError:
    long_description = "See README.md where installed."
class PyTest(TestCommand):
    def finalize_options(self):
        TestCommand.finalize_options(self)
        self.test_args = []
        self.test_suite = True
    def run_tests(self):
        import pytest
        errcode = pytest.main(self.test_args)
        sys.exit(errcode)
tests_require = [<[test_packages]>]
setup(name='<[name]>', version='0.1',
		description='<[description]>',
		url='<[url]>',
		author='<[author]>',
		author_email='<[author_email]>',
		license='<[license]>',
		tests_require=tests_require,
		include_package_data=True,
		install_requires=[<[requirements]>],
		cmdclass={'test': PyTest},
		namespace_packages=['<[name]>',],
		packages=[<[packages]>], platforms='any', zip_safe=False,
		classifiers=[<[classifiers]>],
		extras_require={'testing': tests_require, })
#==============================Source Materials=================================||
'''
'''
#================================:::DNA:::======================================||
'''
<(DNA)>:
  <(WT)>: 32
  <@[datetime]@>:
    <[class]>:
      version: <[active:.version]>
    test:
    description: >
      <[description]>
    work:
    - <@[work_datetime]@>
  <[datetime]>:
    here:
      version: <[active:.version]>
    test:
    description: >
      <[description]>
    work:
      - <@[work_datetime]@>
'''
#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@||

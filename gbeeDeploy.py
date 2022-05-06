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
import gravitybee
#===============================================================================||
args = gravitybee.Arguments(src_dir="src", extra_data=["gbextradata"],
							pkg_dir=os.path.join("tests", "gbtestapp"),
							clean=True)
pg = gravitybee.PackageGenerator(args)
pg.generate()
# show path (and name) of standalone app
print("The standalone app: ", pg.gen_file_w_path)
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

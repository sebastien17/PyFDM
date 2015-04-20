#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyfdm import fdmexec
JSBSIM_ROOT = os.path.abspath('data/jsbsim_data') + os.sep


#Load
fdm = fdmexec.FGFDMExec(root_dir=JSBSIM_ROOT)
fdm.load_model("FG_c172p")

fdm.set_property_value("fcs/mixture-cmd-norm",1.0)
fdm.set_property_value("propulsion/magneto_cmd",3)
fdm.set_property_value("propulsion/starter_cmd",1)
      
fdm.set_property_value("ic/lat-gc-rad",0.761552988)
fdm.set_property_value("ic/long-gc-rad",0.0239284344)
fdm.set_property_value("ic/h-agl-ft",1000)
fdm.set_property_value("ic/vc-kts",80)
fdm.set_property_value("ic/gamma-deg",0)
fdm.do_trim(1)

fdm.realtime(max_time = 5.0, verbose = False)

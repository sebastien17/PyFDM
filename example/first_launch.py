#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyfdm import fdmexec

JSBSIM_ROOT = os.path.abspath('../jsbsim/') + os.sep


#Load
fdm = fdmexec.FGFDMExec(root_dir=JSBSIM_ROOT)
fdm.load_model("f16")

# trim
fdm.set_property_value("ic/h-agl-ft",1000)
fdm.set_property_value("ic/vc-kts",400)
fdm.set_property_value("ic/gamma-deg",0)
fdm.do_trim(0)

# simulate
#(t,y) = fdm.simulate(t_final=10,dt=0.1,record_properties=["position/h-agl-ft", "attitude/theta-deg"])
#print(t,y)
fdm.print_property_catalog()
fdm.realtime(input_properties = [], output_properties = [], dt=0.01, max_time = 0.1, verbose = False)   

#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyfdm import fdmexec

JSBSIM_ROOT = os.path.abspath('./data/jsbsim_data') + os.sep
print('JSBSIM_PATH : ' + JSBSIM_ROOT)

#Load
fdm = fdmexec.FGFDMExec(root_dir=JSBSIM_ROOT)
fdm.load_model("f16")

fdm.print_property_catalog()
  

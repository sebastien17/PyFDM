#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
from pyfdm import fdmexec

JSBSIM_ROOT = os.path.abspath('../jsbsim/') + os.sep


#Load
fdm = fdmexec.FGFDMExec(root_dir=JSBSIM_ROOT)
fdm.load_model("f16")

fdm.print_property_catalog()
  

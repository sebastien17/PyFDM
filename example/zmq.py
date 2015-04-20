
# coding: utf-8

# In[1]:

import os
from pyfdm import fdmexec
JSBSIM_ROOT = os.path.abspath('../data/jsbsim_data') + os.sep


#Load
fdm = fdmexec.FGFDMExec(root_dir=JSBSIM_ROOT)
fdm.load_model("FG_c172p")


# In[10]:

fdm._zmq_in_suscribe(['ic/lat-gyc-rad','ic/long-gc-rad'])


# In[11]:

fdm._zmq_in_suscribe_list()


# In[12]:

fdm._zmq_in_get()


# In[ ]:




# In[ ]:




# In[ ]:




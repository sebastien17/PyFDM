=====
PyFDM
=====

Python Wrapper for JSBsim with:

* ZMQ based exchange class for I/O
* Realtime capacities

Original Code from : `pyjsbsim <https://github.com/arktools/pyjsbsim>`

JSBSim Flight Dynamics Model code from : `Sourceforge <http://sourceforge.net/projects/jsbsim/>`

How to compile jsbsim (MinGW)
-----------------------------

CMake for Windows : http://www.cmake.org/cmake/resources/software.html

.. code-block:: bash

  cd <jsbsim_root>
  mkdir build_mingw
  cd build_mingw
  cmake -G "MinGW Makefiles" -DBUILD_SHARED_LIBS=TRUE -DJSBSIM_ENABLE_PLUGINS=TRUE ..
  mingw32-make
  copy dll in path

How to use it
-------------  
  
.. code-block:: python
  
	import os, time
	from pyfdm import fdmexec
	from pyfdm.exchange import zmq_exchange
	
	#Setting JSBSIM_ROOT path
	JSBSIM_ROOT = os.path.abspath('data/jsbsim_data') + os.sep
	
	#Initializing FGFDMExec class
	fdm = fdmexec.FGFDMExec(root_dir=JSBSIM_ROOT)
	
	#Loading aircraft model
	fdm.load_model("FG_c172p")
	
	#Initializing Aircraft
	fdm.set_property_value("fcs/mixture-cmd-norm",1.0)
	fdm.set_property_value("propulsion/magneto_cmd",3)
	fdm.set_property_value("propulsion/starter_cmd",1)
	fdm.set_property_value("ic/lat-gc-rad",0.761552988)
	fdm.set_property_value("ic/long-gc-rad",0.0239284344)
	fdm.set_property_value("ic/h-agl-ft",1000)
	fdm.set_property_value("ic/vc-kts",80)
	fdm.set_property_value("ic/gamma-deg",0)
	#Trim
	fdm.do_trim(1)
	
	#Defining parameters
	_IN = ['fcs/aileron-cmd-norm',
	'fcs/elevator-cmd-norm',
	'fcs/rudder-cmd-norm',
	'fcs/flap-cmd-norm',
	'fcs/speedbrake-cmd-norm',
	'fcs/spoiler-cmd-norm',
	'fcs/pitch-trim-cmd-norm',
	'fcs/roll-trim-cmd-norm',
	'fcs/yaw-trim-cmd-norm',
	'fcs/left-brake-cmd-norm',
	'fcs/right-brake-cmd-norm',
	'fcs/steer-cmd-norm',
	'fcs/throttle-cmd-norm',
	'fcs/mixture-cmd-norm']
	
	_OUT = ['position/h-sl-ft',
	'position/h-sl-meters',
	'position/lat-gc-rad',
	'position/long-gc-rad',
	'position/lat-gc-deg',
	'position/long-gc-deg',
	'position/h-agl-ft',
	'position/h-agl-km',
	'position/terrain-elevation-asl-ft']
	
	#Defining zmq exchange parameters
	zmq_tool = zmq_exchange(_IN,_OUT ,'tcp://127.0.0.1:17171','tcp://localhost:17172' )
	
	#Registering exchange instance to FGFDMExec instance
	fdm.exchange_register(zmq_tool)
	
	#List of exchange instance registered
	fdm.list_exchange_class()
	
	#Running FDM loop
	fdm.realtime(dt=1.0/100)

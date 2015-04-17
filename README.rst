=====
PyFDM
=====

Python Wrapper for JSBsim

Original Code from : `pyjsbsim <https://github.com/arktools/pyjsbsim>`

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

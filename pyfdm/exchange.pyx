#	-*- coding: utf-8 -*-

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%
#	This file is part of PyFDM.

#	PyFDM is free software: you can redistribute it and/or modify
#	it under the terms of the GNU General Public License as published by
#	the Free Software Foundation, either version 3 of the License, or
#	(at your option) any later version.

#	PyFDM is distributed in the hope that it will be useful,
#	but WITHOUT ANY WARRANTY; without even the implied warranty of
#	MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#	GNU General Public License for more details.

#	You should have received a copy of the GNU General Public License
#	along with PyFDM.  If not, see <http://www.gnu.org/licenses/>.
#	%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%

from cpython.ref cimport PyObject
from libcpp cimport bool, float, int
from libcpp.string cimport string
from libcpp.vector cimport vector
import zmq 
import threading

#Threading decorator definition
def in_thread(isDaemon = True):
    def base_in_thread(fn):
        '''Decorator to create a threaded function '''
        def wrapper(*args, **kwargs):
            t = threading.Thread(target=fn, args=args, kwargs=kwargs)
            t.setDaemon(isDaemon)
            t.start()
            return t
        return wrapper
    return base_in_thread


cdef class zmq_exchange(object):
    cdef object _zmq_context
    cdef object _zmq_socket
    cdef bool _running
    cdef bool _direction            #1 = GET 0 = SET
    cdef PyObject* _get_function
    cdef PyObject* _set_function
    cdef vector[string] _param_list
    cdef vector[float] _values
    cdef vector[float] _tmp_values

    def __cinit__(self, list, direction ='OUT' , zmq_address ='tcp://localhost:17171'):
        print('Zmq_Exchange Init')
        self._zmq_context = zmq.Context()
        self._running = True
        self._param_list = [_str.encode('utf-8') for _str in list]
        if (direction == 'IN'):
            self._direction = False
            self._zmq_socket = self._zmq_context.socket(zmq.SUB)
            self._zmq_socket.connect(zmq_address)
            self._zmq_socket.setsockopt(zmq.SUBSCRIBE, '')
            self._set_loop()
        else:
            self._direction = True
            self._zmq_socket = self._zmq_context.socket(zmq.PUB)
            self._zmq_socket.connect(zmq_address)
        #All is ready we register into the FDM class

    def direction(self):
        return self._direction
    def list(self):
        return self._param_list
    def  get(self, vector[float] values):
        print(' '.join([str(f) for f in values]))
        self._zmq_socket.send_string(' '.join([str(f) for f in values]))
        return
    def set(self, vector[float] values):
        cdef vector[float] vector_null
        if(self._values.size() == self._param_list.size()):
            return self._values
        else:
            return vector_null
    @in_thread()
    def  _set_loop(self):
        cdef string _string
        cdef vector[string] _tmp
        cdef string _s
        while(self._running):
            _string = self._zmq_socket.recv_string()
            _tmp = _string.split('')
            self._tmp_values = [float(_s) for _s in _tmp]
            #Is this one tick ?
            self._values = self._tmp_values

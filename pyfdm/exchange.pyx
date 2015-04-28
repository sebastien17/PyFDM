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
from zmq.eventloop import ioloop, zmqstream
ioloop.install()

cdef class zmq_exchange(object):
    cdef object fdm_class
    cdef object _zmq_context
    cdef object _socket_out
    cdef object _socket_in
    cdef vector[string] _list_in
    cdef vector[string] _list_out
    
    def __init__(self, list_in,  list_out, zmq_address_in, zmq_address_out):
 
        self._zmq_context = zmq.Context()
        self._list_in = [_str.encode('utf-8') for _str in list_in]
        self._list_out = [_str.encode('utf-8') for _str in list_out]
        if( not self._list_in.empty()):
            self._socket_in = self._zmq_context.socket(zmq.SUB)
            self._socket_in.setsockopt(zmq.CONFLATE, 1)             #Has to be set up before bind/connect
            self._socket_in.connect(zmq_address_in.encode('utf-8'))
            self._socket_in.setsockopt_string(zmq.SUBSCRIBE, '')
        if( not self._list_out.empty()):
            self._socket_out = self._zmq_context.socket(zmq.PUB)
            self._socket_out.connect(zmq_address_out.encode('utf-8'))
    def register(self, fdm_class):
        self.fdm_class = fdm_class
    def list_in(self):
        return self._list_in
    def list_out(self):
        return self._list_out
    def set(self):
        cdef vector[float] _tmp_values
        try:
            _data = self._socket_in.recv(flags=zmq.NOBLOCK).decode('utf-8')
        except Exception as inst:
           _tmp_values = []
        else:
            _tmp_values = [float(_str) for _str in _data.split(' ')]
            if(_tmp_values.size() != self._list_in.size()):
                _tmp_values = []
        finally:
            return _tmp_values
    def get(self, vector[float] values):
        self._socket_out.send_string(' '.join([str(f) for f in values]))

            

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
    cdef object _stream_sub
    cdef object _socket_out
    
    cdef vector[string] _list_in
    cdef vector[string] _list_out
    cdef vector[float] _values_in
    
    def __init__(self, list_in,  list_out, zmq_address_in, zmq_address_out):
        cdef object _socket_in 
        self._zmq_context = zmq.Context()
        self._list_in = [_str.encode('utf-8') for _str in list_in]
        self._list_out = [_str.encode('utf-8') for _str in list_out]
        if( not self._list_in.empty()):
            _socket_in = self._zmq_context.socket(zmq.SUB)
            _socket_in.connect(zmq_address_in.encode('utf-8'))
            _socket_in.setsockopt_string(zmq.SUBSCRIBE, '')
            self._stream_sub = zmqstream.ZMQStream(_socket_in)
            self._stream_sub.on_recv(self._process_message)
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
        return self._values_in
    def get(self, vector[float] values):
        self._socket_out.send_string(' '.join([str(f) for f in values]))
    def _process_message(self, msg):
        self._values_in = [float(_str) for _str in msg]

            


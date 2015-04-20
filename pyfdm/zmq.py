#!/usr/bin/env python
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

import zmq as _zmq
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

class exchange (object):
    def __init__(self, _fdmexec):
        self._zmq_context = _zmq.Context()
        self.fdmexec = _fdmexec
        self._running = True
        self._thread_list = []

    def new_in(self, zmq_sock_in, list = None):
        if(list== None):
            return False
        socket_in = self._zmq_context.socket(_zmq.SUB)
        socket_in.bind(zmq_sock_in)
        socket_in.setsockopt(_zmq.SUBSCRIBE, '')
        self.fdmexec.exchange_set_suscribe(list)
        self._thread_list.append(self._in_tmp)
        return True
     
    def new_out(self, zmq_sock_out, list = None):
        if(list== None):
            return False
        socket_in = self._zmq_context.socket(_zmq.PUB)
        socket_in.bind(zmq_sock_out)
        self.fdmexec.exchange_get_suscribe(list)
        self._thread_list.append(self._out_tmp)
        return True
        
    @in_thread(True)
    def _in_tmp(self,socket_in):
        while(self._running):
            string = socket_in.recv()
            tmp = string.split('')
            self.fdmexec.exchange_set_value_list(tmp)
            
    @in_thread(True)
    def _out_tmp(self,socket_out):
        while(self._running):
            tmp = self.fdmexec._exchange_get_value_list()
            socket_out.recv(' '.join(tmp))

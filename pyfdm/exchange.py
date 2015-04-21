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

class zmq_exchange(object):
    def __init__(self, _fdmexec):
        print('Zmq_Exchange Init')
        self._zmq_context = zmq.Context()
        self.fdmexec = _fdmexec
        self._running = True
        self._thread_list = []

    def new_in(self, zmq_sock_in, list = None):
        if(list== None):
            return False
        socket = self._zmq_context.socket(zmq.SUB)
        socket.connect(zmq_sock_in)
        socket.setsockopt(zmq.SUBSCRIBE, '')
        self.fdmexec.exchange_set_suscribe(list)
        self._thread_list.append(self._in_tmp(socket))
        return True
     
    def new_out(self, zmq_sock_out, list = None):
        if(list== None):
            return False
        print('Zmq_Exchange New Out Init')
        socket = self._zmq_context.socket(zmq.PUB)
        socket.connect(zmq_sock_out)
        self.fdmexec.exchange_get_suscribe(list)
        self._thread_list.append(self._out_tmp(socket))
        return True
        
    @in_thread(True)
    def _in_tmp(self,socket):
        while(self._running):
            string = socket.recv_string()
            tmp = string.split('')
            self.fdmexec.exchange_set_value_list(tmp)
            
    @in_thread(True)
    def _out_tmp(self,socket):
        while(self._running):
            tmp = self.fdmexec.exchange_get_value_list()
            socket.send_string(' '.join([str(f) for f in tmp]))

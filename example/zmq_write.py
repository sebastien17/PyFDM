#!/usr/bin/env python
#	-*- coding: utf-8 -*-

import zmq, time

_PORT = 'tcp://127.0.0.1:17171'

if(__name__ == '__main__'):
    _context = zmq.Context()
    socket = _context.socket(zmq.PUB)
    socket.bind(_PORT)
    _IN = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
    while(True):
        _bytes = ' '.join( ['0.0' for i in range(14)]).encode('utf-8')
        socket.send(_bytes)
        print(_bytes)
        time.sleep(0.00001)

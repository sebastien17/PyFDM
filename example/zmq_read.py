#!/usr/bin/env python
#	-*- coding: utf-8 -*-

import zmq

_PORT = 'tcp://*:23123'

if(__name__ == '__main__'):
    _context = zmq.Context()
    socket = _context.socket(zmq.SUB)
    socket.bind(_PORT)
    socket.setsockopt(zmq.SUBSCRIBE, ''.encode())
    while(True):
        string = socket.recv()
        print(string)

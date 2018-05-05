'''
Created on 4 maj 2018

@author: arazu
'''
import socket
from Lib.test.test_getopt import sentinel

class MySocket:
    
    def __init__(self, sock=None):
        if sock is None:
            self.sock = socket.socket(
                socket.AF_INET,
                socket.SOCK_DGRAM)
        else:
            self.sock = sock
    
    def connect(self, host, port):
        self.sock.connect((host, port))
    
    def mysend(self, msg):
        totalsent = 0
        while totalsent < MSGLEN:
            sent = self.sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("socket conntction failure")
            totalsent = totalsent + sent
            
    def myreceive(self):
        chunks = []
        bytes_recv = 0
        while bytes_recv < MSGLEN:
            chunk = self.sock.recv(min(MSGLEN - bytes_recv, 2048))
            if chunk == b'':
                raise RuntimeError("socket connection broken")
            chunks.append(chunk)
            bytes_recv = bytes_recv + len(chunk)
        return b''.join(chunks)
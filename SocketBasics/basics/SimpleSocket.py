'''
Created on 3 maj 2018

@author: arazu
'''
import socket

serv = ('localhost', 10000)

s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

s.bind(serv)

while True:
    data, addr = s.recvfrom(1024)
    msg = data.decode()
    print(msg)
    

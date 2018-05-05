'''
Created on 4 maj 2018

@author: arazu
'''
import socket

msg = "hello there!"
serv = ("127.0.0.1", 10000)

client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

client.sendto(msg.encode(encoding='utf_8', errors='strict'), ("127.0.0.1", 10000))

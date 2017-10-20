import socket
import os
import struct
from ctypes import*

#host do nasluchiwania
host = "192.168.0.11"

#naglowek ip
class IP(Structure):

    _fields_ = [
        ("ihl",           c_ubyte, 4),
        ("version",       c_ubyte, 4),
        ("tos",           c_ubyte),
        ("len",           c_ushort),
        ("id",            c_ushort),
        ("offset",        c_ushort),
        ("ttl",           c_ubyte),
        ("protocol_num",  c_ubyte),
        ("sum",           c_ushort),
        ("src",           c_ulong),
        ("dst",           c_ulong)
    ]

    #surowy buffor tego co dostaniemy z sieci
    def __new__(self, socket_buffer = None):
        return self.from_buffer_copy(socket_buffer)

    def __init__(self, socket_buffer = None):
        #mapowanie stalych protokolowa na ich nazwy
        self.protocol_map = {1:"ICMP", 6:"TCP", 17:"UDP"}

        #adresy ip czytelne dla czlowieka
        self.src_address = socket.inet_ntoa(struct.pack("<L",self.src))
        self.dst_address = socket.inet_ntoa(struct.pack("<L",self.dst))

        #protokol czytelny dla czlowieka
        try:
            self.protocol = self.protocol_map[self.protocol_num]
        except:
            self.protocol = str(self.protocol_num)

#to powinno wygladac znajomo

if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host,0))
sniffer.setsockopt(socket.IPPROTO_IP,socket.IP_HDRINCL,1)

if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

try:
    while True:

        #wczytanie jednego pakietu
        raw_buffer = sniffer.recvfrom(65565)[0]

        #utworzenie naglowka IP z 20 pierwszych bajtow z bufora
        ip_header = IP(raw_buffer[0:32])

        #wydruk wykrytego protokolu i hostow
        print "protokol: %s %s => %s" % (ip_header.protocol,
                                         ip_header.src_address,
                                         ip_header.dst_address)

        #obsluga kombinacji klawiszy ctrl+c
except KeyboardInterrupt:
    #jesli uzywany jest system windows, wylaczamy tryb nieograniczony
    if os.name == "nt":
        sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

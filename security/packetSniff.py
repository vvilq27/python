import socket
import os

#host do nasluchiwania
host = "192.168.0.0"

#utworzenie surowego gniazda i powiazanie go z interfejsem publicznym
if os.name == "nt":
    socket_protocol = socket.IPPROTO_IP
else:
    socket_protocol = socket.IPPROTO_ICMP

sniffer = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket_protocol)
sniffer.bind((host, 0))

#przechytujemy tez naglowki ip
sniffer.setsockopt(socket.IPPROTO_IP, socket.IP_HDRINCL, 1)

#jesli uzywamy systemu windows tomusimywysylac wywolanie IOCTL, aby wlaczyc tryb nieograniczony
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_ON)

#wczytanie pojedynczeko pakietu
print sniffer.recvfrom(65565)

#jesli uzywany jest system wind wylaczamy tryb nieograniczony
if os.name == "nt":
    sniffer.ioctl(socket.SIO_RCVALL, socket.RCVALL_OFF)

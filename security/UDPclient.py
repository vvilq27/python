import socket

target_host = "127.0.0.1"
target_port = 80

#utworzenie gniazda
client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

#wyslanie danych
client.sendto("AAABBBCCC", (target_host,target_port))

#odebranie danych
data, addr = client.recvfrom(4096)

print(data)
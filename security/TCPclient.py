import socket

target_host = "0.0.0.0"
target_port = 9999

#gniazdo
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#polaczenie z clientem
client.connect((target_host,target_port))

#wyslanie danych
client.send("aaa gowno wgowno") #GET / HTTP/1.1\r\nHost: google.com\r\n\r\n")

#odebranie danych
response = client.recv(4096)

print(response)
import socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

server = "145.239.82.215"


def pscan(port):
    try:
        s.connect(server, port)
        return True
    except:
        return False
    


for x in range(1000, 2000):
    if pscan(x):
        print('Port ',x,' is open')
    else:
        print('Port ', x, ' is closed')
import sys
import socket
import threading

# te zmienne (local_host...) przekazywane sa jako parametry przy wywolaniu programu
def server_loop(local_host, local_port, remote_host, remote_port, receive_first):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        # oczekiwanie na polaczenia
        server.bind((local_host,local_port))

    except:
        print"[!!] nieudanaproba nasluchu na portcie %s:%d" %(local_host,local_port)
        print"[!!] poszukaj innego gniazda lub zdobadz odpowiednie uprawnienia"
        sys.exit(0)
        print "[*] nasluchiwanie na porcie %s:%d" %(local_host,local_port)

        #zbieranie do 5 polaczen
        server.listen(5)

        while True:
            #akceptuj polaczenia z zewnatrz => client.connect(..)
            client_socket, addr = server.accept() #nie wyskoczylo uzupelnienie !!

            #wydruk informacji o polaczeniu lokalnym
            print "[==>] otrzymano polaczenie przychodzace od %s:%d" %(addr[0],addr[1])

            #uruchomienie watku do wspolpracy ze zdalnym hostem
            proxy_thread = threading.Thread(target = proxy_handler, args = (client_socket,
                                                                            remote_host,
                                                                            remote_port,
                                                                           receive_first))
            proxy_thread.start()


def proxy_handler(client_socket, remote_host, remote_port, receive_first) :
    #polaczenie ze zdalnym hostem
    remote_socket = socket.socket(socket.AF_INET,
                                  socket.SOCK_STREAM)
    remote_socket.connect((remote_host,
                           remote_port))

    #odebranie danych od zdalnegohosta w razie potrzeby
    if receive_first:
        remote_buffer = receive_from(remote_socket)
        hexdump(remote_buffer)

        #wyslanie danych do procedury obslugi odpowiedzi
        remote_buffer = response_handler(remote_buffer)

        #jesli mamy dane do wyslania doklenta lokalnego to je wysylamy
        if len(remote_buffer):
            print "<== wyslanie %d baltow do localhost." % len(remote_buffer)
            client_socket.send(remote_buffer)

    #uruchamiamy pelte w ktorej odczytujemy dane z hosta lokalnego
    #wysylamy dane do hosta zdalnego wysylamy dane do hosta lokalnego
    #wszystko powtarzamy
    while True:
        #odczyt z lokalnego hosta
        local_buffer = receive_from(client_socket)

        if len(local_buffer):
            print "==> odebrano %d bajtow od localhost." %len(local_buffer)
            hexdump(local_buffer)

            #wysylanie danych do procedury obslugi zadan
            local_buffer = request_handler(local_buffer)

            #przeslanie danych do zdalnego hosta
            remote_socket.send(local_buffer)
            print "==> wyslano do zdalnego hosta."

            #odebranie odpowiedzi
            remote_buffer = receive_from(remote_socket)

            if len(remote_buffer):
                print "<== odebrano %d bajtow od zdalnego hosta" % len(remote_buffer)
                hexdump(remote_buffer)

            #wyslanie danych do procedury obslugi odpowiedzi
            remote_buffer = response_handler(remote_buffer)

            #wyslanie odpowiedzi do lokalnego gniazda
            client_socket.send(remote_buffer)

            print "<== wyslano do localhost."

        #jesli nie ma wiecej danych po zadnej ze stron zamykamy polaczenia

        if not len(local_buffer) or not len(remote_buffer):
            client_socket.close()
            remote_socket.close()
            print "[*] nie ma wiecej danych. zamykanie polaczen"

            break


#jest to elegancka funkcja do robienia zrzutow szesnastkowych wydobyta wprost
#z komentarzy na stronie...
def hexdump(src, length = 16):
    result = []
    digits = 4 if isinstance(src, unicode) else 2
    for i in xrange(0, len(src), length):
        s = src[i:i+length]
        hexa = b' '.join("%0*X" % (digits, ord(x)) for x in s)
        text = b''.join([x if 0x20 <= ord(x) <0x7F else b'.' for x in s])
        result.append( b"%04X %-*s %s" % (i,length*(digits + 1), hexa, test))

    print b'\n'.join(result)

#pobiera jako parametr obiekt gniazda, zwraca dane z polaczenia
def receive_from(connection):
    buffer = ""

    #ustawiamy 2-sekundowy limit czasu w niektorych przypadkach moze byc konieczna
    #zmiana tej wartosci

    connection.setimeout(2)

    try:
    #wczytujemy dane do bufora az wyczytamy wszystkie albo skonczy sie czas
        while True:
            data = connection.recv(4096)
            if not data:
                break
        buffer += data
    except:
        pass
        return buffer


#modyfikujemy zadania przeznaczone dla zdalnego hosta
def request_handler(buffer):
    #modyfikujemy pakiety
    return buffer


#modyfikujemy odpowiedzi przeznaczone dla lokalnego hosta
def response_handler(buffer):
    #modyfikujemy pakiety
    return buffer


def main():

    #musi byc 5 parametrow w wywolaniu i to tu sprawdzamy
    if len(sys.argv[1:]) != 5:
        print "sposob uzycia : ./TCPproxy.py [localhost] [localport] [remothost] [remoteport] [receive_first"
        print "przykla: ./proxy.py 127.0.01 9000 10.12.132.1 9000 True"
        sys.exit(0)

    #konfiguracja lokalnych parametrow nasluchu
    local_host= sys.argv[1]
    local_port = int(sys.argv[2])

    #ustawienie zdalnego celu
    remote_host = sys.argv[3]
    remote_port = int(sys.argv[4])

    #nakazujemy proxy nawiazanie polaczenia i odebranie danych
    #przed wyslaniem danych do zdalnego hosta
    receive_first = sys.argv[5]

    if "True" in receive_first:
        receive_first = True
    else:
        receive_first = False

    #wlaczamy gniazdo do nasluchu
    #dokonuje polaczenia i tworzy watki z tych polaczen
    server_loop(local_host,local_port,remote_host,remote_port,receive_first)

main()




























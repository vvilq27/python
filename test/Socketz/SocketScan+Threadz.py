import socket
import threading
from queue import Queue

print_lock = threading.Lock()

target = "https://pythonprogramming.net"

def portscan(port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        con = s.connect((target,port))
        with print_lock:
            print('port ', port,' is open')
        con.close()
    except:
        pass
    
def threader():
    while True:
        portNum = q.get()  #from here threads get ports number to scan
        portscan(portNum)
        q.task_done()
        
q = Queue()

for x in range(30):
    t = threading.Thread(target=threader()) #makes 30 threads that will wait for numbers in queue in threader method
    t.deamon = True
    t.start()
    
for portNumberToScan in range(1,2000):
    q.put(portNumberToScan) #here i put port numbers from 1-100 in queue, so later threads will pick them up and scan those port numbers
    
q.join() # waits  for threads to terminate

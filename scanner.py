from os import name
import socket
from queue import Queue
import threading
import time

socket.setdefaulttimeout(0.6)  #if there is no response in 0.6 seconds than move on
print_lock = threading.Lock()  #to pront threads in the right order
q = Queue()

#def to scan ports
def my_scanner(host,port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)   #creating a socket
    try:
        connection = s.connect((host, port))  #trying to connect
        with print_lock:
            print(f'Port {port} is open!')   #notifiyng the user if the port is open

        connection.close()    #closing the connection
    except:
        pass

#def that creates threads
def threader(host):   
    while True:   
        port_to_scan = q.get()
        my_scanner(host, port_to_scan)
        q.task_done()

def main():
    target = input('Enter ip or domain: ')   #we ask user to enter the domain for example 'pythonprogramming.net'
    host = socket.gethostbyname(target)    #socket function that gets host by the name
    threads = 50 #amount of threads, can be changed 
    amount_of_ports = 2**10  #amount of ports to scan, also can be changed
    start_time = time.time()
    for _ in range(threads):
        t = threading.Thread(target=threader, args=(host,))  #creating a thread 
        t.daemon = True   #all the children dies with the main thread  
        t.start()

    for port in range(1,amount_of_ports):
        q.put(port)

    q.join()

    totalrun = float('%0.2f' %(time.time() - start_time))
    print(f'Total run is {totalrun}')

if __name__=='__main__':
    main()
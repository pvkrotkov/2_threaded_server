import socket
import re
from threading import Thread, Lock
from queue import Queue


def get_host():
    while True:
        host = input('Enter host IP: ')
        if re.match(r'^(\d{1,3}\.){3}\d{1,3}$', host):
            return host
        else:
            print('Invalid IP, try again!')


def port_scanner(port, host):
    global print_lock
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except:
        pass
    else:
        with print_lock:
            print("port", port, "is open")
    # except ConnectionRefusedError:
    #     print(f'port {port} is closed')
    #     continue
    # except TimeoutError:
    #     print(f'Unreacheable host {host}')
    #     break
    finally:
        sock.close()


def scan_thread(host):
    global ports_queue

    while True:
        current_port = ports_queue.get()
        port_scanner(current_port, host)
        ports_queue.task_done()

    
def main(host, ports):
    global ports_queue
    for port_number in ports:
        ports_queue.put(port_number)
    for _ in range(TREADS_NUMBER):
        Thread(target=scan_thread, args = [host], daemon = True).start()

    ports_queue.join()



# host = get_host()
host = '192.168.1.39'
PORTS_COUNT = 2**16
TREADS_NUMBER = 10000
ports_queue = Queue()
print_lock = Lock()
ports_list = [i for i in range(PORTS_COUNT)]
main(host, ports_list)
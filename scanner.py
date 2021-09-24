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
    global print_lock, open_ports, locked_ports, forbidden_access_method_ports
    sock = socket.socket()
    try:
        sock.connect((host, port))
    except ConnectionRefusedError:
        with print_lock:
            locked_ports.append(port)

    except TimeoutError as err:
        with print_lock:
            if '10060' in str(err):
                print('unreachable host!', host)
            else:
                raise 

    except OSError as err:
        with print_lock:
            if '10055' in str(err):
                print('Too much daemons, set daemon count fewer!')
            elif '10013' in str(err):
                forbidden_access_method_ports.append(port)
            else:
                raise


    #10055 слишком много потоков, буфер переполнился все упадет в ошибку
    #10013 не тот метод доступа
    #10060 не получен нужный отклик за требуемое время

    else:
        with print_lock:
            open_ports.append(port)
    finally:
        sock.close()


def scan_thread(host):
    global ports_queue

    while True:
        current_port = ports_queue.get()
        port_scanner(current_port, host)
        ports_queue.task_done()


def printProgressBar(iteration, total, prefix = '', suffix = '', decimals = 1, length = 100, fill = '█', printEnd = "\r"):
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end = printEnd)
    if iteration == total: 
        print()


def progress_bar():
    global PORTS_COUNT, START_PORT, ports_queue
    while True:
        total = PORTS_COUNT-START_PORT
        cnt = ports_queue.qsize()
        processed = total - cnt
        printProgressBar(processed, total, ' Scanning:', length = 70)
        if not cnt:
            break
    

def scanning(host, ports):
    global ports_queue, TREADS_NUMBER

    for port_number in ports_list:
        ports_queue.put(port_number)

    Thread(target=progress_bar, daemon = True).start()

    for _ in range(TREADS_NUMBER):
        Thread(target=scan_thread, args = [host], daemon = True).start()

    ports_queue.join()   




# host = get_host()
host = '192.168.1.39'
PORTS_COUNT = 2**16
START_PORT = 1
TREADS_NUMBER = 15000
ports_queue = Queue()
print_lock = Lock()
ports_list = [i for i in range(START_PORT,PORTS_COUNT)]
open_ports = []
locked_ports = []
forbidden_access_method_ports = []

scanning(host, ports_list)

open_ports.sort()
locked_ports.sort()
forbidden_access_method_ports.sort()
print('Open ports:', '; '.join([str(i) for i in open_ports]))
import socket
import threading
address = input("Type ip-address to check ports: ")
opened_ports = list()
closed_ports = list()
threads_number = int(input("Enter number of threads to use: "))
ports = int(input("Enter number of ports to check: "))

def check_port(port):
    global opened_ports
    global closed_ports
    global address
    sock = socket.socket()
    try:
        sock.connect((address, port))
    except Exception:
        closed_ports.append(port)
        # print(f"{port} is closed")
    else:
        opened_ports.append(port)
        # print(f"{port} is opened")
        sock.close()


i = 1
for port_heap in range(threads_number + 1, ports, threads_number):
    threads = [threading.Thread(target=check_port, args=[port]) for port in range(i, port_heap)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    i = port_heap
if ports % threads_number != 0:
    threads = [threading.Thread(target=check_port, args=[port]) for port in range(ports - (ports % threads_number) + 1, ports)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]


print(*sorted(opened_ports))

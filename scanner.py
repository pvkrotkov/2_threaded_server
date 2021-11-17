import socket
import threading 
import pyprind

N = 2**16 - 1
address = input('Введите адрес: ')
ports = []
progress_bar = pyprind.ProgBar(N)
def scanner(ip, port):
    global ports
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.settimeout(.5)
    try:
        sock.connect((ip, port))
        ports.append(port)
        sock.close()
    except:
        pass
for port in range(N):
    if port in ports:
        continue
    thread = threading.Thread(target=scanner, args=(address, port))
    thread.start()
    progress_bar.update()

print('Список открытых портов:', ports)

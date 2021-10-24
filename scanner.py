import socket, time
from threading import Thread


N = 2**16 - 1
sock = socket.socket()



def progress():
    progress = 0
    percent = 100 / N
    for i in range(1, N):
        progress += percent
        print('\rОбработка файлов завершена на %3d%%' % progress, end='', flush=True)
        time.sleep(.00001)

def scann(sock):
    ip = input('Write the ip >>> ')
    if ip == '':
        ip = '127.0.0.1'
    progress()
    for port in range(1, N):
        try:
            sock.connect((ip, port))
            time.sleep(.0001)
        except:
            print(f'Port {port} is close')
            continue

Thread(target=scann, args=(sock, )).start()
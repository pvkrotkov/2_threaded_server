import socket
from threading import Thread

N = 2**16 - 1
count_n = N//1000+1

def proc(n):
    for port in range(n-999,n):
        sock = socket.socket()
        try:
            sock.connect(('127.0.0.1', port))
            print("Порт", port, "открыт")
        except:
            continue
        finally:
            sock.close()

threads = [Thread(target = proc, args=[(i+1)*1000]) for i in range(count_n)]
[t.start() for t in threads]

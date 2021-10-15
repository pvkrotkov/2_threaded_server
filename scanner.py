import socket, threading


def TCP_connect(ip, port_number, delay, output):
    TCPsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    TCPsock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    TCPsock.settimeout(delay)
    try:
        TCPsock.connect((ip, port_number))
        output[port_number] = "Слушает"
    except:
        output[port_number] = ""


def scan_ports(host_ip, delay):
    # Для одновременного запуска TCP_connect
    threads = []
    # Вывод портов
    output = {}

    # Создание потоков для сканирования портов
    for i in range(10000):
        t = threading.Thread(target=TCP_connect, args=(host_ip, i, delay, output))
        threads.append(t)

    # Начинаем threads
    for i in range(10000):
        threads[i].start()

    # Блокировка основного потока до завершения всех потоков
    for i in range(10000):
        threads[i].join()

    # Печать портов
    for i in range(10000):
        if output[i] == "Слушает":
            print(str(i) + ": " + output[i])


def main():
    host_ip = input("Напишите ip host: ")
    delay = int(input("Сколько секунд socket ждет до timeout: "))
    scan_ports(host_ip, delay)


if __name__ == "__main__":
    main()

# ip = '127.0.0.1'

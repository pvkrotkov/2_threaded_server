import socket
import threading
# Библиотека для прогресс-бара
from time import sleep
from tqdm import tqdm

# Списки для сохранения открытых и закрытых портов
opened_ports = list()
closed_ports = list()

address = input("Type ip-address to check ports: ")
# Вводится количество потоков, которое будет использоваться для работы сканера
threads_number = int(input("Enter number of threads to use: "))

# Вводится диапазон портов через пробел
ports = list(map(int, input("Enter number of ports to check: ").split()))


# Функция для прогресс-бара. Итерация для прогрессбара проходит по количеству куч потоков:
# Куча потоков - количество потоков, которое задал пользователь


def progress():
    global ports
    global threads_number
    for _ in tqdm(range((ports[1] - ports[0])//threads_number)):
        sleep(0.05)

# Функция, которая пробует подключиться к конкретному порту.
# Основана на том, что при неудачном подключении возбуждается ошибка
# Для ускорения работы скрипта поставим ограничение на ожидание подключения 0.5 секунды


def check_port(port):
    global opened_ports
    global closed_ports
    global address
    sock = socket.socket()
    sock.settimeout(0.5)
    try:
        sock.connect((address, port))
    except Exception:
        closed_ports.append(port)
        # print(f"{port} is closed")
    else:
        opened_ports.append(port)
        # print(f"{port} is opened")
        sock.close()

# Создаём потоки кучами, до тех пор, пока не обработаем весь отрезок портов


i = ports[0]
for port_heap in range(threads_number + ports[0], ports[1] + 1, threads_number):
    threads = [threading.Thread(target=check_port, args=[port]) for port in range(i, port_heap + 1)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]
    i = port_heap
if (ports[1] - ports[0]) % threads_number != 0:
    threads = [threading.Thread(target=check_port, args=[port]) for port in range(ports[1] - ((ports[1] - ports[0]) % threads_number) + 1, ports[1] + 1)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

# Запуск потока с прогрессбаром
progress_bar = threading.Thread(target=progress, args=[])
progress_bar.start()
progress_bar.join()

# Вывод открытых потоков в отсортированном виде. Если таковых не нашлось - выводится None.
print("Opened ports: ", end=' ')
print(*sorted(opened_ports) if opened_ports != [] else [None], sep=', ', end='.')

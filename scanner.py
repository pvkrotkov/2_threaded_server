import socket
#модуль для многопоточности
import concurrent.futures
#модуль для progress bar
import tqdm

def scan_port(host, port, progress_bar, ports):
    sock = socket.socket()  #создаем сокет
    sock.settimeout(0.5)
    try:
        sock.connect((host, port)) 
        ports.append(port)
    except:
        pass
    progress_bar.update()


host = input('Введите адрес: ')
start_port = int(input('Введите минимальный порт: '))
end_port = int(input('Введите максимальный порт: '))
thread = int(input('Сколько потоков использовать для сканирования одновременно: '))



open_ports = []     #список открытых портов
progress_bar = tqdm.tqdm(total=end_port-start_port+1)

with concurrent.futures.ThreadPoolExecutor(thread) as executor: #Выражение with используется для создания исполнительного блока экземпляра ThreadPoolExecutor, который будет быстро очищать потоки после выполнения
    futures = []
    for port in range(start_port, end_port+1):
        future = executor.submit(scan_port, host, port, progress_bar, open_ports) #возвращает объект future из futures
        futures.append(future)
    for future in futures:
        future.result()

progress_bar.close()


for port in open_ports:
    print(f'Порт {port} открыт!')

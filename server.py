import socket
import datetime
import threading

print(f"\33[93mServer launched on {datetime.datetime.now().strftime('%A, %d. %B %Y %I:%M%p')}\33[0m")

# Содержит словар с зарегистрированными пользователями
clients = dict()
# Содержит словарь с подключёнными пользователями
connections = dict()

flag = False
# host = socket.gethostbyname(socket.gethostname())
host = "127.0.0.1"
try:
    port = int(input("Enter port number: "))
except Exception:
    port = 9090

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.bind((host, port))
# Указываем максимальное количество подключений. Я поставил 5
sock.listen(5)


def send_message(sock, client_name):
    while True:
        try:
            data = connections[client_name]["socket"].recv(1024)
            msg = data.decode()
        except Exception:
            connections[client_name]["socket"].send("\33[91mIncorrect message!\33[0m".encode())

        if msg == "exit":
            end_time = datetime.datetime.now().strftime('%d %B %Y %I:%M%p')
            print(f"\33[93m{client_name} disconnected on {end_time}\33[0m")
            connections[client_name]["socket"].close()
            del connections[client_name]
            for connection in connections.values():
                connection["socket"].send(f'\33[93m{client_name} disconnected!\33[0m'.encode())
            break

        else:
            print(f"[ \33[93m{datetime.datetime.now().strftime('%d %B %Y %I:%M%p')}"
                  f"\33[0m ] [{connections[client_name]['address']}]  \33[7m{client_name}\33[0m: {msg}")
            for connection in connections.values():
                if connection["socket"] != connections[client_name]["socket"]:
                    connection["socket"].send(f"[ \33[93m{datetime.datetime.now().strftime('%I:%M%p')}"
                                              f"\33[0m ] -- \33[7m{client_name}\33[0m: {msg}".encode())


def authorization(sock, client, address):
    '''
        Функция для авторизации клиента.
        Если клиент не зарегистрирован - ему предлагается зарегистрироваться.
        Если клиент зарегистрирован - программа запрашивает пароль.
        Для простоты будем хранить пароль в исходном виде, без хеширования.
        Программа вместе с сообщением посылает системные коды.
        0001 - успешная авторизация
        0002 - требование ввести пароль
        0003 - требования придумать пароль
    '''
    global clients
    global connections
    name = client.recv(1024)
    name = name.decode()
    while True:
        if name in clients.keys():
            while True:
                client.send("|0002||".encode())
                password = client.recv(1024)
                password = password.decode()

                if password == clients[name]:
                    for connection in connections.values():
                        connection["socket"].send(f'\33[92m{name} connected!\33[0m'.encode())

                    client.send("\33[92m|0001|Welcome back|\33[0m".encode())
                    connections[name] = {"socket": client, "address": address,
                                         "last_in": datetime.datetime.now().strftime('%d %B %Y %I:%M%p')}
                    print(f'\33[92m{name} connected! on {datetime.datetime.now().strftime("%d %B %Y %I:%M%p")}\33[0m')

                    break

                else:
                    client.send("\33[91m|0002|Incorrect password!|\33[0m".encode())
                    continue
            break
        else:
            client.send("\33[92m|0003|Welcome! Enter your password to sign up|\33[0m".encode())
            password = client.recv(1024)
            password = password.decode()
            clients[name] = password
            connections[name] = {"socket": client, "address": address,
                                 "last_in": datetime.datetime.now().strftime('%d %B %Y %I:%M%p')}
            print(f'\33[92m{name} connected! on {datetime.datetime.now().strftime("%d %B %Y %I:%M%p")}\33[0m')

            for connection in connections.values():
                connection["socket"].send(f'\33[92m{name} connected!\33[0m'.encode())

            break
    # Получение количества активных пользователей и строки с их именами
    users = "Users: "
    for client_name in connections.keys():
        users += client_name + ", "
    users = users[:len(users) - 2] + '.'
    client.send(f"\n\33[92mUsers online: {len(connections.keys())}\n{users}\33[0m".encode())

    send_message(sock, name)

    # Функция для подключения с последующей авторизацией


def connected(sock):
    while True:
        client, address = sock.accept()
        if client is not None:
            authorization(sock, client, address)


# Создание пяти потоков
while True:
    threads = [threading.Thread(target=connected, args=[sock]) for _ in range(5)]
    [thread.start() for thread in threads]
    [thread.join() for thread in threads]

# if False:
#     print(f"\33[93mServer turns off on {datetime.datetime.now().strftime('%d %B %Y %I:%M%p')}\33[0m")
#     sock.close()

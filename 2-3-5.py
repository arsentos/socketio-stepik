import socketio
import eventlet

# Степ https://stepik.org/lesson/1210368/step/3?unit=1223619

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

users = []


def print_server_status(users_length):
    if users_length == 0:
        print("Сервер пуст")
    elif users_length == 1:
        print("Пользователь один")
    elif users_length >= 2:
        print("Команда в сборе")


# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ):
    users.append(sid)
    print(f"Клиент {sid} подключился!")
    users_length = len(users)
    print_server_status(users_length)


@sio.event
def disconnect(sid):
    users.remove(sid)
    print(f"Клиент {sid} отключился \n")
    users_length = len(users)
    print_server_status(users_length)


print("Сервер пуст")

# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

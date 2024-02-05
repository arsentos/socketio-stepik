import socketio
import eventlet

# Степ https://stepik.org/lesson/1210367/step/6?unit=1223618

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

users = []


# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ, *args):
    print(args)
    users.append(sid)
    print(f"connect  {sid}")
    print(users)


@sio.event
def disconnect(sid):
    print(f"sid {sid} removed from users")
    users.remove(sid)


@sio.on("get_users_online")
def get_users_online(sid, environ):
    sio.emit("users", to=sid, data={
        "online": len(users),
        "users": users
    })


# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

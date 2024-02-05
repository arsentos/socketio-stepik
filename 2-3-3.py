import socketio
import eventlet

# Степ https://stepik.org/lesson/1210368/step/3?unit=1223619

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

users = []

# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ):
    users.append(sid)
    sio.emit("message", to=sid, data={
        "users": users,
        "online": len(users)
    })


@sio.event
def disconnect(sid):
    users.remove(sid)
    print(f"sid {sid} discconected :(")


# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

import socketio
import eventlet

# Степ https://stepik.org/lesson/1210367/step/8?unit=1223618

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)


# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ):
    sio.emit("message", to=sid, data={"message": "Welcome to the server"})


@sio.event
def disconnect(sid):
    print(f"sid {sid} discconected :(")


# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

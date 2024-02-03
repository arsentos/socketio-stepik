import socketio
import eventlet

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ):
    sio.emit("hello", to=sid, data={"message": "hello socket"})
    print("connect ", sid)

# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)
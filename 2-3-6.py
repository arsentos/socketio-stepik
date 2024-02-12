import socketio
import eventlet
from datetime import datetime
# Степ https://stepik.org/lesson/1210368/step/3?unit=1223619

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

users = {}

# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ):
    users[sid] = {"connected_at": datetime.now()}
    print(f"Клиент {sid} подключился!")



@sio.event
def disconnect(sid):
    time_on_server = datetime.now() - users[sid]["connected_at"]
    print(f"Клиент {sid} отключился, время сессии: {time_on_server}")




# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

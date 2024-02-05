import socketio
import eventlet

# Степ https://stepik.org/lesson/1210367/step/8?unit=1223618

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

user_scores = {}


# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ, *args):
    user_scores[sid] = {"score": 0}
    print(user_scores)


@sio.on("increase")
def increase(sid, data):
    user_scores[sid]["score"] += 1


@sio.on("decrease")
def decrease(sid, data):
    user_scores[sid]["score"] -= 1


@sio.on("get_score")
def get_score(sid, data):
    sio.emit("score", to=sid, data=user_scores[sid])


@sio.event
def disconnect(sid):
    print(user_scores)
    user_scores.pop(sid)
    print(f"sid {sid} removed from users_scores")
    print(user_scores)


# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

import socketio
import eventlet

# Степ https://stepik.org/lesson/1210367/step/6?unit=1223618

# Создаем экземпляр сервера Socket.IO
sio = socketio.Server(cors_allowed_origins='*')

# Создаем WSGI приложение
app = socketio.WSGIApp(sio)

lost_queries = {}


@sio.on("*")
def catch_all(event, sid, data):
    if lost_queries.get(event) is None:
        lost_queries[event] = 1
    else:
        lost_queries[event] += 1


@sio.on("count_queries")
def count_queries(sid, data):
    sio.emit("queries", to=sid, data=lost_queries)


# Обработчик события соединения
@sio.on('connect')
def connect(sid, environ, *args):
    print(args)
    print(f"connect  {sid}")


@sio.event
def disconnect(sid):
    print(f"sid {sid} removed from users")


# Запускаем eventlet WSGI сервер
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

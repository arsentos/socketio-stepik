import socketio
import uvicorn
from fastapi import FastAPI

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)

# создаем счетсик пользователей
users_list = []


@sio.event
async def connect(sid, environ):
    # меняем счетчик пользователей
    users_list.append(sid)
    print(f"Пользователь {sid} подключился")


@sio.event
async def disconnect(sid):
    users_list.remove(sid)
    print(f"Пользователь {sid} отключился")

@app.get("/")
async def get_index():
    # отдаем счетчик пользователей
    return users_list


uvicorn.run(socket_app, host='0.0.0.0', port=80)

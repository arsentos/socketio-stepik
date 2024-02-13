import socketio
import uvicorn
from fastapi import FastAPI

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)

message = {"text": "someone visited over http"}


@sio.event
async def connect(sid, environ):
    print(f"Пользователь {sid} подключился")


@sio.event
async def disconnect(sid):
    print(f"Пользователь {sid} отключился")


@app.get("/")
async def get_index():
    await sio.emit("message", data=message)
    return f"main page"


uvicorn.run(socket_app, host='0.0.0.0', port=80)

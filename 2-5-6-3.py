import socketio
import uvicorn
from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
sio = socketio.AsyncServer(async_mode='asgi')
socket_app = socketio.ASGIApp(sio, app)


class Message(BaseModel):
    message: str


@sio.event
async def connect(sid, environ):
    print(f"Пользователь {sid} подключился")


@sio.event
async def disconnect(sid):
    print(f"Пользователь {sid} отключился")


@app.post("/")
async def post_message(message: Message):
    await sio.emit("message", data=message.message)
    return f"message posted"


uvicorn.run(socket_app, host='0.0.0.0', port=80)

import json
import random
import eventlet
import socketio
import uvicorn
import random
from collections import namedtuple

# https://stepik.org/lesson/1210371/step/1
static_files = { '/': './index.html', '/assets/': "./assets/"}
sio = socketio.Server(cors_allowed_origins='*', async_mode='eventlet')

app = socketio.WSGIApp(sio, static_files=static_files)

Riddle = namedtuple("Riddle", ["riddle", "answer"])
users = {}
riddles = [Riddle("Я летаю, но не птица,\nЛюблю ночью порезвиться.\nДнем я сплю вниз головой,\nТы не встретишься со "
                  "мной.", "летучая мышь"),
           Riddle("У моей игрушки-свинки\nЕсть отверстие на спинке.\nПоложу туда монеты,\nЧтоб купить себе конфеты.",
                  "копилка"),
           Riddle("Не испортишь кашу им,\nБутерброды с ним едим.\nОно для крема пригодится,\nЧтобы тортом насладиться.",
                  "сливочное масло"),
           Riddle("Не вода, а все время течёт,\nНе хулиган, а больно бьёт.", "ток"),
           Riddle("Когда молчишь, он отдыхает,\nСказать захочешь - помогает.", "язык")]

@sio.event
def connect(sid, environ):
    # Тут копия списка, что бы сделать в один файл и не подключать БД
    users[sid] = {"last_riddle": None, "score": 0, "riddles": riddles.copy()}
    print(f"Пользователь {sid} подключился")


@sio.event
def disconnect(sid):
    users.pop(sid)
    print(f"Пользователь {sid} отключился")


@sio.on("next")
def next(sid, data):
    # Перемешиваем вопросы, что бы доставать последний
    random.shuffle(users[sid]["riddles"])
    try:
        riddle = users[sid]["riddles"].pop()
    except IndexError as e:
        sio.emit("over", to=sid)
        return
    users[sid]["last_riddle"] = riddle
    response = {"text": riddle.riddle}
    sio.emit("riddle", data=response, to=sid)

@sio.on("answer")
def answer(sid, data):
    riddle: Riddle = users[sid]["last_riddle"]
    if data["text"].lower() == riddle.answer.lower():
        is_correct = "true"
        users[sid]["score"] += 1
    else:
        is_correct = "false"

    response = {"riddle": riddle.riddle, "is_correct": is_correct, "answer": riddle.answer}
    sio.emit("result", data=response, to=sid)
    score_response = {"value": users[sid]["score"]}
    sio.emit("score", data=score_response, to=sid)

# Создаем экземпляр сервера Socket.IO
eventlet.wsgi.server(eventlet.listen(('', 80)), app)

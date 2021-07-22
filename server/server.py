# Server
import socketio
from fastapi import FastAPI
sio = socketio.AsyncServer(async_mode="asgi", ping_interval=16, logger=True, engineio_logger=True, ping_timeout=4800,)
fast_app = FastAPI()
app = socketio.ASGIApp(sio, fast_app)

users = []
rooms = []


@sio.event
async def connect(sid, data):
    print(f"[SERVER]: connect {sid}")


@sio.event
async def disconnect(sid):
    print(f"[SERVER]: disconnect {sid}")


@sio.event 
async def logger(sid, data):
    if data["event"] == "left_room":
        print(f"{data['user']} left {data['room']}")


@sio.event
async def create_room(sid, data):
    global rooms
    print(f"{data['room_owner']} joined to {data['room_name']}")
    room_data = {"room_name": data['room_name'], "private": data["private"], "password": data["password"], "capacity": data["capacity"], "room_owner": data["room_owner"]}
    rooms.append(room_data)
    sio.enter_room(sid, data['room_name'])
    return room_data


@sio.event
async def join_room(sid, data):
    print(f"{data['username']} joined to {data['room_name']}")
    sio.enter_room(sid, data['room_name'])


@sio.event
async def leave_room(sid, data):
    print(f"{data['username']} left {data['room_name']}")
    sio.leave_room(sid, data['room_name'])


@sio.event
async def send_message(sid, data):
    print(f"[SERVER]: send message {sid}, data: {data}")
    await sio.emit("receive_message", data, room=data["room_name"])


@sio.event
async def receive_message(sid, data):
    print(f"[SERVER]: receive message {sid}, data: {data}")


@sio.event
async def get_rooms(sid):
    room_data = rooms
    print(f"[SERVER]: getting rooms for {sid}.")
    print(room_data)
    return room_data


@sio.event
async def keep_alive(sid):
    print(f"[SERVER]: {sid} pinging server...")
    return "OK"

if __name__ == "__main__":
    web.run_app(app)

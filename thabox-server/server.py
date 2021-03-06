# Server
import socketio
import sqlite3 as sqlite
from os import path



# Configure database...
if not path.exists("users.db"):
    conn = sqlite.connect('users.db')
    cur = conn.cursor()

    print("Database not found in current directory. Setting up new one...")
    conn.execute("""CREATE TABLE users(
    username varchar(255),
    password varchar(255),
    NameColour varchar(255),
    MessageColour varchar(255),
    BorderColour varchar(255),
    MessageBorderColour varchar(255));""")
    conn.commit()
else:
    conn = sqlite.connect('users.db')
    cur = conn.cursor()

# Configure server app
sio = socketio.AsyncServer(async_mode="asgi", ping_interval=30, ping_timeout=4294967)
app = socketio.ASGIApp(sio)



users = []
rooms = []


room_data = {} # {"room_name": list(["room_name", "privacy", "password"])} password is None if privacy is public


@sio.event
async def connect(sid, data):
    print(f"[SERVER]: connect {sid}")


@sio.event
async def disconnect(sid):
    print(f"[SERVER]: disconnect {sid}")


@sio.event
async def create_room(sid, data):
    global rooms
    print(f"{data['room_owner']} joined to {data['room_name']}")
    room_data = {"room_name": data['room_name'], "private": data["private"], "password": data["password"], "capacity": data["capacity"], "room_owner": data["room_owner"]}
    sio.enter_room(sid, data['room_name'])
    return room_data


@sio.event
async def join_room(sid, data):
    global room_data
    request_from = data["sid"]
    if data["room_name"] not in room_data:
        room_data[data["room_name"]] = [data["room_name"], "public", None]
        print(f"{data['username']} joined to {data['room_name']}")
        sio.enter_room(sid, data['room_name'])
        return
    info = room_data.get(data["room_name"])
    if info[1] == "public":
        sio.enter_room(sid, data['room_name'])
        print(f"{data['username']} joined to {data['room_name']}")
        return
    await sio.emit("password_prompt", {"sid": request_from, "password": info[2]})
    
    


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


@sio.event
async def save_user(sid, data):
    username, password, pref_dict = data["username"], data["password"], data["pref_dict"]
    print(username, password, pref_dict)   
    global cur, conn
    cur.execute("INSERT INTO users VALUES" \
     "(:username, :password, :NameColour, :MessageColour, :BorderColour, :MessageBorderColour)",
     {
         "username": username,
         "password": password,
         "NameColour": pref_dict["Name Colour"],
         "MessageColour": pref_dict["Message Colour"], 
         "BorderColour": pref_dict["Border Colour"],
         "MessageBorderColour" : pref_dict["Message Border Colour"]
         })
    conn.commit()


@sio.event
async def get_user_data(sid, data):
    cur.execute(f"""SELECT * FROM users WHERE username=\"{data["to_access"]}\" LIMIT 1;""")
    a = cur.fetchone()
    conn.commit()
    await sio.emit("set_user_data", {"info": a, "sid": data["sid"]})


@sio.event
async def update_user(sid, data):
    global cur, conn
    print(data)
    username, password, prefs = data["username"], data["passwrd"], data["prefs"]
    cur.execute(f"""DELETE FROM users WHERE username = '{username}';""")
    cur.execute("INSERT INTO users VALUES" \
     "(:username, :password, :NameColour, :MessageColour, :BorderColour, :MessageBorderColour)",
     {
         "username": username,
         "password": password,
         "NameColour": prefs["Name Colour"],
         "MessageColour": prefs["Message Colour"], 
         "BorderColour": prefs["Border Colour"],
         "MessageBorderColour" : prefs["Message Border Colour"]
         })
    conn.commit()
    
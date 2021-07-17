# Client
import asyncio
import socketio
import keyboard
import rendering
import main as main_navigation
from rich.console import Console
from rich.prompt import Prompt, Confirm, IntPrompt
from rich.panel import Panel
from rich.text import Text
from rich.live import Live
from utils import clear, User


class MessagePromptStop(Exception):
    pass


sio = socketio.AsyncClient()
console = Console()
CONNECTED: bool = False
USERNAME = ""
ROOM = ""
ROOMS: list[dict] = []

messages_to_show: list = []


async def exit_client():
    # print("[CLIENT]: exiting client application.")
    await sio.disconnect()
    exit()


def set_rooms(data):
    globals().update(ROOMS=data["rooms"])


async def get_rooms():
    await sio.emit("get_rooms", callback=set_rooms)


def get_room_data():
    return ROOMS


@sio.event
async def connect():
    print('[CLIENT]: connected to server')
    globals().update(CONNECTED=True)


@sio.event
async def disconnect():
    print('[CLIENT]: disconnected from server')
    globals().update(CONNECTED=False)


@sio.event
async def send_message(sid, data):
    print(f'[CLIENT]: message sent {sid}, data: {data}')


@sio.event
async def receive_message(data):
    global messages_to_show
    messages_to_show.append([data["username"], data["message"]])
    print(f"{data['username']}-{data['message']}")


async def main():
    print("[CLIENT]: Starting connection...")
    try:
        await sio.connect('http://localhost:8080')
    except ConnectionError as e:
        print("[CLIENT]: could not connect to server, please restart the application.")
    await asyncio.sleep(2)
    print("[CLIENT]: Running console...")
    await console_loop()


async def ping_server():
    await sio.emit("keep_alive")


async def console_loop():
    global messages_to_show
    # TODO: log the user in/make an account
    if CONNECTED:
        user = main_navigation.main_menu(logged_in=False, logged_in_as=None)
        globals().update(USERNAME=user.username)
        console.print(Panel("Enter the name of a box to join \nIf the box doesn't exist a new one will be created", style=user.preferences.preference_dict["Border Colour"], border_style=user.preferences.preference_dict["Border Colour"]))
        name = Prompt.ask(Text.assemble(("╰>", user.preferences.preference_dict["Border Colour"])))
        console.print(Panel(f"Joining {name}", style="green", border_style="green"))

        await sio.emit("join_room", {"username": user.username, "room_name": name})
        clear()
        await asyncio.sleep(0.01)

    while True and CONNECTED:
        console.print("Tip: Hold space to type")
        await asyncio.sleep(2)
        if keyboard.is_pressed("space"):
            message = rendering.prompt(user)
            await asyncio.sleep(0.01)
            await sio.emit("send_message", {"username": user.username, "message": message, "room_name": name})
        global messages_to_show
        if len(messages_to_show) != 0:
            clear()
            index_of_i = -1
            for i in messages_to_show:
                index_of_i += 1
                with Live("", refresh_per_second=14) as live:
                    render_user = User(i[0], "NotImportant", preferences=user.preferences)
                    rendering.render_message(i[1], render_user, live=live)
                    messages_to_show.pop(index_of_i)
        clear()

if __name__ == "__main__":
    asyncio.run(main())

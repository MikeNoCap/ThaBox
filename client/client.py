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
ROOMS: list = []
ROOM_WORKS : bool = False

messages_to_show: list = []


async def exit_client():
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
    print("[CLIENT]: reconnecting...")
    globals().update(ROOM_WORKS=False)
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
        await sio.connect('http://thabox.asmul.net:8000')
    except ConnectionError as e:
        print("[CLIENT]: could not connect to server, please restart the application.")
    await asyncio.sleep(2)
    print("[CLIENT]: Running console...")
    await console_loop()


async def ping_server():
    await sio.emit("keep_alive")


async def console_loop(user=None):
    global messages_to_show
    # TODO: log the user in/make an account
    if True:
        if user is None:
            user = main_navigation.main_menu(logged_in=False, logged_in_as=None)
        if user is not None:
            user = main_navigation.main_menu(logged_in=True, logged_in_as=user)
        globals().update(USERNAME=user.username)
        console.print(Panel("Enter the name of a box to join \nIf the box doesn't exist a new one will be created", style=user.preferences.preference_dict["Border Colour"], border_style=user.preferences.preference_dict["Border Colour"]))
        name = Prompt.ask(Text.assemble(("╰>", user.preferences.preference_dict["Border Colour"])))
        console.print(Panel(f"Joining {name}", style="green", border_style="green"))

        await sio.emit("join_room", {"username": user.username, "room_name": name})
        clear()
        await asyncio.sleep(0.01)
        globals().update(ROOM_WORKS=True)

    cancel_render = False
    while True:
        if not ROOM_WORKS:
            await sio.emit("join_room", {"username": user.username, "room_name": name})
            globals().update(ROOM_WORKS=True)
        if not cancel_render:
            console.print(rendering.render_menu_screen(rendering.get_message_box_rows([], user)))
            console.print("Tips: Hold AltGr+Space to type, Hold AltGR+C to go back to main-menu.")
        else:
            cancel_render = False
        wait = True
        while wait:
            if not ROOM_WORKS:
                await sio.emit("join_room", {"username": user.username, "room_name": name})
                globals().update(ROOM_WORKS=True)
            if keyboard.is_pressed("alt gr+space"):
                event = "msg"
                break
            if keyboard.is_pressed("alt gr+c"):
                event = "return"
                break
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
                console.print(rendering.render_menu_screen(rendering.get_message_box_rows([], user)))
                console.print("Tips: Hold AltGr+Space to type, Hold AltGR+C to go back to main-menu.")
                
            await asyncio.sleep(0.2)
        if event == "msg":
            clear()
            message = rendering.prompt(user)
            await asyncio.sleep(0.01)
            await sio.emit("send_message", {"username": user.username, "message": message, "room_name": name})
            cancel_render = True
        if event == "return":
            return await console_loop(user)

if __name__ == "__main__":
    asyncio.run(main())

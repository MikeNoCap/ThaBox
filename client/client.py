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
    console.print(Panel('Connected!', style="bold green", border_style="bold green"))
    globals().update(CONNECTED=True)


@sio.event
async def disconnect():
    globals().update(ROOM_WORKS=False)
    globals().update(CONNECTED=False)


@sio.event
async def send_message(sid, data):
    return #print(f'[CLIENT]: message sent {sid}, data: {data}')


@sio.event
async def receive_message(data):
    global messages_to_show, ROOM
    if data["room_name"] == ROOM:
        messages_to_show.append([data["username"], data["message"]])


async def main():
    console.print(Panel("Starting connection...", style="bold yellow", border_style="bold yellow"))
    try:
        await sio.connect('http://thabox.asmul.net:8000')
    except ConnectionError as e:
        print("[CLIENT]: could not connect to server, please restart the application.")

    
    console.print(Panel("Enjoy your stay!", style="bold green", border_style="bold green"))
    await asyncio.sleep(3)
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
        globals().update(ROOM=name)
        globals().update(ROOM_WORKS=True)
        await asyncio.sleep(0.01)
        clear()
        
        

    cancel_render = False
    while True:
        if not cancel_render:
            console.print(rendering.render_menu_screen(rendering.get_message_box_rows([], user)))
            console.print("Tips: Hold AltGr+Space to type, Hold AltGR+C to go back to main-menu.")
        else:
            cancel_render = False

        
        wait = True
        while wait:
            if not ROOM_WORKS: # Check if connection was lost to reconnect if it was try to reconnect.
                console.print(Panel("Your connection was lost.", style="bold yellow", border_style="bold yellow"))
                console.print(Panel("Reconnecting...", style="bold yellow", border_style="bold yellow"))


                loop_count = 0 # Store loop-count to cancel reconnect if it exceeds time-limit.
                feedback = Panel("Could not reconnect. Please check your internet connection and restart the program.", style="bold red", border_style="bold red")
                back_online = False
                
                reconnecting = True
                while reconnecting:
                    await asyncio.sleep(1)
                
                    loop_count += 1
                    if loop_count == 11:
                        break

                    try:
                        await sio.emit("join_room", {"username": user.username, "room_name": name})
                    except Exception as e:
                        print(e)
                        continue
                
                    feedback = Panel("Back online!", style="bold green", border_style="bold green")
                    reconnecting = False
                    back_online = True
                    globals().update(ROOM_WORKS=True)
                console.print(feedback)

                if back_online:
                    clear()
                    console.print(rendering.render_menu_screen(rendering.get_message_box_rows([], user)))
                    console.print("Tips: Hold AltGr+Space to type, Hold AltGR+C to go back to main-menu.")

            
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
            await sio.emit("leave_room", {"username": user.username, "room_name": name})
            return await console_loop(user)

if __name__ == "__main__":
    asyncio.run(main())

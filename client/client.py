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
import sys
import os
#from playsound import playsound

class MessagePromptStop(Exception):
    pass


sio = socketio.AsyncClient(request_timeout=30)

console = Console()


CONNECTED: bool = False
SERVER_ADDRESS = ("http://localhost:8000", "http://thabox.asmul.net:8000")[0]

USERNAME = ""
ROOM = ""
ROOMS: list = []
ROOM_WORKS : bool = False
WAIT_FOR_INFO = False
LOGIN_DATA = 0

messages_to_show: list = []



async def exit_client():
    await sio.disconnect()
    exit()


def set_rooms(data):
    globals().update(ROOMS=data["rooms"])


async def get_rooms():
    await sio.emit("get_rooms", callback=set_rooms)


@sio.event
def set_user_data(data):
    if data["sid"] != sio.sid:
        return
    globals().update(LOGIN_DATA=data["info"])
    globals().update(WAIT_FOR_INFO=False)


async def update_user(user: User):
    prefs = user.preferences.preference_dict
    username = user.username
    password = user.hashed_pass
    
    success = False
    while not success:    
        try:
            await sio.emit("update_user", {"username": username, "passwrd": password, "prefs": prefs})
            success = True
        except socketio.exceptions.BadNamespaceError:
            try:
                await sio.connect(SERVER_ADDRESS)
            except socketio.exceptions.ConnectionError:
                feedback = Panel("Lost connection and could not reconnect. Please check your internet connection and restart the program.", style="bold red", border_style="bold red")
                console.print(feedback)
            continue



async def get_user_data(username):
    globals().update(WAIT_FOR_INFO=True)
    success = False
    while not success:    
        try:
            await sio.emit("get_user_data", {"to_access": username, "sid": sio.sid})
            success = True
        except socketio.exceptions.BadNamespaceError:
            try:
                await sio.connect(SERVER_ADDRESS)
            except socketio.exceptions.ConnectionError:
                feedback = Panel("Lost connection and could not reconnect. Please check your internet connection and restart the program.", style="bold red", border_style="bold red")
                console.print(feedback)
            continue

            
    
    while True:
        await asyncio.sleep(0.7)
        global WAIT_FOR_INFO
        if not WAIT_FOR_INFO:
            break
    global LOGIN_DATA
    info = LOGIN_DATA
    globals().update(LOGIN_DATA=0)
    return info


async def save_user(username, password, pref_dict):
    success = False
    while not success:
        await asyncio.sleep(0.1)
        try:
            await sio.emit("save_user", {"username": username, "password": password, "pref_dict": pref_dict})
            success = True
        except socketio.exceptions.BadNamespaceError:
            try:
                await sio.connect(SERVER_ADDRESS)
            except socketio.exceptions.ConnectionError:
                feedback = Panel("Lost connection and could not reconnect. Please check your internet connection and restart the program.", style="bold red", border_style="bold red")
                console.print(feedback)
            continue
    


def get_room_data():
    return ROOMS


@sio.event
async def connect():
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
        await sio.connect(SERVER_ADDRESS)
    except socketio.exceptions.ConnectionError as e:
        feedback = Panel("Could not connect to server. Please check your internet connection and restart the program.", style="bold red", border_style="bold red")
        console.print(feedback)
        exit()

    console.print(Panel('Connected!', style="bold green", border_style="bold green"))
    console.print(Panel("Enjoy your stay!", style="bold green", border_style="bold green"))
    await asyncio.sleep(2)
    return await console_loop()


async def ping_server():
    await sio.emit("keep_alive")


async def console_loop(user=None):
    global messages_to_show
    clear()
    await rendering.load_box_animation(None)
    if user is None:
        action, user = await main_navigation.main_menu(logged_in=False, logged_in_as=None)
    if user is not None:
        action, user = await main_navigation.main_menu(logged_in=True, logged_in_as=user)
    
    if user is not None:
        await update_user(user)

    if action == "exit":
        if user is not None:
            await update_user(user)        
            await asyncio.sleep(1)
            print("Saving account preferences...")
        try:
            await sio.disconnect()
        except:
            pass
        await sio.wait()
        return
    globals().update(USERNAME=user.username)
    

    console.print(Panel("Enter the name of a box to join \nIf the box doesn't exist a new one will be created", style=user.preferences.preference_dict["Border Colour"], border_style=user.preferences.preference_dict["Border Colour"]))
    name = Prompt.ask(Text.assemble(("╰>", user.preferences.preference_dict["Border Colour"])))
    console.print(Panel(f"Joining {name}", style="green", border_style="green"))
    await sio.emit("join_room", {"username": user.username, "room_name": name, "sid": sio.sid})
    await asyncio.sleep(1)
    globals().update(ROOM=name)
    globals().update(ROOM_WORKS=True)
    clear()
        
        

    cancel_render = False
    while True:
        if not cancel_render:
            console.print(await rendering.render_menu_screen(await rendering.get_message_box_rows([], user)))
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
                        continue
                
                    feedback = Panel("Back online!", style="bold green", border_style="bold green")
                    reconnecting = False
                    back_online = True
                    globals().update(ROOM_WORKS=True)
                console.print(feedback)

                if back_online:
                    clear()
                    console.print(await rendering.render_menu_screen(await rendering.get_message_box_rows([], user)))
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
                        await rendering.render_message(i[1], render_user, live=live)
                        messages_to_show.pop(index_of_i)
                clear()
                console.print(await rendering.render_menu_screen(await rendering.get_message_box_rows([], user)))
                console.print("Tips: Hold AltGr+Space to type, Hold AltGR+C to go back to main-menu.")
                
            await asyncio.sleep(0.2)
        if event == "msg":
            clear()
            message = await rendering.prompt(user)
            await asyncio.sleep(0.01)
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
                        continue
                
                    feedback = Panel("Back online!", style="bold green", border_style="bold green")
                    reconnecting = False
                    back_online = True
                    globals().update(ROOM_WORKS=True)
                console.print(feedback)

                if back_online:
                    clear()
                    console.print(await rendering.render_menu_screen(await rendering.get_message_box_rows([], user)))
                    console.print("Tips: Hold AltGr+Space to type, Hold AltGR+C to go back to main-menu.")
                    
            await sio.emit("send_message", {"username": user.username, "message": message, "room_name": name})
            cancel_render = True
        if event == "return":
            await sio.emit("leave_room", {"username": user.username, "room_name": name})
            return await console_loop(user)

if __name__ == "__main__":
    try:
        asyncio.run(main())
        os.system("python client\exit.py")
        sys.exit(1)
    except RuntimeError:
        pass

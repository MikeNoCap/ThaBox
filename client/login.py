import pickle
import random
import re
import string
import time
import utils
from hashlib import sha256
from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text
from utils import Preferences, User, clear
from client import get_user_data, save_user
import asyncio
try:
    with open("secrets.pkl", "rb") as fp:
        secrets = pickle.load(fp)
except FileNotFoundError:
    print("file not found, creating new file")
    with open("secrets.pkl", "wb") as fp:
        pickle.dump([], fp)
        secrets = []

printable_chars = list(string.printable.replace("\n", "").replace(" ", "").replace("    ", ""))

console = Console()


def add_salt(hash_no_salt):
    for i in range(9):
        hash_no_salt += random.choice(printable_chars)
    return hash_no_salt


def remove_salt(hash_and_salt):
    back_hash_removed = hash_and_salt[:-9]
    return back_hash_removed


def hash_pass(passwrd: str):
    hashed = sha256(bytes(passwrd, "utf8")).hexdigest()
    return add_salt(hashed)


async def create_account(username: str, password: str):
    password = hash_pass(password)
    prefs = Preferences()
    user_ob = User(username=username, paswrd=password, preferences=prefs)
    await save_user(username, password, prefs.preference_dict)
    return user_ob


async def sign_up():
    global secrets
    progress_visual = []
    username_status = "working"
    while username_status != "ready":
        clear()
        console.print(Panel(Text.assemble(("Enter a username", "bold purple")),
                            style="bold purple", border_style="bold purple"))

        username = Prompt.ask(Text.assemble(("╰→", "bold red")))
        console.print("Checking username...", style="bold yellow")
        data = await get_user_data(username)

        if data is not None:
            clear()
            console.print(Panel(Text.assemble(("Username already taken", "bold purple")),
                                style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if " " in username:
            clear()
            console.print(Panel(Text.assemble(("Can not have space in username", "bold purple")),
                                style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if len(username) < 4:
            clear()
            console.print(Panel(Text.assemble(("Username must be at least 4 characters long",
                                               "bold purple")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue

        progress_visual.append(Panel(Text.assemble(("Username ☺", "bold green")),
                                     style="bold green", border_style="bold green"))
        progress_visual.append(Text.assemble(("╰→", "bold red"), (username, "none")))
        username_status = "ready"

    password_status = "working"
    while password_status != "ready":
        clear()
        for i in progress_visual:
            console.print(i)

        console.print(Panel(Text.assemble(("Enter a password (1)", "bold cyan")),
                            style="bold cyan", border_style="bold cyan"))
        password = Prompt.ask(Text.assemble(("╰→", "bold red")), password=True)
        console.print("Checking password...", style="bold yellow")
        await asyncio.sleep(0.3)
        # Checks
        if " " in password:
            clear()
            console.print(Panel(Text.assemble(("Can not have space in password", "bold cyan")),
                                style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if len(password) < 8:
            clear()
            console.print(Panel(Text.assemble(("Password must be at least 8 characters long",
                                               "bold cyan")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if len(password) > 32:
            clear()
            console.print(Panel(Text.assemble(("Password can not be any longer than 32 characters",
                                               "bold cyan")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if not re.search("[a-z]", password):
            clear()
            console.print(Panel(Text.assemble(("Password must contain at least one lowercase character",
                                               "bold cyan")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if not re.search("[A-Z]", password):
            clear()
            console.print(Panel(Text.assemble(("Password must contain at least one uppercase character",
                                               "bold cyan")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if not re.search("[A-Z]", password):
            clear()
            console.print(Panel(Text.assemble(("Password must contain at least one uppercase character",
                                               "bold cyan")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        if not re.search("[0-9]", password):
            clear()
            console.print(Panel(Text.assemble(("Password must contain at least one digit", "bold cyan")),
                                style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue
        for i in password:
            if i not in printable_chars:
                clear()
                console.print(Panel(Text.assemble(("Password can only contain letters from the ASCII table",
                                                   "bold cyan")), style="bold red", border_style="bold red"))
                await asyncio.sleep(2.1)
                clear()
                continue
        clear()
        for i in progress_visual:
            console.print(i)
        console.print(Panel(Text.assemble(("Enter a password (1)", "bold cyan")),
                            style="bold cyan", border_style="bold cyan"))
        console.print(Text.assemble(("╰→", "bold red")))

        console.print(Panel(Text.assemble(("Repeat password (2)", "bold cyan")),
                            style="bold cyan", border_style="bold cyan"))
        password2 = Prompt.ask(Text.assemble(("╰→", "bold red")), password=True)

        if password != password2:
            clear()
            console.print(Panel(Text.assemble(("Passwords did not match", "bold cyan")),
                                style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            clear()
            continue

        progress_visual.append(Panel(Text.assemble(("Password ☺", "bold green")),
                                     style="bold green", border_style="bold green"))
        progress_visual.append(Text.assemble(("╰→", "bold red"), ("HIDDEN", "bold yellow")))
        password_status = "ready"
    clear()
    for i in progress_visual:
        console.print(i)

    a = await create_account(username, password2)

    console.print(Panel(Text.assemble(("Successfully created an account!")), style="bold green", border_style="green"))
    await asyncio.sleep(2.1)
    clear()
    return a


async def log_in():
    status = "working"
    while status != "done":
        clear()
        console.print(Panel(Text.assemble(("Username", "bold purple")),
                            style="bold magenta", border_style="bold purple"))
        username = Prompt.ask(Text.assemble(("╰→", "bold red")))

        console.print(Panel(Text.assemble(("Password", "bold purple")), style="bold cyan", border_style="bold cyan"))
        password = Prompt.ask(Text.assemble(("╰→", "bold red")), password=True)

        console.print("Validating login...", style="bold yellow")
        user_data = await get_user_data(username)
        

        if user_data is None:
            clear()
            console.print(Panel(Text.assemble(("Invalid username or password. Please try again.",
                                               "bold red")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            continue

        if not sha256(bytes(password, "utf-8")).hexdigest() == remove_salt(user_data[1]):
            clear()
            console.print(Panel(Text.assemble(("Invalid username or password. Please try again.",
                                               "bold red")), style="bold red", border_style="bold red"))
            await asyncio.sleep(2.1)
            continue
        clear()
        console.print(Panel(Text.assemble(("Success! Logged in as " + username, "bold green")),
                            style="bold green", border_style="green"))
        await asyncio.sleep(2.1)
        clear()
        prefs = Preferences()
        new_pref_dict = {
            "Name Colour": user_data[2],
            "Message Colour": user_data[3],
            "Border Colour": user_data[4],
            "Message Border Colour": user_data[5]
        }
        prefs.preference_dict = new_pref_dict
        return User(username, hash_pass(password), prefs)


async def login():
    choice = utils.make_style_prompt(choices=["Log in", "Sign up"], prompt_msg="Please log-in/sign up:",
                                     main_style="bold purple", frame_border_style="bold cyan", frame_style="bold red")
    if choice == "Log in":
        return await log_in()
    if choice == "Sign up":
        return await sign_up()

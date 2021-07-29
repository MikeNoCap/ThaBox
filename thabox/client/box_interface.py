import keyboard
import time
import sys
import random
from utils import clear
from utils import GoBack
from utils import User
from rich import print
from rich.console import Console
from rich.align import Align
from rich.prompt import Prompt
from rich.panel import Panel
from rich.layout import Layout
from rich.text import Text
from rendering import render_chat_rooms, render_menu_screen

"""
'id, password, size, stype = create_box_tui(User, sessions_data)'
To run the create_box_tui - the variables can be changed (i.e. to a list), by 
returning a different value at lines 322 and 352. To be called on main.py, hover_on = 1

'join_box_tui(User, sessions_data)'
To run the join_box_tui - no variables returned, as the session id's, from sessions_data
is used to print and select a valid session. May need to be edited to return session_id if needed.
To be called on main.py, hover_on = 2
"""

console = Console()

"""
This will be passed into the join_box_tui() function when called. List(?) to be filled
from the database. After database is created, it needs to be implemented into this code.
currently a temp variable
"""

sessions_data = [[1234]]

global layout, colours, private_box_art, public_box_art

colour = {
    "box_default": "bold white",
    "box_hover": "bold yellow"
}

public_box_art = ("""
          +--+
          |  |
          |  |
          |  |
          |  |
          |  |
        +-+  +-+
   +-----\    /-------+
  /|      \  /       /|
 / |       \/       / |  
+--+---------------+  |
|                  |  |
|    PUBLIC BOX    |  +
|                  | /
+------------------+/
""")

private_box_art = ("""
         .------.
        / .----. \  
       _| |____| |_
     .'    ____    '.
     |    /    \    |  
     |    \____/    |
     '.____________.' 
   +------------------+
  /                  /|
 /                  / |  
+--+---------------+  |
|                  |  |
|    PRIVATE BOX   |  +
|                  | /
+------------------+/
""")

# Splitting the console to place the boxes side by side
layout = Layout()
layout.visible = True
layout.split_column(
    Layout(name="title"),
    Layout(name="boxes"),
    Layout(name="screen")
)

layout["title"].size = 5
layout["boxes"].size = 16
layout["screen"].size = 5

layout["boxes"].split_row(
    Layout(name="left"),
    Layout(name="right")
)

"""
temp values for testing

sessions_data = [
    {
        "room_name": "1234",
        "private" : True,
        "password" : "hello",
        "capacity" : "1",
        "room_owner" : "bob"
    },
    {
        "room_name": "2222",
        "private" : True,
        "password" : "zxcv",
        "capacity" : "1",
        "room_owner" : "lob"
    },
    {
        "room_name": "3333",
        "private" : True,
        "password" : "sdfg",
        "capacity" : "1",
        "room_owner" : "tob"
    },
    {
        "room_name": "4444",
        "private" : False,
        "password" : None,
        "capacity" : "1",
        "room_owner" : "mob"
    },
    {
        "room_name": "5555",
        "private" : False,
        "password" : None,
        "capacity" : "1",
        "room_owner" : "cob"
    },
]
"""


def is_already_an_id(sessions_data, session_id, server_type="all"):
    if not server_type:
        for elem in sessions_data:
            if not elem["private"]:
                if elem["room_name"] == session_id:
                    return True

    elif server_type == "all":
        for elem in sessions_data:
            if elem["room_name"] == session_id:
                return True

    else:
        for elem in sessions_data:
            if elem["private"]:
                if elem["room_name"] == session_id:
                    return True

    return False


def is_correct_password(sessions_data, password, session_id):
    for elem in sessions_data:
        if elem["room_name"] == session_id:
            if elem["password"] == password:
                return True
    return False


def layout_setup(select: str, text: str):  # DONE
    """
    Creates menu layout, with ASCII box art and navigation help text.
    """
    global layout, private_box_art, public_box_art, colour

    clear()
    layout["title"].update(Align(text, align="center"))
    layout["screen"].update(
        "\n\n[bold white]!   Use [bold magenta] right arrow[/] or [bold magenta]left arrow[/] to select a box.[/]"
        + "\n[bold white]!   [bold magenta]ENTER[/] to confirm your choice.[/]"
        + "\n[bold white]!   Press [bold magenta]BACKSPACE[/] to return to Menu.[/]")

    if select == "left":
        layout["right"].update(Align(Text(f"{private_box_art}", style=colour["box_default"]), align="center"))
        layout["left"].update(Align(Text(f"{public_box_art}", style=colour["box_hover"]), align="center"))
    else:
        layout["right"].update(Align(Text(f"{private_box_art}", style=colour["box_hover"]), align="center"))
        layout["left"].update(Align(Text(f"{public_box_art}", style=colour["box_default"]), align="center"))

    console.print(layout)


def tui_navigation(select: str, sessions_data):  # DONE
    """
    Returns which box is selected.
    """

    # Adds delay between key presses
    time.sleep(0.2)
    while True:
        if keyboard.is_pressed("backspace"):
            raise GoBack

        if keyboard.is_pressed("left_arrow"):
            if select != "left":
                select = "left"
                return select
            continue

        if keyboard.is_pressed("right_arrow"):
            if select != "right":
                select = "right"
                return select
            continue

        if keyboard.is_pressed("enter"):
            if select == "left":
                select = "public"
                return select

            elif select == "right":
                select = "private"
                return select


def create_session_id(sessions_data):  # DONE
    """
    Adds leading 0's if necessary and returns a unique session_id,
    by comparing it to taken id's.
    """
    num: int = random.randint(1, 1000)
    session_id: str = ("0" * (4 - len(str(num)))) + str(num)
    if is_already_an_id(sessions_data, session_id):
        return create_session_id(sessions_data)

    return str(session_id)


def enter_session_id(prompt: str, alignment: str, password_prompt, sessions_data):
    """
    Prompts user to enter a valid session ID
    """
    given_id = console.input(prompt)

    if given_id.lower() == "back":
        return join_box_tui(User, sessions_data)

    elif (len(given_id) == 4) and (given_id.isdigit() is True):
        if is_already_an_id(sessions_data, given_id, password_prompt):
            if password_prompt:
                enter_password(sessions_data, password_prompt, given_id)

            else:
                console.print(Align("\n✔️   Joining ThaBox...", align=alignment))
                time.sleep(0.5)
                clear()
                return given_id

        else:
            console.print(Align("❌   The room you are trying to join doesn't exist\n", align=alignment))
            time.sleep(0.5)
            return enter_session_id(prompt, alignment, password_prompt, sessions_data)

    else:
        console.print(Align("❌   Session ID's can only be 4 digit numbers!\n", align=alignment))
        time.sleep(0.5)
        return enter_session_id(prompt, alignment, password_prompt, sessions_data)


def enter_password(sessions_data, prompt, session_id):
    """
    Checks if entered password is correct.
    """
    time.sleep(0.3)  # Input delay
    given_password = console.input(prompt)
    if is_correct_password(sessions_data, given_password, session_id):
        console.print(Align("\n✔️   Joining ThaBox...", align="center"))
        time.sleep(1)
        clear()
        return session_id, given_password

    else:
        console.print(Align("❌   Incorrect Password!", align="center"))
        return enter_password(sessions_data, prompt, session_id)


def enter_room_size(user):  # DONE
    """
    Validates the user input, so they enter a correct size, and 
    returns the room_size.
    """
    size = console.input(" " * ((console.width // 2) - 14) + "[bold red]Enter room size (2 - 6):   [/]")

    if size.lower() == "back":
        return create_box_tui(user, sessions_data)

    if size == "2" or size == "3" or size == "4" or size == "5" or size == "6":
        return str(size)

    else:
        console.print(Align("❌   Enter a valid number!\n", align="center"))
        return enter_room_size(user)


def join_box_tui(user: User, sessions_data, select="left"):
    if select == "public":
        """
        PLAN - print only 4 session at once. Users can navigate this using arrow keys.
        They type the session id of the room they wan to join, and then they join the room.
        DATA NEEDED - public session id, max user count for the room, current amount of users
        in the room. 
        """
        clear()

        console.print(Align("\n█▀█ █ █ █▄▄ █   █ █▀▀   █▄▄ █▀█ ▀▄▀ █▀▀ █▀\n"
                            + "█▀▀ █▄█ █▄█ █▄▄ █ █▄▄   █▄█ █▄█ █ █ ██▄ ▄█\n",
                            align="center"),
                      style=user.preferences.preference_dict['Border Colour'])

        for elem in sessions_data:
            if not elem["private"]:
                console.print(Align(Panel("Session ID = " + elem["room_name"]
                                          + "\nOwner = " + elem["room_owner"]
                                          + "\nCapacity = " + elem["capacity"], expand=False), align="center"),
                              style="bold white")
        console.print(
            "\n\n[bold white]!   Use [bold magenta] right arrow[/] or [bold magenta]left arrow[/] to find more rooms.[/]\n"
            + "[bold white]!   [bold magenta]SPACE[/] to type in a session ID.[/]\n"
            + "[bold white]!   Press [bold magenta]BACKSPACE[/] to go back.[/]")

        time.sleep(0.2)
        while True:
            if keyboard.is_pressed("backspace"):
                select = "left"
                return join_box_tui(user, sessions_data, select)

            if keyboard.is_pressed("space"):
                console.print()
                chatroom_name = enter_session_id(
                    "[bold red]>   Enter the session ID or type 'BACK' to go back:[/]   ", "left", False, sessions_data)

                return chatroom_name
                """
                user needs to be redirected to another chat room
                """

    elif select == "private":
        clear()
        console.print(Align("\n█▀█ █▀█ █ █ █ ▄▀█ ▀█▀ █▀▀   █▄▄ █▀█ ▀▄▀\n"
                            + "█▀▀ █▀▄ █ ▀▄▀ █▀█  █  ██▄   █▄█ █▄█ █ █\n", align="center"),
                      style=user.preferences.preference_dict["Border Colour"])

        console.print(Align("\nType [bold magenta]BACK[/] in the Session ID field to go back.\n", align="center"))

        chatroom_name, room_password = enter_session_id((" " * ((console.width // 2) - 14) + "[bold red]Enter the session ID:[/]   "), "center",
                                                        (str("\n" + " " * ((console.width // 2) - 17) + "[bold red]Enter the room password:[/]   ")), sessions_data)

        return chatroom_name
        """
        user needs to be redirected to the chat room
        """

    else:
        """
        JOIN BOX MENU
        """
        layout_setup(select,
                     f"[{user.preferences.preference_dict['Border Colour']}]\n\n  █ █▀█ █ █▄ █   █▄▄ █▀█ ▀▄▀\n█▄█ █▄█ █ █ ▀█   █▄█ █▄█ █ █[/]")  # select, "JOIN BOX"
        select = tui_navigation(select, sessions_data)
        join_box_tui(user, sessions_data, select)


def create_box_tui(user: User, sessions_data, select="left"):
    """
    Allows user to create thier own box - can set the room_size
    and add a password, which are both returned along with a random,
    unique session id.
    """

    if select == "public":
        clear()
        public_session_id = create_session_id(sessions_data)

        console.print(Align("\n█▄▄ █▀█ ▀▄▀   █▀ █▀▀ ▀█▀ ▀█▀ █ █▄ █ █▀▀ █▀\n"
                            + "█▄█ █▄█ █ █   ▄█ ██▄  █   █  █ █ ▀█ █▄█ ▄█\n", align="center"),
                      style=user.preferences.preference_dict['Border Colour'])
        console.print(Align("Type [bold magenta]BACK[/] in any of the fields to go back.\n", align="center"))
        console.print(Align(f"[bold red]Session ID:[/]   {public_session_id}", align="center"))

        room_size = enter_room_size(user)

        console.print(Align("\n✔️   Creating ThaBox...", align="center"))
        time.sleep(0.5)

        is_private = False
        password = None

        return "create", user, public_session_id, password, room_size, is_private

    elif select == "private":
        clear()
        private_session_id = create_session_id(sessions_data)

        console.print(Align("\n█▄▄ █▀█ ▀▄▀   █▀ █▀▀ ▀█▀ ▀█▀ █ █▄ █ █▀▀ █▀\n"
                            + "█▄█ █▄█ █ █   ▄█ ██▄  █   █  █ █ ▀█ █▄█ ▄█\n", align="center"),
                      style=user.preferences.preference_dict['Border Colour'])
        console.print(Align("Type [bold magenta]BACK[/] in any of the fields to go back.\n", align="center"))
        console.print(Align(f"[bold red]Session ID:[/]   {private_session_id}", align="center"))

        while True:
            time.sleep(0.2)
            password = console.input(" " * ((console.width // 2) - 12) + "[bold red]Create a Password:   [/]")
            if password.lower() == "back":
                return create_box_tui(user, sessions_data)
            elif password == "":
                console.print(Align("❌   Password can't be blank!\n", align="center"))
            elif " " in password:
                console.print(Align("❌   Password can't have spaces!\n", align="center"))
            elif len(password) < 8:
                console.print(Align("❌   Password must have at least 8 characters!\n", align="center"))

            else:
                room_size = enter_room_size(user)
                break

        console.print(Align("\n✔️   Creating ThaBox...", align="center"))
        time.sleep(0.5)

        is_private = True
        return "create", user, private_session_id, password, room_size, is_private

    else:
        """
        CREATE BOX MENU
        """
        layout_setup(select,
                     f"[{user.preferences.preference_dict['Border Colour']}]\n\n█▀▀ █▀█ █▀▀ ▄▀█ ▀█▀ █▀▀   █▄▄ █▀█ ▀▄▀\n█▄▄ █▀▄ ██▄ █▀█  █  ██▄   █▄█ █▄█ █ █[/]")  # select, "CREATE BOX"

        select = tui_navigation(select, sessions_data)
        return create_box_tui(user, sessions_data, select)


def chat_rooms_scroll(logged_in_as: User):
    clear()
    selected = False
    options = {
        "Never": 1,
        "Gonna": 2,
        "Give": 3,
        "You": 4,
        "Up": 5,
        "Never": 6,
        "Gonna": 7,
        'Let': 8,
        'You': 9,
        'Down': 10,
    }

    hover_on = 1
    while not selected:
        rows = []
        rows_temp = [x.center(len("--------------------"), "|") for x in list(options)]

        rows_temp[hover_on - 1] = Text.assemble(
            (rows_temp[hover_on - 1].center(len("--------------------"), "|"), "bold yellow"))

        rows.append(Text.assemble(("--------------------", "bold blue")))
        for i in rows_temp:
            rows.append("")
            rows.append(i)
            rows.append("")
            rows.append(Text.assemble(("--------------------", "bold blue")))

        # Fill up unused space.
        while len(rows) < 21:
            rows.append(Text.assemble(("--------------------", "bold red")))

        console.print(render_menu_screen(rows))

        what_to_do = Prompt.ask(Text.assemble(("1: Scroll up\n", "bold cyan"), ("2: Scroll down\n", "bold cyan"),
                                              ("3: Select\n", "bold purple"), ("back: Back\n", "bold red")),
                                choices=["1", "2", "3", "back"], default="3")

        if what_to_do == "1":
            if hover_on == 1:
                clear()
                continue
            hover_on -= 1
        if what_to_do == "2":
            if hover_on == len(rows_temp):
                clear()
                continue
            hover_on += 1
        if what_to_do == "3":
            pass

        if what_to_do == "back":
            raise GoBack

        clear()


def ask_for_session():
    session = Prompt.ask("Please enter a session id")
    return session


def is_valid_session(session_id):
    """
    Use this function to test whether a given session id is valid or not.
    """
    for session in sessions_data:
        if session["room_name"] == session_id:
            return True
        else:
            continue
    return False


if __name__ == "__main__":
    chat_rooms_scroll({'Rick', 'Roll', 'Lol', })

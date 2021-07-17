import textwrap
from typing import List, TYPE_CHECKING
from rich import console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.console import Console
from rich.screen import Screen
from rich.live import Live
from rich.markup import escape
from rich.layout import Layout
from rich.prompt import Prompt
from utils import clear, User, Preferences
import time
import random

client_user = None


def get_index_duplicates(lst, item) -> list:
    """
    :param lst: The list to search for an item or items in.
    :param item: The item to find indexes for in list.
    Like list.index(), but list.index() only returns one index. This function returns all the indexes of which an item appears.
    """
    return [i for i, x in enumerate(lst) if x == item]


# Create the colored logo-text manually because rich's Panel()
# function does not allow you to get the raw_output (the string that is actually being printed)
RED = '\033[91m'
ENDC = '\033[0m'
PURPLE = '\033[95m'
CYAN = '\033[96m'
box_logo_lines = [
    RED + "╭────────────────────────────────╮  " + ENDC,
    RED + "│                                │  " + ENDC,
    RED + "│" + ENDC + PURPLE + " $$$$$$$$\\ $$\\                  " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + " \\__$$  __|$$ |                 " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + "    $$ |   $$$$$$$\\   $$$$$$\\   " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + "    $$ |   $$  __$$\\  \\____$$\\  " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + "    $$ |   $$ |  $$ | $$$$$$$ | " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + "    $$ |   $$ |  $$ |$$  __$$ | " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + "    $$ |   $$ |  $$ |\\$$$$$$$ | " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + PURPLE + "    \\__|   \\__|  \\__| \\_______| " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│                                │" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$$$$$$\\                       " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$  __$$\\                      " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$ |  $$ | $$$$$$\\  $$\\   $$\\  " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$$$$$$\\ |$$  __$$\\ \\$$\\ $$  | " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$  __$$\\ $$ /  $$ | \\$$$$  /  " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$ |  $$ |$$ |  $$ | $$  $$<   " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " $$$$$$$  |\\$$$$$$  |$$  /\\$$\\  " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│" + ENDC + CYAN + " \\_______/  \\______/ \\__/  \\__| " + ENDC + RED + "│" + ENDC + "  ",
    RED + "│                                │  " + ENDC,
    RED + "╰────────────────────────────────╯  " + ENDC
]
menu_logo = "".join([x + "\n" if x != box_logo_lines[-1] else x for x in box_logo_lines])


def render_menu_screen(rows: list) -> Text:
    """
    This function gets the Text-object that is shown to the user once in the main_menu or while in a box.

    :param rows: A list of strings that together make a box. (There must be at least 21 rows/items)
    :return: Text-object which can be printed with console.print().
    """

    logo_rows = menu_logo.split("\n")

    if len(rows) < 21:
        raise ValueError("The argument rows needs to contain at least 21 rows.")
    if len(rows) > 21:
        dummy_rows_to_add = len(rows) - len(logo_rows)
        dummy_rows = [Text.assemble(('-' * 34 + "  ", "red")) for _ in range(dummy_rows_to_add)]
        for i in range(dummy_rows_to_add):
            logo_rows.append(dummy_rows[i])

    new_rows = []
    for i in range(0, len(rows)):
        new_rows.append(Text.assemble(logo_rows[i], rows[i] + '\n'))
    return Text.assemble(*new_rows)


def get_message_box_rows(message_box: list, user: User) -> list:
    message_box = [_ + "".join([" " for i in range(90 - len(_))]) for _ in message_box]

    while len(message_box) != 26:
        message_box.append("".join([" " for i in range(90)]))
        if len(message_box) == 26:
            break
        message_box.insert(0, "".join([" " for i in range(90)]))

    if len(message_box) != 26:
        raise ValueError("Box must contain 26 rows.")

    border_color = user.preferences.preference_dict["Border Colour"]
    new_rows = []

    new_rows.append(
        Text.assemble(("┌──────────────────────────────────────────────────────────────────────────────────────────┐",
                       border_color)))
    for i in message_box:
        new_rows.append(Text.assemble(("│", border_color), i, ("│", border_color)))
    new_rows.append(
        Text.assemble(("└──────────────────────────────────────────────────────────────────────────────────────────┘",
                       border_color)))
    return new_rows


def get_message_box(msg_sender: User, message: str, stage: int) -> list:
    """Returns a list of strings which together assemble the message box that is being displayed in render_message."""

    name_color = msg_sender.preferences.preference_dict["Name Colour"]
    message_color = msg_sender.preferences.preference_dict["Message Colour"]
    border_color = msg_sender.preferences.preference_dict["Message Border Colour"]

    message_lines = textwrap.wrap(message, width=32)

    message_string = ""
    count = 0
    for _ in message_lines:
        count += 1
        if not count == len(message_lines):
            message_string += f"│{_ : <32}│" + "\n"
            continue
        message_string += f"│{_ : <32}│"

    if len(message_string.splitlines()) > 9:
        raise ValueError("Message too long!")

    msg_box = \
        f"┌────────────────────────────────┐\n" \
        f"│{'Message from' : ^32}│\n" \
        f"│{msg_sender.username : ^32}│\n" \
        f"├────────────────────────────────┤\n" \
        f"{message_string}\n" \
        f"└────────────────────────────────┘"

    lines = msg_box.splitlines()
    if stage < 34:
        a = [line[(34 - stage):34] for line in lines]
    if stage >= 34:
        a = ["".join([" " for _ in range(stage - 34)]) + line for line in lines]

    new = []

    c = 0
    for i in a:
        c += 1
        if c == 1 or c == 2 or c == 4:
            new.append(Text.from_markup(f"[{border_color}]{i}[/]"))
            continue
        if c == 3:
            list_username = list(msg_sender.username)
            list_line = list(i)
            if list_line.count("│") - list_username.count("│") == 2:  # Ignore │ in usernames.
                indexes = get_index_duplicates(list_line, "│")
                list_line[indexes[0]] = f"[{border_color}]│[/][{name_color}]"
                list_line[indexes[-1]] = f"[/][{border_color}]│[/]"
                new.append(Text.from_markup("".join(list_line)))
            if list_line.count("│") - list_username.count("│") == 1:
                indexes = get_index_duplicates(list_line, "│")
                list_line[indexes[-1]] = f"[/][{border_color}]│[/]"
                list_line.insert(0, f"[{name_color}]")
                new.append(Text.from_markup("".join(list_line)))
            continue
        if not c - 4 > len(message_lines):
            list_line = list(i)
            current_msg_line = list(message_lines[c - 5])
            if list_line.count("│") - current_msg_line.count("│") == 2:  # Ignore │ in usernames.
                indexes = get_index_duplicates(list_line, "│")

                list_line[indexes[0]] = f"[{border_color}]│[/][{message_color}]"
                list_line[indexes[-1]] = f"[/][{border_color}]│[/]"

                new.append(Text.from_markup("".join(list_line)))
            if list_line.count("│") - current_msg_line.count("│") == 1:
                indexes = get_index_duplicates(list_line, "│")

                if stage == 1:
                    list_line[0] = f"[{border_color}]│[/]"
                else:
                    list_line[0] = f"[{message_color}]"
                    list_line[indexes[-1]] = f" [{border_color}]│[/]"

                new.append(Text.from_markup("".join(list_line)))

        if c - 4 > len(message_lines):
            list_line = list(i)
            if "└" in list_line and "┘" in list_line:
                indexleft = get_index_duplicates(list_line, "└")[0]
                indexright = get_index_duplicates(list_line, "┘")[0]

                list_line[indexleft] = f"[{border_color}]└"
                list_line[indexright] = f"┘[/]"
                new.append(Text.from_markup("".join(list_line)))

            if "┘" in list_line and not "└" in list_line:
                index = get_index_duplicates(list_line, "┘")[0]

                if stage == 1:
                    list_line[index] = f"[{border_color}]┘[/]"

                else:
                    list_line[0] = f"[{border_color}]─"
                    list_line[index] = f"┘[/]"
                new.append(Text.from_markup("".join(list_line)))

    return new


def render_message(message: str, user: User, message_show_time: int = 6, live=Live()) -> Text:
    fade_left_frames = []
    for _ in range(0, 63):
        message_box = get_message_box(user, message, _)
        frame = render_menu_screen(get_message_box_rows(message_box, user))
        fade_left_frames.append(frame)

    going_down_box = get_message_box(user, message, 62)
    going_down_frames = []

    message_size = len(going_down_box)

    for i in range(26 - message_size):
        going_down_box.insert(0, "".join([" " for ___ in range(90)]))
        going_down_frames.append(render_menu_screen(get_message_box_rows(going_down_box, user)))
    for i in range(message_size):
        going_down_box.insert(0, "".join([" " for ___ in range(90)]))
        going_down_box.pop(-1)
        going_down_frames.append(render_menu_screen(get_message_box_rows(going_down_box, user)))

    for i in fade_left_frames:
        live.update(Text.assemble(i, ("\nYou can send messages or exit once messages are done displaying...")))
        time.sleep(0.05)

    time.sleep(message_show_time)

    for i in going_down_frames:
        live.update(Text.assemble(i, ("\nYou can send messages or exit once messages are done displaying...")))
        time.sleep(0.07)

    return live


def message_demo(user: User):
    global client_user
    client_user = user
    console = Console()
    while True:
        with Live("") as live:
            live.update(
                render_menu_screen(get_message_box_rows(["".join(" " for i in range(90)) for j in range(26)], user)))
            mes = "This is a demo message..."
            live = render_message(mes, user, live=live)
            time.sleep(100)


def render_chat_rooms(rows: list, hover_on: int) -> Text:
    """
    This function gets the Text-object that is shown to the user once in the main_menu or while in a box.

    :param rows: A list of strings that together make a box. (There must be at least 21 rows/items)
    :return: Text-object which can be printed with console.print().
    """

    logo_rows = menu_logo.split("\n")

    dummy_rows_to_add = len(rows[:hover_on + 7]) - len(logo_rows)  # [:(hover_on + 7) * 4 + 1]

    dummy_rows = [Text.assemble(('-' * 34 + "  ", "red")) for _ in range(dummy_rows_to_add)]
    for i in range(dummy_rows_to_add):
        logo_rows.append(dummy_rows[i])

    new_rows = []

    for i in range(0, len(logo_rows)):
        try:
            new_rows.append(Text.assemble(logo_rows[i], rows[i] + '\n'))
        except IndexError:
            new_rows.append(Text.assemble(logo_rows[i] + '\n'))

    return Text.assemble(*new_rows)


def prompt(user):
    console = Console()
    console.print(render_menu_screen(get_message_box_rows([""], user)))
    time.sleep(1.2)
    return Prompt.ask("Send a message")

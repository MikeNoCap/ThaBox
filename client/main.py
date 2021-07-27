from rich.text import Text
from rich.prompt import Prompt
from rich.panel import Panel
from rich.screen import Screen
from rich.console import Console, RenderGroup
from rich.align import Align
import box_interface
from utils import User, Preferences, GoBack, clear
from rendering import render_menu_screen, message_demo
import login
import credits
import help as help_page
from client import update_user

console = Console()

main_title = Text.assemble(
    (
        """
$$$$$$$$\\ $$\\
\\__$$  __|$$ |
   $$ |   $$$$$$$\\   $$$$$$\\
   $$ |   $$  __$$\\  \\____$$\\
   $$ |   $$ |  $$ | $$$$$$$ |
   $$ |   $$ |  $$ |$$  __$$ |
   $$ |   $$ |  $$ |\\$$$$$$$ |
   \\__|   \\__|  \\__| \\_______|\n
""",
        "bold magenta"),
    (
        """$$$$$$$\\
$$  __$$\\
$$ |  $$ | $$$$$$\  $$\   $$\\
$$$$$$$\ |$$  __$$\ \$$\ $$  |
$$  __$$\ $$ /  $$ | \$$$$  /
$$ |  $$ |$$ |  $$ | $$  $$<
$$$$$$$  |\$$$$$$  |$$  /\$$\\
\\_______/  \\______/ \\__/  \\__|
""",
        "bold cyan")
)


async def main_menu(logged_in: bool = False, logged_in_as=None):
    event = ""
    clear()
    selected = False
    if logged_in:
        options = {
            "Logged in as " + logged_in_as.username: 1,
            "Create/join a box": 2,
            "Preferences": 3,
            "Help/Info": 4,
            "Credits": 5,
            "Exit": 6
        }
    if not logged_in:
        options = {
            "Log in/Sign up": 1,
            "Help/Info": 2,
            "Credits": 3,
            "Exit": 4
        }

    hover_on = 1
    while not selected:
        rows = []
        rows_temp = [x.center(len("--------------------"), "|") for x in list(options)]
        if logged_in:
            logged_in_as_msg = rows_temp.pop(0)
        rows_temp[hover_on - 1] = Text.assemble(
            (rows_temp[hover_on - 1].center(len("--------------------"), "|"), "bold yellow"))

        rows.append(Text.assemble(("--------------------", "bold purple" if not logged_in else logged_in_as.preferences.preference_dict["Border Colour"])))
        for i in rows_temp:
            rows.append("")
            rows.append(i)
            rows.append("")
            rows.append(Text.assemble(("--------------------", "bold purple" if not logged_in else logged_in_as.preferences.preference_dict["Border Colour"])))

        # Fill up unused space.
        while len(rows) < 21:
            rows.append(Text.assemble(("--------------------", "bold purple" if not logged_in else logged_in_as.preferences.preference_dict["Border Colour"])))

        if logged_in:
            rows.insert(0, Text.assemble((logged_in_as_msg, "bold purple" if not logged_in else logged_in_as.preferences.preference_dict["Border Colour"])))

        console.print(await render_menu_screen(rows))
        if logged_in:
            what_to_do = Prompt.ask(Text.assemble(("1: Scroll up\n", "bold cyan"), ("2: Scroll down\n", "bold cyan"),
                                                  ("3: Select\n", "bold purple"), ("out: Log out\n", "bold red")),
                                    choices=["1", "2", "3", "out"], default="3")
        if not logged_in:
            what_to_do = Prompt.ask(Text.assemble(("1: Scroll up\n", "bold cyan"), ("2: Scroll down\n", "bold cyan"),
                                                  ("3: Select\n", "bold purple")), choices=["1", "2", "3"], default="3")
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
            if logged_in:
                if hover_on == 1:
                    try:
                        clear()
                        event = "box"
                        return event, logged_in_as  # Create/join box
                    except GoBack:
                        hover_on = 1
                        clear()
                        continue
                elif hover_on == 2:
                    try:
                        clear()
                        logged_in_as.preferences.settings()  # Preferences
                        hover_on = 1
                        clear()
                        continue
                    except GoBack:
                        hover_on = 1
                        clear()
                        continue
                elif hover_on == 3:
                    try:
                        clear()
                        help_page.help_start_page(logged_in_as)  # Help/Info
                        hover_on = 1
                        clear()
                        continue
                    except GoBack:
                        hover_on = 1
                        clear()
                        continue
                elif hover_on == 4:
                    try:
                        clear()
                        credits.credits_rework()  # Credits
                        hover_on = 1
                        clear()
                        continue
                    except GoBack:
                        hover_on = 1
                        clear()
                        continue
                elif hover_on == 5:
                    clear()
                    event = "exit"
                    return event, logged_in_as  # Replaced by exit function in client so the socket connection is properly closed.
                elif what_to_do == "out":
                    return await main_menu(logged_in=False, logged_in_as=None)
            if hover_on == 1:
                clear()
                return await main_menu(logged_in=True, logged_in_as=await login.login())
            elif hover_on == 2:
                try:
                    clear()
                    help_page.help_start_page(logged_in_as)  # Help/Info
                    hover_on = 1
                    clear()
                    continue
                except GoBack:
                    hover_on = 1
                    clear()
                    continue
            elif hover_on == 3:
                try:
                    clear()
                    credits.credits_rework()  # Credits
                    hover_on = 1
                    clear()
                    continue
                except GoBack:
                    hover_on = 1
                    clear()
                    continue
            elif hover_on == 4:
                clear()
                event = "exit"
                return event, logged_in_as  # Replaced by exit function in client so the socket connection is properly closed.
        

        clear()




import keyboard
import time
from utils import clear
from utils import GoBack
from rich import print
from rich.console import Console
from rich.prompt import Prompt
from rich.align import Align
import asyncio

console = Console()


async def help_navigation(currentpage, user):
    """
    Allows user to cycle through the help pages.
    """

    page_cycle: list = ["About", "Boxes", "Messages", "Pref"]
    currentpage: int = page_cycle.index(currentpage)

    if currentpage == 3:
        next: int = page_cycle[0]
        previous: int = page_cycle[2]

    elif currentpage == 0:
        next: int = page_cycle[1]
        previous: int = page_cycle[3]

    else:
        next: int = page_cycle[currentpage + 1]
        previous: int = page_cycle[currentpage - 1]

    console.print(
        "\n[bold white][bold red]![/]   Use [bold magenta] right arrow[/] or [bold magenta]left arrow[/] to navigate the page, or press [bold magenta]BACKSPACE[/] to return to Menu.[/]")

    # Adding delays between key presses so that the pages won't cyle through too fast.
    await asyncio.sleep(0.2)

    while True:
        if keyboard.is_pressed("left_arrow"):
            if previous == "About":
                await help_start_page(user)
                break

            elif previous == "Boxes":
                await help_boxes(user)
                break

            elif previous == "Messages":
                await help_messages(user)
                break

            elif previous == "Pref":
                await help_preference(user)
                break

        elif keyboard.is_pressed("right_arrow"):
            if next == "About":
                await help_start_page(user)
                break

            elif next == "Boxes":
                await help_boxes(user)
                break

            elif next == "Messages":
                await help_messages(user)
                break

            elif next == "Pref":
                await help_preference(user)
                break

        elif keyboard.is_pressed("backspace"):
            raise GoBack


async def help_start_page(user):
    if user is not None:
        main_style = user.preferences.preference_dict["Border Colour"]
    else:
        main_style = "bold cyan"
    clear()
    paragraph = "[bright_white]ThaBox is a social media platform in which the conversations " \
                "\nbetween users are for the users only. Not a single message is " \
                "\nsaved, giving you the utmost privacy. Chat with " \
                "\nstrangers in boxes, or have a blast with your friends " \
                "\nin boxes. " \
                "\n\n[/][bold grey58]This program was created for the 'Python Discord 2021 CodeJam'.\n[/]"

    paragraph = """
    [bright_white]ThaBox is a social media platform in which the conversations 
    between users are for the users only. Not a single message is
    saved, giving you the utmost privacy. Chat with
    strangers in boxes, or have a blast with your friends
    in boxes.
    
    [/][bold grey58]This program was created for the 'Python Discord 2021 CodeJam'.\n[/]
    """

    console.print((Align(f"""[{main_style}]
    ▄▀█ █▄▄ █▀█ █ █ ▀█▀
    █▀█ █▄█ █▄█ █▄█  █ [/]\n""", align="center", )))
    console.print((Align(paragraph, align="center")))
    await help_navigation('About', user)


async def help_boxes(user):
    if user is not None:
        main_style = user.preferences.preference_dict["Border Colour"]
    else:
        main_style = "bold cyan"
    clear()
    paragraph = "[bright_white]There is one type of box available." \
                "\When creating a box, it will check if a box of that name already exists, and" \
                "\nif it doesn't one will be created. However, if it does" \
                "\nexist, you will join the box and be able to start talking.\n[/]"
    paragraph = """
    [bright_white]There is one type of box available. 
    When creating a box, it will check if a box of that name already exists, and
    if it doesn't one will be created. However, if it does exist,
    you will join the box and be able to start talking.
    [/]
    """

    console.print((Align(f"""[{main_style}]
     █▄▄ █▀█ ▀▄▀ █▀▀ █▀
     █▄█ █▄█ █ █ ██▄ ▄█[/]\n""", align="center", )))
    console.print((Align(paragraph, align="center")))
    await help_navigation('Boxes', user)


async def help_messages(user):
    if user is not None:
        main_style = user.preferences.preference_dict["Border Colour"]
    else:
        main_style = "bold cyan"
    clear()
    paragraph = "[bright_white]Messages can be sent to another person in the same box, by simply"\
                "\ntyping it out when you receive the prompt. However"\
                "\nyou can only see the other people's messages after you"\
                "\nhave finished typing."\
                "\n\nMessages that you receive are available for some seconds."\
                "\nPast message are not stored and can't be "\
                "\nretrieved.\n[/]"
    paragraph = """
    [bright_white]Messages can be sent to another person in the same box, by simply
    typing it out when you receive the prompt. However you can only see the other 
    people's messages after you have finished typing.
    
    Messages that you receive are available for some seconds.
    message has been sent. Past message are not stored and can't be
    retrieved.
    [/]
    """

    console.print((Align(f"""[{main_style}]
    █▀▄▀█ █▀▀ █▀ █▀ ▄▀█ █▀▀ █▀▀ █▀
    █ ▀ █ ██▄ ▄█ ▄█ █▀█ █▄█ ██▄ ▄█[/]\n""", align="center", )))
    console.print((Align(paragraph, align="center")))
    await help_navigation("Messages", user)


async def help_preference(user):
    if user is not None:
        main_style = user.preferences.preference_dict["Border Colour"]
    else:
        main_style = "bold cyan"
    clear()
    paragraph = "[bright_white]The colour scheme of your box can be changed in the"\
                "\nPreferences page once logged in. A valid colour name or a hex-value (#xxxxxx)"\
                "\ncan be used to personalise different parts of your box. [/]\n"
    paragraph = """
    [bright_white]The colour scheme of your box can be changed in the
    Preferences page once logged in. A valid colour name or a hex-value (#xxxxxx)
    can be used to personalise different parts of your box. [/]
    
    """

    console.print((Align(f"""[{main_style}]
    █▀█ █▀█ █▀▀ █▀▀ █▀▀ █▀█ █▀▀ █▄ █ █▀▀ █▀▀ █▀
    █▀▀ █▀▄ ██▄ █▀  ██▄ █▀▄ ██▄ █ ▀█ █▄▄ ██▄ ▄█[/]\n""", align="center", )))
    console.print((Align(paragraph, align="center")))
    await help_navigation("Pref", user)


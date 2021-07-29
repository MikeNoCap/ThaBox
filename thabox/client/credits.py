import copy
from time import sleep
from rich.align import Align
from rich.live import Live
from rich.panel import Panel
from rich.text import Text
from utils import clear, GoBack

height: list = ['bottom', 'middle', 'top']

team_name: list = [
    '[purple]--------------------[/purple][magenta]This was built by:[/magenta]['
    'purple]--------------------[/purple] ',
    Text.assemble((r":                |$$$$$$$$| |$$| |$$| |$$$$$$|               :", 'bold purple'),
                  justify='center'),
    Text.assemble((r":                   |$$|    |$$| |$$| |$|                    :", 'bold purple'),
                  justify='center'),
    Text.assemble((r":                   |$$|    |$$$$$$$| |$$$$|                 :", 'bold purple'),
                  justify='center'),
    Text.assemble((r":                   |$$|    |$$| |$$| |$|                    :", 'bold purple'),
                  justify='center'),
    Text.assemble((":                   |$$|    |$$| |$$| |$$$$$$|               :\n", 'bold purple'),
                  justify='center'),

    Text.assemble((r":          |$| |$$$$$| |$$$$$| |$$$$$| |$$$$$| |$$$$$\       :", 'bold magenta'),
                  justify='center'),
    Text.assemble((r":          |$| |$$ $$|    /$$/    /$$/ |$|     |$$| \$\      :", 'bold magenta'),
                  justify='center'),
    Text.assemble((r":          |$| |$$$$$|   /$$/    /$$/  |$$$|   |$$| |$|      :", 'bold magenta'),
                  justify='center'),
    Text.assemble((r":       ___|$| |$| |$|  /$$/    /$$/   |$|     |$$| /$/      :", 'bold magenta'),
                  justify='center'),
    Text.assemble((":      |$$$$$| |$| |$| |$$$$$| |$$$$$| |$$$$$| |$$$$$/       :\n", 'bold magenta'),
                  justify='center'),

    Text.assemble((r":    |$| |$$$$$| |$$$$$\  |$$$$\   /$$$$$\  |$$$$$|  /$$$$$| :", 'bold purple'),
                  justify='center'),
    Text.assemble((r":    |$| |$|     |$$  $$| |$  $$| |$$   $$| |$$ $$| |$$\     :", 'bold purple'),
                  justify='center'),
    Text.assemble((r":    |$| |$$$|   |$$$$$/  |$$$$/  |$$   $$| |$$$$$|  \$$$$$\ :", 'bold purple'),
                  justify='center'),
    Text.assemble((r": ___|$| |$|     |$| \$\  |$  $$\ |$$   $$| |$| |$|      /$$|:", 'bold purple'),
                  justify='center'),
    Text.assemble((r":|$$$$$| |$$$$$| |$|  \$\ |$$$$$/  \$$$$$/  |$| |$|  |$$$$$/ :", 'bold purple'),
                  justify='center'),
    Text.assemble((r":____________________________________________________________:", 'bold purple'),
                  justify='center'),
]

jazzed_jerboas: list = [
    '\n\n[green]Teamleader| Discord: StormedPanda#9999 | GitHub: tomheaton | aka Tom |[/]\n\n',
    '\n\n[bold yellow]Teammember| Discord: Miklath#1000 | GitHub: MikeNoCap | aka Mike |[/]\n\n',
    '\n\n[bold yellow]Teammember | Discord: HiPeople21#6968 | GitHub: HiPeople21 |[/]\n\n',
    '\n\n[bold yellow]Teammember | Discord: Mega#6949 | GitHub: TahU28 |[/]\n\n',
    '\n\n[bold yellow]Teammember | Discord: Darling#9795 | GitHub: ryoflux |[/]\n\n',
    '\n\n[bold yellow]Teammember | Discord: babis99#8888 | GitHub: b-a-b-i-s |[/]\n\n']

message: list = [
    'We are very thankfull for getting to join this event. Special thanks to the Python Discord event-team\nfor taking their time off to manage and host this event.',
    '',
    'Placeholder'
]

rows_ = ["\n", "\n", "\n", "[bold white]-----------------------Credits-----------------------[/]", "\n",
         "\n", "\n", "[bold white]There will be stops along this ride so you can take your time to read.[/]"]
for i in range(9):
    rows_.append("")
for i in team_name:
    rows_.append(i)
for i in range(3):
    rows_.append("")
for i in jazzed_jerboas:
    rows_.append(i)
for i in range(12):
    rows_.append("")

for i in range(14):
    rows_.append("")
rows_.append("[bold blue]ThaBox was made as a submission for Python Discord's code-jam[/]")
rows_.append("[bold blue]and was developed by The Jazzed Jerboa's over the timespan of a week. [/]")
for i in range(2):
    rows_.append("")
rows_.append("[bold blue]We are very thankful for getting to join this event (Python code-jam Summer 2021). " \
             "Special thanks to the Python Discord event-team [/]")
rows_.append("[bold blue]for taking their time off to manage and host this event. [/]")
for i in range(2):
    rows_.append("")
rows_.append("[bold blue]Please don't look at The Jazzed Jerboa's as a team that submitted a project for the " \
             "Python code-jam Summer 2021,[/]")
rows_.append("[bold blue]but rather a team of wonderful people that shares the same interests. " \
             "Being a part of the team gives you a feeling that you really belong somewhere.[/]")
for i in range(2):
    rows_.append("")
rows_.append("[bold blue]During this event we have come a bit closer to mastering the art of collaboration.[/]")
rows_.append("[bold blue]It was super fun developing this! [/]")
for i in range(2):
    rows_.append("")
rows_.append("[bold blue]It's been a hell of a ride. [/]")
rows_.append("[bold blue]Enjoy our project! [/]")
for i in range(5):
    rows_.append("")

new_line = '\n'


def credits(console) -> None:
    """
    Displays the credits
    """
    with console.screen() as screen:
        rule: str = '[purple]--------------------[/purple][magenta]This was built by:[/magenta][' \
                    'purple]--------------------[/purple] '
        clear()
        text: Text = Align.center(
            Text.from_markup(
                f"{rule}", justify="center"),
            vertical=height[0],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(0.5)

        for j in range(len(team_name)):
            console.clear()
            text: Text = Align.center(
                Text.from_markup(
                    f"{rule}\n{new_line.join([str(i) for i in team_name[:j]])}", justify="center"),
                vertical=height[0],
            )
            screen.update(Panel(text, style="bold magenta", border_style="red"))

        for j in range(len(jazzed_jerboas) + 1):
            clear()
            text: Text = Align.center(
                Text.from_markup(
                    f"{rule}\n{new_line.join([str(i) for i in team_name])}\n{new_line.join([str(i) for i in jazzed_jerboas[:j]])}",
                    justify="center"),
                vertical=height[0],
            )
            screen.update(Panel(text, style="bold magenta", border_style="red"))
            sleep(0.5)

        clear()
        text: Text = Align.center(
            Text.from_markup(
                f"{rule}\n{new_line.join([str(i) for i in team_name])}\n{new_line.join([str(i) for i in jazzed_jerboas])}",
                justify="center"),
            vertical=height[1],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(0.5)

        clear()
        text: Text = Align.center(
            Text.from_markup(
                f"{rule}\n{new_line.join([str(i) for i in team_name])}\n{new_line.join([str(i) for i in jazzed_jerboas])}",
                justify="center"),
            vertical=height[2],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(0.5)

        clear()
        text: Text = Align.center(
            Text.from_markup(
                f"\n{new_line.join([str(i) for i in team_name])}\n{new_line.join([str(i) for i in jazzed_jerboas])}",
                justify="center"),
            vertical=height[2],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(0.5)

        for j in range(len(team_name)):
            clear()
            text: Text = Align.center(
                Text.from_markup(
                    f"{new_line.join([str(i) for i in team_name[j:]])}\n{new_line.join([str(i) for i in jazzed_jerboas])}",
                    justify="center"),
                vertical=height[2],
            )
            screen.update(Panel(text, style="bold magenta", border_style="red"))
            sleep(0.5)

        for j in range(len(jazzed_jerboas) + 1):
            clear()
            text: Text = Align.center(
                Text.from_markup(
                    f"{new_line.join([str(i) for i in jazzed_jerboas[j:]])}", justify="center"),
                vertical=height[2],
            )
            screen.update(Panel(text, style="bold magenta", border_style="red"))
            sleep(0.5)
        sleep(8)

        clear()
        text: Text = Align.center(
            Text.from_markup(
                "", justify="center"),
            vertical=height[2],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(0.5)

        for j in range(len(message) + 1):
            clear()
            text: Text = Align.center(
                Text.from_markup(
                    f"{new_line.join([str(i) for i in message[:j]])}", justify="center"),
                vertical=height[0],
            )
            screen.update(Panel(text, style="bold magenta", border_style="red"))
            sleep(1)

        clear()
        text: Text = Align.center(
            Text.from_markup(
                f"{new_line.join([str(i) for i in message])}", justify="center"),
            vertical=height[1],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(1)

        for j in range(len(message)):
            clear()
            text: Text = Align.center(
                Text.from_markup(
                    f"{new_line.join([str(i) for i in message[j:]])}", justify="center"),
                vertical=height[2],
            )
            screen.update(Panel(text, style="bold magenta", border_style="red"))
            sleep(1)

        clear()
        text: Text = Align.center(
            Text.from_markup(
                "", justify="center"),
            vertical=height[2],
        )
        screen.update(Panel(text, style="bold magenta", border_style="red"))
        sleep(0.5)
        clear()


def credits_rework() -> None:
    rows = copy.deepcopy(rows_)
    with Live("", refresh_per_second=9) as screen:

        loop_times = 0  # Keep track of where in rows we are so we can stop at a specific point

        while len(rows) != 0:
            loop_times += 1
            rows.pop(0)

            scroll_through = Align.center(
                Text.from_markup(
                    "".join(
                        [x + "\n" if not isinstance(x, Text) else Text.assemble((x))._text[1] + "\n" for x in rows]),
                    justify="center"
                )
            )

            screen.update(Panel(scroll_through, border_style="bold red", style="bold magenta"))
            if loop_times == 3:
                for i in range(6):
                    screen.update(Panel(scroll_through, border_style="bold yellow", style="bold magenta"))
                    sleep(1)
            if loop_times == 37:
                for i in range(10):
                    screen.update(Panel(scroll_through, border_style="bold yellow", style="bold magenta"))
                    sleep(1)
            if loop_times == 65:
                for i in range(32):
                    screen.update(Panel(scroll_through, border_style="bold yellow", style="bold magenta"))
                    sleep(1)
            if loop_times == 78:
                for i in range(9):
                    screen.update(Panel(scroll_through, border_style="bold yellow", style="bold magenta"))
                    sleep(1)

            sleep(0.4)
    clear()


def skip_credits():
    raise GoBack

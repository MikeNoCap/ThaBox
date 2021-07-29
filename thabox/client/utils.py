import os
import time

from rich.console import Console
from rich.markdown import Markdown
from rich.panel import Panel
from rich.prompt import Prompt
from rich.text import Text

console: Console = Console()


class Preferences:
    """
    This needs to be passed onto the 'User' class as it sets the default preferences:
    'sampleuser = User("samplename", "password", default_preference)'

    default_preference = {
        "Name Colour" : "bold cyan",
        "Message Colour" : "bold white",
        "Border Colour" : "bold magenta"
    }

    To change the preference, this is used:
    'sampleuser.preferences = Preferences.settings(sampleuser.preferences)'
    *Note: this only allows for one settings to be changed, so a while loop would need
    to be used to allow multiple settings be to changed.
    """

    def __init__(self):
        self.preference_dict = default_preference = {
            "Name Colour": "bold cyan",
            "Message Colour": "bold white",
            "Border Colour": "bold purple",
            "Message Border Colour": "bold magenta",
        }

    def template_message(self) -> None:
        """
        Function which prints out a preview of how the users box is going to look.
        """
        message_preview = f"""[{self.preference_dict["Message Border Colour"]}]┌────────────────────────────────┐[/]
[{self.preference_dict["Message Border Colour"]}]│{"Message from" : ^32}│[/]
[{self.preference_dict["Message Border Colour"]}]│[/][{self.preference_dict["Name Colour"]}]{"Preview" : ^32}[/][{self.preference_dict["Message Border Colour"]}]│[/]
[{self.preference_dict["Message Border Colour"]}]├────────────────────────────────┤[/]
[{self.preference_dict["Message Border Colour"]}]│[/][{self.preference_dict["Message Colour"]}]This is what a message looks[/]    [{self.preference_dict["Message Border Colour"]}]│[/]
[{self.preference_dict["Message Border Colour"]}]│[/][{self.preference_dict["Message Colour"]}]like with your current[/]          [{self.preference_dict["Message Border Colour"]}]│[/]
[{self.preference_dict["Message Border Colour"]}]│[/][{self.preference_dict["Message Colour"]}]preferences.[/]                    [{self.preference_dict["Message Border Colour"]}]│[/]
[{self.preference_dict["Message Border Colour"]}]└────────────────────────────────┘[/]"""
        console.print(Panel(message_preview, border_style=self.preference_dict["Border Colour"]))

    def settings(self):
        """
        Function which allows the user to change thier settings. Allows hex and named
        colour values and returns then updated preference.
        """
        while True:
            Preferences.template_message(self)
            val_to_be_changed: str = make_style_prompt(prompt_msg="What would you like to change?",
                                                       choices=["Border Colour", "Name Colour", "Message Colour",
                                                                "Message Border Colour", "[red]Exit preferences[/]"],
                                                       main_style=self.preference_dict["Message Border Colour"],
                                                       frame_border_style=self.preference_dict["Border Colour"])
            clear()
            if val_to_be_changed == "[red]Exit preferences[/]":
                raise GoBack

            else:
                while True:
                    console.print(Panel("🎨 Name a color or enter a hex-value",
                                        border_style=self.preference_dict["Message Border Colour"]))
                    colour: str = Prompt.ask(Text.assemble(("╰>", self.preference_dict["Message Colour"])))
                    try:
                        test: str = console.print("", style=colour)
                    except:
                        clear()
                        console.print("❌   Please enter a valid colour!\n")
                        time.sleep(2.2)
                        clear()
                    else:
                        previous_setting: str = self.preference_dict[val_to_be_changed]
                        self.preference_dict[val_to_be_changed] = "bold " + str(colour)
                        console.print("✔️   Updated successfully!\n")
                        time.sleep(2.2)
                        # update_userfiles()
                        clear()
                        break


class User:
    def __init__(self, username: str, paswrd: str, preferences: Preferences):
        self.username = username
        self.hashed_pass = paswrd
        self.preferences = preferences
        self.friends = []


class GoBack(Exception):
    pass


def make_style_prompt(choices: list, default: str = None, prompt_msg: str = "Would you like to:",
                      main_style: str = "none",
                      frame_style: str = "none",
                      frame_border_style: str = "none") -> str:
    """
    Prompts user in a cool way and retrieves what the user picked.

    :param choices: A list of choices.
    :param default: The value that gets returned if user doesn't type anything in.
    :param prompt_msg: The message being printed before the choices.
    :param main_style: The main theme/color of the prompt.
    :param frame_style: The theme/color for the text in the panels.
    :param frame_border_style: The theme/color for the frame in the panels.
    :return: str value of final style choice the user selected.
    """
    choices = [str(i) for i in choices]
    if default is not None:
        # Get index of default so it can be set to the default choice.
        default_index = str(choices.index(default) + 1)
    else:
        default_index = None

    choices_styled = []
    c = 0
    for i in choices:
        c += 1
        choices_styled.append(Panel(f"{c}. {i}", style=frame_style, border_style=frame_border_style))

    console.print(Panel(prompt_msg.replace("\n", ""), style=main_style, border_style=main_style))
    for i in choices_styled:
        console.print(i)

    choice_index = Prompt.ask(Text.assemble(("╰>", main_style)), choices=[str(x) for x in range(1, c + 1)],
                              default=default_index)
    choice_index = int(choice_index)
    return choices[choice_index - 1]


def clear() -> int:
    """
    Clears terminal
    """
    return os.system('cls' if os.name == 'nt' else 'clear')

from rich.console import Console
from rich.text import Text 
from rich.live import Live
from rich.panel import Panel
import os, sys
import time


print_string = "[a]Hope[/][b] you[/][a] had[/][b] a[/][a] great[/][b] time![/]"
s1 = print_string.replace("[a]", "[cyan]").replace("[b]", "[magenta]")
s2 = print_string.replace("[a]", "[magenta]").replace("[b]", "[cyan]")


frames = []

extra = ""
s = ""

for i in range(30):
    x = s1 if i % 2 == 0 else s2
    frames.append(Panel(extra+s+x, height=32, width=90))
    s += " "
    extra += "\n"
for i in range(30):
    x = s1 if i % 2 == 0 else s2
    s+=" "
    extra = extra[:-1]
    frames.append(Panel(extra+s+x, height=32, width=90))
frames.append(Panel("", height=32, width=90))
console = Console()
os.system("cls" if os.name == "nt" else "clear")


with Live(refresh_per_second=10) as l:
    for i in frames:
        time.sleep(0.15)
        
        l.update(i)


    
sys.exit(1)

    
    
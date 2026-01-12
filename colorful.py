import os
import sys
import builtins
import subprocess

from typing import ClassVar

##################
## Terminal Fix ##
##################
if os.name == "nt":
  try:
    import colorama
    colorama.just_fix_windows_console()
  except ImportError:
    print("[ERROR]: 'colorama' has not been found on your system, but you're using Windows.")
    while True:
      res = input("[ERROR]: continue (y/n)? ")
      if res == 'y':
        break
      elif res == 'n':
        sys.exit(1)

####################
## Shell Coloring ##
####################
def fore(r: int, g: int, b: int) -> str:
  return f'\x1b[38;2;{r};{g};{b}m'

def back(r: int, g: int, b: int) -> str:
  return f'\x1b[48;2;{r};{g};{b}m'

######################
## Formatting Codes ##
######################
class f:
  select: ClassVar = fore(115, 115, 115)
  reset: ClassVar = f'\x1b[0m'
  gold: ClassVar = fore(155, 125, 0)
  blue: ClassVar = fore(55, 95, 115)

###########
## print ##
###########
def print(text: str = "") -> str:
  for name in f.__dict__:
    if name.startswith('_'):
      continue

    text = text.replace("{%s}" % name, f.__dict__[name])

  builtins.print(text + f.reset)

def cls() -> None:
  # im lazy alright
  subprocess.run("cls" if os.name == "nt" else "clear", shell=True)

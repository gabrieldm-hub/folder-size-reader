import os

if os.name == 'nt':
    os.system('color')

BLACK = "\u001b[30;1m"
RED = "\u001b[31;1m"
GREEN = "\u001b[32;1m"
YELLOW = "\u001b[33;1m"
BLUE = "\u001b[34;1m"
MAGENTA = "\u001b[35;1m"
CYAN = "\u001b[36;1m"
WHITE = "\u001b[37;1m"

BOLD = "\u001b[1m"
UNDERLINE = "\u001b[4m"
REVERSED = "\u001b[7m"

RESET = "\u001b[0m"
CLEAR = "\033[K"
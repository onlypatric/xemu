from datetime import datetime
import os
import platform
import socket
from colorama import Back, Fore, Style
from .login import login


formatOptions = {
    "$T1": f"{Fore.RESET}",
    "$T2": f"{Fore.GREEN}",
    "$T3": f"{Fore.CYAN}",
    "$T4": f"{Fore.BLUE}",
    "$T5": f"{Fore.BLACK}",
    "$T6": f"{Fore.RED}",
    "$T7": f"{Fore.YELLOW}",
    "$T8": f"{Fore.MAGENTA}",
    "$T9": f"{Fore.WHITE}",
    "$R1": f"{Back.RESET}",
    "$R2": f"{Back.GREEN}",
    "$R3": f"{Back.CYAN}",
    "$R4": f"{Back.BLUE}",
    "$R5": f"{Back.BLACK}",
    "$R6": f"{Back.RED}",
    "$R7": f"{Back.YELLOW}",
    "$R8": f"{Back.MAGENTA}",
    "$R9": f"{Back.WHITE}",
    "$U1": f"{Style.NORMAL}",
    "$U2": f"{Style.BRIGHT}",
    "$U3": f"{Style.DIM}",
    "$U4": f"{Style.RESET_ALL}",
    "$_": "\n",
    "$$": "$",
    "$A": "&",
    "$B": "|",
    "$CH0": "(",
    "$D": datetime.now().strftime("%D"),
    "$F": ")",
    "$G": ">",
    "$H": "~",
    "$I": login(),
    "$J": socket.gethostname(),
    "$L": "<",
    "$N": f"{os.getcwd().split(':')[0]}",
    "$M": f"{os.getcwd()}",
    "$O": "/{0}/".format(os.getcwd().replace("\\", "/").split("/")[-1]),
    "$P": "=",
    "$Q": " ",
    "$S": datetime.now().strftime("%T"),
    "$V": f"{platform.version()}",
    "$CH1": "§",
    "$CH2": "✓",
    "$CH3": "✕",
    "$CH4": "⋆",
    "$CH5": "✶",
    "$CH6": "⌥",
    "$CH7": "⌘",
    "$CH8": "⏻",
    "$CH9": "⏼",
    "$CR1": "⎞",
    "$CR2": "⎜",
    "$CR3": "⎝",
    "$CR4": "⎛",
    "$CR5": "⎟",
    "$CR6": "⎠",
    "$CR7": "⭘",
    "$CR8": "⋯",
    "$CR9": "⊸",
}


def update():
    formatOptions.update({
        "$N": f"{os.getcwd().split(':')[0]}",
        "$M": f"{os.getcwd()}",
        "$O": "/{0}/".format(os.getcwd().replace("\\", "/").split("/")[-1]),
        "$S": datetime.now().strftime("%T"),
        "$V": f"{platform.version()}",
    })

def formatStr(string:str) -> str:
    for a,b in formatOptions.items():
        string=string.replace(a,b);
    return string;
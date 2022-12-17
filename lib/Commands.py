from colorama import Fore,Style,Back,init
import sys
def run():
    _TEXT=f"""
{Fore.GREEN}X-Runner {Fore.LIGHTBLACK_EX}| {Fore.YELLOW}Script executor{Fore.RESET}
run <filename>
{' '*3}1 - C,C++ files
{' '*6}Requires {Back.YELLOW}{Fore.BLACK}GCC/G++ {Style.BRIGHT}compiler{Style.NORMAL}{Back.RESET}{Fore.RESET}
{' '*3}2 - Assembly (.s) files
{' '*6}Requires {Back.YELLOW}{Fore.BLACK}GCC {Style.BRIGHT}compiler{Style.NORMAL}{Back.RESET}{Fore.RESET}
{' '*3}3 - Java files
{' '*6}Requires {Back.MAGENTA}{Fore.BLACK}JDK {Style.BRIGHT}Pack{Style.NORMAL}{Back.RESET}{Fore.RESET}
{' '*3}4 - javascript nodeJS files
{' '*6}Requires {Back.GREEN}{Fore.BLACK}NodeJS {Style.BRIGHT}Interpreter{Style.NORMAL}{Back.RESET}{Fore.RESET}
{' '*3}5 - python 3.x.x files (headless and no-headless)
{' '*6}Requires {Back.GREEN}{Fore.BLACK}Python {Style.BRIGHT}Interpreter{Style.NORMAL}{Back.RESET}{Fore.RESET}
Examples:
1 - {Fore.LIGHTCYAN_EX}{Back.RED}run main.c{Fore.RESET}{Back.RESET}
2 - {Fore.LIGHTCYAN_EX}{Back.RED}run main.py{Fore.RESET}{Back.RESET}
{Style.DIM}and so on...{Style.NORMAL}
"""
    sys.stdout.write(_TEXT)
def prompt():
    _TEXT=f"""{Fore.GREEN}Xemu {Fore.MAGENTA}prompt editor{Fore.RESET}
{Back.GREEN}This command has a built-in help section{Back.RESET}
Type:
{' '*3}{Style.BRIGHT}prompt --help{Style.NORMAL}
"""
    sys.stdout.write(_TEXT)
def clear():
    _TEXT="""Clears the Console-Host window that has been opened\nNo parameters in need to be specified or settings...\n"""
    sys.stdout.write(_TEXT)
def chdir():
    sys.stdout.write("""NAME 
    chdir

SYNTAX
    chdir <AbsPath|RelPath|Path>

ALIAS
    cd
    navdir
""")
def shdir():
    """"""
def shdir():
    """"""
def shdir():
    """"""
def byteTForm():
    """Transforms given byte amount (either B,KB,MB,GB,TB,PB) into all the byte forms\ntry:\nbyte 1TB\n"""
def TerminalEditor():
    sys.stdout.write(f"""{Fore.GREEN}Xemu Editor{Fore.RESET}
Have you ever tried linux's nano application?
XEditor is a somewhat adapted for windows terminal text editor,
for the people who love lightweight editors that are easy to use

command arguments are followings:
   {Style.BRIGHT}<file>{Style.NORMAL}
      required  :no
      default   :untilted.txt
      type      :text/string/path
    #specify what file is software pointing to
   {Style.BRIGHT}[-r | --read]{Style.NORMAL}
      required  :no
      default   :False (not set)
      type      :boolean
    #Read only mode
   {Style.BRIGHT}[-b | --box]{Style.NORMAL}
      required  :no
      default   :False (not set)
      type      :boolean
    #Shows a somewhat box around the file
   {Style.BRIGHT}[--lines=<int>]{Style.NORMAL}
      required  :no
      default   :Infinite
      type      :integer
    #How many lines maximum
""".replace("required",f"{Fore.RED}required{Fore.RESET}").replace("default",f"{Fore.GREEN}default{Fore.RESET}").replace("type",f"{Fore.BLUE}type{Fore.RESET}").replace("False",f"{Fore.BLUE}False{Fore.RESET}").replace("True",f"{Fore.BLUE}True{Fore.RESET}").replace(f"<int>",f"<{Fore.YELLOW}int{Fore.RESET}>").replace("|",f"{Fore.RED}|{Fore.RESET}").replace("-",f"{Fore.RED}-{Fore.RESET}").replace("<",f"{Fore.CYAN}<{Fore.RESET}").replace(">",f"{Fore.CYAN}>{Fore.RESET}").replace("int\n",f"{Fore.YELLOW}int\n{Fore.RESET}").replace("integer\n",f"{Fore.YELLOW}integer\n{Fore.RESET}").replace("boolean\n",f"{Fore.YELLOW}boolean\n{Fore.RESET}").replace("text/string/path\n",f"{Fore.YELLOW}text/string/path\n{Fore.RESET}"))
def help():
    sys.stdout.write("""This command right here""")
def exit():
    sys.stdout.write("""Exits the terminal and returns 0""")
if __name__=="__main__":
    init(True)
    TerminalEditor()
import curses,sys
import os
from editor.editor import Editor
from colorama import Fore

def showHelp():
    help_txt = (f" Save and exit         {Fore.CYAN}:{Fore.RESET} F2 or Ctrl-x\n"
                f"            (Enter if in single-line entry mode)\n"
                f" Exit (no save)        {Fore.CYAN}:{Fore.RESET} F3, Ctrl-c or ESC\n"
                f" Cursor movement       {Fore.CYAN}:{Fore.RESET} Arrow keys/Ctrl-f/b/n/p\n"
                f" Beginning of line     {Fore.CYAN}:{Fore.RESET} Home/Ctrl-a\n"
                f" End of line           {Fore.CYAN}:{Fore.RESET} End/Ctrl-e\n"
                f" Page Up/Page Down     {Fore.CYAN}:{Fore.RESET} PgUp/PgDn\n"
                f" Backspace/Delete      {Fore.CYAN}:{Fore.RESET} Backspace/Ctrl-h\n"
                f" Delete current char   {Fore.CYAN}:{Fore.RESET} Del/Ctrl-d\n"
                f" Insert line at cursor {Fore.CYAN}:{Fore.RESET} Enter\n"
                f" Paste block of text   {Fore.CYAN}:{Fore.RESET} Ctrl-v\n"
                f" Delete to end of line {Fore.CYAN}:{Fore.RESET} Ctrl-k\n"
                f" Delete to BOL         {Fore.CYAN}:{Fore.RESET} Ctrl-u\n")
    help_txt_no = (
                f" Quit                  {Fore.CYAN}:{Fore.RESET} q,F2,F3,ESC,Ctrl-c or Ctrl-x\n"
                f" Cursor movement       {Fore.CYAN}:{Fore.RESET} Arrow keys/j-k/Ctrl-n/p\n"
                f" Page Up/Page Down     {Fore.CYAN}:{Fore.RESET} J/K/PgUp/PgDn/Ctrl-b/n\n")
    sys.stdout.write(help_txt)
    sys.stdout.write("\n\tFor read only mode:\n\n")
    sys.stdout.write(help_txt_no)

class _Editor:
    def __init__(self,fName:"str|None"=None) -> None:
        self.size=(20,80)
        try:
            self.size=(os.get_terminal_size().lines,os.get_terminal_size().columns)
        except:pass
        if fName==None:
            fName="untilted.txt"
        self.fName=fName
        if not os.path.exists(self.fName):
            try:
                open(self.fName,"x")
            except:
                self.fName="untilted.txt"
                open(self.fName,"x")
        self.fName=fName
        curses.wrapper(self.main)

    def main(self,stdscr):
        self.editor=Editor(stdscr,title="XEditor",box=False,win_size=self.size,win_location=(5,5),save=self.save)
        try:
            self.editor()
        except KeyboardInterrupt:pass
        except:pass
        self.save()

    def save(self):
        try:
            if not os.path.exists(self.fName):
                try:
                    open(self.fName,"x")
                except:
                    self.fName="untilted.txt"
                    open(self.fName,"x")
            open(self.fName,"w").write(self.getText())
        except Exception as e:
            print(e)
    def getText(self):
        r="\n".join([i for i in ["".join(j) for j in self.editor.text]])

        return r

if __name__=="__main__":
    _Editor("untilted.txt")
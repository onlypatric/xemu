import os
import sys
from pynput import keyboard
from pynput.keyboard import Key
from colorama import Fore, Style,init,Back
init();
class ChoiceInput:
    def __init__(self,choices:"list[str]",colored:bool=False,color=Back.CYAN,up:Key=Key.up,down:Key=Key.down) -> None:
        self.stopped=False
        self.lines=len(choices);
        self.up=up
        self.down=down
        self.index=0;
        self.choices=choices;
        self.colored=colored;
        self.color=color;
        self.focuses=[False for i in choices]
        self.focuses.insert(self.index,not self.focuses.pop(self.index))
        self.update()
        with keyboard.Listener(on_press=self.on_release,suppress=True) as listener:
            listener.join()
        while not self.stopped:
            pass
    def get(self):
        return self.choices[self.index]
    def update(self):
        for a,b in zip(self.choices,self.focuses):
            if b:
                if self.colored:
                    sys.stdout.write(f"{self.color}{a}\n{Back.RESET+Fore.RESET+Style.NORMAL}")
                else:
                    sys.stdout.write(f"({a})\n")
            else:sys.stdout.write(f"{a}  \n")
            sys.stdout.flush()
    def on_release(self,key):
        if key == self.up:
            self.index-=1
            if self.index<0:
                self.index=0;
                return
            sys.stdout.write("\r\033[A"*self.lines)
            if self.lines>=os.get_terminal_size().lines:
                sys.stdout.write("\033[2J\033[H\033c")
                sys.stdout.flush()
            self.focuses.insert(self.index,self.focuses.pop(self.index+1))
            self.update()
            return None

        elif key == self.down:
            if self.index == self.lines-1:
                self.index=0
            else:self.index+=1
            sys.stdout.write("\r\033[A"*self.lines)
            if self.lines>=os.get_terminal_size().lines:
                sys.stdout.write("\033[2J\033[H\033c")
                sys.stdout.flush()
            self.focuses.insert(self.index,self.focuses.pop(self.index-1))
            self.update()
            return None
        elif key==Key.enter:
            self.stopped=True
            return False
        elif key == Key.esc or key==Key.end or key==Key.right: 
            self.stopped=True
            keyboard.Controller().press(Key.enter)
            return False

if __name__=="__main__":
    print(ChoiceInput(["1 - select something","2 - delete something else","3 - create something"]).get())
#! /usr/bin/python3
import os,sys,ArgumentParser,appdirs,json
from colorama import Fore, init
from pynput.keyboard import Key,KeyCode
from lib import formats,login
import ChoiceInput as CI
from pathlib import Path
from const import ERR

init(1)


class Console:

# ---------------------- initialize default variables
    def __init__(self) -> None:

        self.setCommands();
        self.execute(["clear"])
        self.variables = {
            "#FORMAT": "$T2$L$T4$I$T2$G$T7$T6$U3$CR8$U1$T4$J$T9$Q$U3[$T7$O$T9]$U1$U2$U2$Q$T6$CH7$T1$Q$T8$CH1$Q$T2$CH6$Q$T7$U1$G$G$G$T1$Q",
            "#SHOWCODE": "False",
            "#SILENT":"False",
            "#PATH":os.environ["PATH"],
            "#CWD":os.getcwd(),
        }
        self.dir=appdirs.user_data_dir("xemu","GrowPlan","1.0")
        self.home=str(Path.home().absolute())
        self.execute(["cd",self.home])
        if not os.path.exists(self.dir):
            try:
                os.makedirs(self.dir)
                open(self.dir+"/config.json","w").write(json.dumps(self.variables))
            except:pass
        else:
            try:
                self.variables.update( 
                    json.load(open(self.dir+"/config.json"))
                )
            except:pass
# ---------------------- setup default commands
    def setCommands(self):
        self.commands={
            "clear":lambda:self.clear(),
            "cd":lambda:self.chdir(),
            "exit":lambda:sys.exit(0),
        }
# ---------------------- Clear console command
    def clear(self):
        sys.stdout.write("\033[2J\033[H\033c")
        sys.stdout.flush()
# ---------------------- Change Dir command
    def chdir(self):
        dir_=self.get(self.last_params,0,None)
        if dir_==None:
            sys.stdout.write(f"{Fore.GREEN}<{Fore.CYAN}W{Fore.GREEN}>{Fore.WHITE} - Go up\n{Fore.GREEN}<{Fore.CYAN}S{Fore.GREEN}>{Fore.WHITE} - Go down{Fore.RESET}\n")
            dir_=CI.ChoiceInput(os.listdir(os.getcwd()),True,up=KeyCode.from_char("w"),down=KeyCode.from_char("s")).get()
        if os.path.exists(dir_) and os.path.isdir(dir_):
            os.chdir(dir_)
        
    def execute(self,parameters:"list[str]"=None,settings:"dict[str,str]"=None):
        if settings is None:
            try:settings:"dict[str,str]" = self.parsed[0]
            except:pass
        if parameters is None:
            try:parameters:"list[str]" = self.parsed[1]
            except:pass
        command=parameters.pop(0)
        self.last_settings=settings
        self.last_params=parameters
        self.last_command=command
        for name,func in self.commands.items():
            if name==command:
                func()
                break;
        else:
            CODE=os.system(self.last)
            if not CODE:
                pass
            else:sys.stdout.write(ERR)
    def update(self):
        self.variables.update(
            {
                "#CWD":os.getcwd(),
            }
        )
    def run(self):
        while True:
            try:
                sys.stdout.write(formats.formatStr(self.variables.get("#FORMAT")))
                self.last=input()
                self.parsed=[ArgumentParser.FindSettings(self.last),ArgumentParser.FindParams(self.last)]
                self.execute()
                formats.update()
                self.update()
            except KeyboardInterrupt:
                pass
    
    def get(self,arr,idx,_def):
        try:
            return arr[idx]
        except:
            return _def


if __name__=="__main__":
    console=Console()
    console.run()
#! /usr/bin/python3
import os,sys,ArgumentParser,appdirs,json
from colorama import Back, Fore, Style, init
from pynput.keyboard import Key,KeyCode
from lib import formats,login
import CInput as CI
from pathlib import Path
from const import *

init(1)


class Console:

# ---------------------- initialize default variables
    def __init__(self) -> None:

        self.home=str(Path.home().absolute())
        if(type(self.get(sys.argv,1,False))==str and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1])):
                os.chdir(sys.argv[1])
        else:
            os.chdir(self.home)
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
            "run":self.runFile,
            "prompt":self.prompt,
            "clear":self.clear,
            "cd":self.chdir,
            "exit":lambda:sys.exit(0),
        }
# ---------------------- Clear console command
    def clear(self):
        sys.stdout.write("\033[2J\033[H\033c")
        sys.stdout.flush()
# ---------------------- Configure prompt command
    def prompt(self):
        if(self.last_settings.get("help",False)):
            idx=0;
            for kw,val in formats.formatOptions.items():
                idx+=1
                if val.startswith("\033"):
                    sys.stdout.write(f"{Style.BRIGHT}%-5s\t%s{Style.NORMAL}"%(kw,val+"text"+Fore.RESET+Back.RESET+Style.NORMAL))
                else:
                    sys.stdout.write(f"{Style.BRIGHT}%-5s%20s{Style.NORMAL}"%(kw,str(((val[:16] + '-...') if len(val) > 16 else val).replace("\n","\\n"))))
                if idx%2==0:
                    sys.stdout.write("\n")
                else:
                    sys.stdout.write(f"{Fore.LIGHTBLACK_EX}|{Fore.RESET}")
            sys.stdout.write("\n")
# ---------------------- Change Dir command
    def chdir(self):
        dir_=self.get(self.last_params,0,None)
        if dir_==None:
            sys.stdout.write(f"{Fore.GREEN}<{Fore.CYAN}W{Fore.GREEN}>{Fore.WHITE} - Go up\n{Fore.GREEN}<{Fore.CYAN}S{Fore.GREEN}>{Fore.WHITE} - Go down{Fore.RESET}\n")
            dir_=CI.ChoiceInput([i for i in os.listdir(os.getcwd()) if os.path.isdir(os.getcwd()+"/"+i)],True,up=Key.up,down=Key.down,color=Style.BRIGHT+Fore.MAGENTA+Back.CYAN).get()
        if os.path.exists(dir_) and os.path.isdir(dir_):
            os.chdir(dir_)
# ---------------------- Run some files command
    #TODO: Finish globally run script files
    def runFile(self):
        if(self.last_params == []):
            sys.stdout.write(f"NO_FILE_EXCEPTION: {NO_FILE_ERR}")
            return;
        scriptName=self.last_params[0]

    def execute(self,parameters:"list[str]"=None,settings:"dict[str,str]"=None):
        formats.update()
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
                sys.stdout.write(f"Executing function {name}\n")
                func()
                break;
        else:
            CODE=os.system(self.last)
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
                sys.stdout.write("\n")
                pass
    
    def get(self,arr,idx,_def):
        try:
            return arr[idx]
        except:
            return _def


if __name__=="__main__":
    console=Console()
    console.run()
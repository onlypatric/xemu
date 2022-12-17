#! /usr/bin/python3
import datetime
from colorama import Back, Fore, Style, init
from pynput.keyboard import Key,KeyCode
from lib import formats,login,txtEditorHelper as xEditor,Commands
from pathlib import Path
from const import *
import os,sys,ArgumentParser,appdirs,json
import CInput as CI,subprocess as pwsh
import pynput.keyboard as kb

init(1)

const={}

defaultPrompt={
    "#FORMAT": "$T2$L$T4$I$T2$G$T7$T6$U3$CR8$U1$T4$J$T9$Q$U3[$T7$O$T9]$U1$U2$U2$Q$T6$CH7$T1$Q$T8$CH1$Q$T2$CH6$Q$T7$U1$G$G$G$T1$Q",
}


# some list chunk checking
def chunks(xs, n) -> int:
    n = max(1, n)
    return (xs[i:i+n] for i in range(0, len(xs), n))

class Console:

# ---------------------- check if user set to silent mode
    def isSilent(self) -> bool:
        return self.get(self.variables,"#SILENT","False")
# ---------------------- check if user set to not show code mode
    def showCode(self) -> bool:
        return self.get(self.variables,"#SHOWCODE","False")
# ---------------------- initialize default variables
    def __init__(self) -> None:
        self.prc=None
        self.variables = {
            "#FORMAT": "$T2$L$T4$I$T2$G$T7$T6$U3$CR8$U1$T4$J$T9$Q$U3[$T7$O$T9]$U1$U2$U2$Q$T6$CH7$T1$Q$T8$CH1$Q$T2$CH6$Q$T7$U1$G$G$G$T1$Q",
            "#SHOWCODE": "False",
            "#CODE": "NULL",
            "#SILENT":"False",
            "#PATH":os.environ["PATH"],
            "#CWD":os.getcwd(),
        }

        self.home=str(Path.home().absolute())
        self.variables.update({
            "#HOME":self.home
        })
        if(type(self.get(sys.argv,1,False))==str and os.path.exists(sys.argv[1]) and os.path.isdir(sys.argv[1])):
                os.chdir(sys.argv[1])
        else:
            os.chdir(self.home)
        self.setCommands();
        self.execute(["clear"])
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
    def setHelp(self):
        self.helpCommas={
            "run":Commands.run,
            "prompt":Commands.prompt,
            "clear":Commands.clear,
            "cd":Commands.chdir,
            "chdir":Commands.chdir,
            "navdir":Commands.chdir,
            "List-Dir":Commands.shdir,
            "dir":Commands.shdir,
            "ls":Commands.shdir,
            "byte":Commands.byteTForm,
            "xed":Commands.TerminalEditor,
            "Xemu-Editor":Commands.TerminalEditor,
            "xe":Commands.TerminalEditor,
            "xhelp":Commands.help,
            "exit":Commands.exit,
        }
    def setCommands(self):
        self.commands={
            "run":self.runFile,
            "prompt":self.prompt,
            "clear":self.clear,
            "cd":self.chdir,
            "chdir":self.chdir,
            "navdir":self.chdir,
            "List-Dir":self.shdir,
            "dir":self.shdir,
            "ls":self.shdir,
            "byte":self.byteTForm,
            "xed":self.TerminalEditor,
            "Xemu-Editor":self.TerminalEditor,
            "xe":self.TerminalEditor,
            "xhelp":self.help,
            "exit":lambda:sys.exit(0),
        }
# ---------------------- Clear console command
    def clear(self):
        sys.stdout.write("\033[2J\033[H\033c")
        sys.stdout.flush()
# ---------------------- Configure prompt command
    def prompt(self):
        if(self.last_settings.get("help",False) or self.last_settings.get("h",False)):
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
            sys.stdout.write("\n\nType:\n  -  prompt set <string>\nto format to your needs the output prompt\n  -  prompt default \nreset shown prompt to default one\n")
        elif self.get(self.last_params,0,None)=="set":
            newPrompt=self.get(self.last_params,1,None)
            if newPrompt is not None:
                self.variables.update({
                    "#FORMAT":newPrompt
                })
        elif self.get(self.last_params,0,None) in ["default","reset"]:
            self.variables.update(
                defaultPrompt
            )
        if self.last_settings.get("c",False) or self.last_settings.get("clear",False):
            self.execute(["clear"],{})
# ---------------------- Change Dir command
    def chdir(self):
        dir_=self.get(self.last_params,0,None)
        if self.last_settings.get("current",False) or self.last_settings.get("c",False):
            sys.stdout.write("%s"%(os.getcwd()))
            return;
        if dir_==None:
            sys.stdout.write(f"{Fore.GREEN}<{Fore.CYAN}PgUp{Fore.GREEN}>{Fore.WHITE} - Go up\n{Fore.GREEN}<{Fore.CYAN}PgDn{Fore.GREEN}>{Fore.WHITE} - Go down{Fore.RESET}\n")
            dir_=CI.ChoiceInput([i for i in os.listdir(os.getcwd()) if os.path.isdir(os.getcwd()+"/"+i)],True,up=Key.up,down=Key.down,color=Style.BRIGHT+Fore.MAGENTA+Back.CYAN).get()
        if os.path.exists(dir_) and os.path.isdir(dir_):
            try:
                os.chdir(dir_)
            except:
                sys.stdout.write
# ---------------------- Run some files command
    def runFile(self):
        if(self.last_params == []):
            sys.stdout.write(f"NO_FILE_EXCEPTION: {NO_FILE_ERR}")
            return;
        scriptName=self.last_params[0]
        if scriptName.endswith(".c"):
            if not os.system(f"gcc -S {scriptName} -o {scriptName[:-2]}.s"):
                if not os.system(f"gcc {scriptName[:-2]}.s -o {scriptName[:-2]}"):
                    R=os.system(f"./{scriptName[:-2]}")
                    if not R:
                        if self.variables.get("#SHOWCODE",False):
                            sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                    else:
                        if self.variables.get("#SHOWCODE",False):
                            sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
                else:sys.stdout.write(COMPILE_ERR)
            else:sys.stdout.write(COMPILE_ERR)
        elif scriptName.endswith(".cpp"):
            if not os.system(f"g++ {scriptName} -o {scriptName[:-2]}"):
                R=os.system(f"./{scriptName[:-2]}")
                if not R:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                else:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
            else:sys.stdout.write(COMPILE_ERR)
        elif scriptName.endswith(".java"):
            if not os.system(f"javac {scriptName}"):
                R=os.system(f"java {scriptName[:-5]}")
                if not R:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                else:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
            else:sys.stdout.write(COMPILE_ERR)
        elif scriptName.endswith(".js"):
            R=os.system(f"node {scriptName}")
            if not R:
                if self.variables.get("#SHOWCODE",False):
                    sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
            else:
                if self.variables.get("#SHOWCODE",False):
                    sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
        elif scriptName.endswith(".py"):
            if os.name=="nt":
                R=os.system(f"python {scriptName}")
                if not R:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                else:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
            else:
                R=os.system(f"python3 {scriptName}")
                if not R:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                else:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
        elif scriptName.endswith(".pyw"):
            if os.name=="nt":
                R=os.system(f"pythonw {scriptName}")
                if not R:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                else:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
            else:
                R=os.system(f"pythonw3 {scriptName}")
                if not R:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                else:
                    if self.variables.get("#SHOWCODE",False):
                        sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
        elif scriptName.endswith(".s"):
            if not os.system(f"gcc -c {scriptName} -o {scriptName[:-2]}.o"):
                if not os.system(f"gcc {scriptName[:-2]}.o -o {scriptName[:-2]}"):
                    R=os.system(f"./{scriptName[:-2]}")
                    if not R:
                        if self.variables.get("#SHOWCODE",False):
                            sys.stdout.write(f"Executed{Fore.GREEN} successfully{Fore.RESET}")
                    else:
                        if self.variables.get("#SHOWCODE",False):
                            sys.stdout.write(f"Encountered{Fore.GREEN} error{R}{Fore.RESET}")
                else:sys.stdout.write(COMPILE_ERR)
            else:sys.stdout.write(COMPILE_ERR)
        else:
            os.system(f"./{scriptName}")
# ---------------------- Show directory command
    def shdir(self):
        _dir=self.get(self.last_params,0,".")
        if self.last_settings.get("all",False) or self.last_settings.get("a",False):
            _contents=os.listdir(_dir)
            sys.stdout.write("\n%30s\n"%(f"Directory: {Path(_dir).absolute()}"))
            sys.stdout.write("%s%s%30s%10s%7s\n%s%30s%10s%7s%s\n"%(Fore.GREEN,"Mode","LastWriteTime","Size","Name","-"*4,"-"*13,"-"*4,"-"*4,Fore.RESET))
            oL=[]
            i_List=[]
            modeList=[]
            for i in _contents:
                modes="-----"
                i_=Path(_dir+"/"+i).stat()
                if os.access(_dir+"/"+i,os.F_OK):
                    modes=modes[:0]+"f"+modes[1:]
                    if os.access(_dir+"/"+i,os.R_OK) and os.access(_dir+"/"+i,os.W_OK) and os.access(_dir+"/"+i,os.X_OK):
                        modes=modes[:1]+"a"+modes[2:]
                    elif os.access(_dir+"/"+i,os.R_OK):
                        modes=modes[:2]+"r"+modes[3:]
                    elif os.access(_dir+"/"+i,os.W_OK):
                        modes=modes[:3]+"w"+modes[4:]
                    elif os.access(_dir+"/"+i,os.X_OK):
                        modes=modes[:4]+"x"+modes[5:]
                if os.path.isdir(_dir+"/"+i):
                    modes="d----"
                oL.append(datetime.datetime.fromtimestamp(i_.st_ctime))
                i_List.append(i_)
                modeList.append(modes)
            for modes,o,i_,i in zip(modeList,oL,i_List,_contents):
                if i.startswith(self.last_settings.get("start","")):sys.stdout.write("%s%30s%10s%7s\n"%(modes,o.strftime("%D %T"),i_.st_size,i))
            return;#TODO: IMPLEMENT A MORE EXPANDED VIEW ON THE FILES OR DIRS
        else:
            _contents=os.listdir(_dir)
            for i in _contents:
                if len(i)<=40:
                    _contents.insert(0,_contents.pop(_contents.index(i)))
            for _obj,_counter in zip(_contents,list(range(len(_contents)))):
                if len(_obj)>40:
                    if _obj.startswith(self.last_settings.get("start","")):sys.stdout.write("%s%20s%s%s"%(Back.MAGENTA,_obj,Back.RESET,"\n"))
                else:
                    if _obj.startswith(self.last_settings.get("start","")):sys.stdout.write(f"%s%20s%s{Fore.RESET}"%(
                        Fore.CYAN if os.path.isfile(_dir+"/"+_obj) else "",
                        (_obj),
                        ("\n" if not _counter%4 else ""))
                    )
            sys.stdout.write("\n")
# ---------------------- Transform bytes command (useful in some cases)
    def byteTForm(self):
        blob=self.get(self.last_params,0,None)
        if blob is not None:
            if blob.endswith("PB"):
                _r=int(blob.replace("PB",""))
                sys.stdout.write(f"{_r}PB\n")
                sys.stdout.write(f"{_r*1024}TB\n")
                sys.stdout.write(f"{_r*1024*1024}GB\n")
                sys.stdout.write(f"{_r*1024*1024*1024}MB\n")
                sys.stdout.write(f"{_r*1024*1024*1024*1024}KB\n")
                sys.stdout.write(f"{_r*1024*1024*1024*1024*1024}B\n")
            elif blob.endswith("TB"):
                _r=int(blob.replace("TB",""))
                sys.stdout.write(f"{_r/1024}PB\n")
                sys.stdout.write(f"{_r}TB\n")
                sys.stdout.write(f"{_r*1024}GB\n")
                sys.stdout.write(f"{_r*1024*1024}MB\n")
                sys.stdout.write(f"{_r*1024*1024*1024}KB\n")
                sys.stdout.write(f"{_r*1024*1024*1024*1024}B\n")
            elif blob.endswith("GB"):
                _r=int(blob.replace("GB",""))
                sys.stdout.write(f"{_r/1024/1024}PB\n")
                sys.stdout.write(f"{_r/1024}TB\n")
                sys.stdout.write(f"{_r}GB\n")
                sys.stdout.write(f"{_r*1024}MB\n")
                sys.stdout.write(f"{_r*1024*1024}KB\n")
                sys.stdout.write(f"{_r*1024*1024*1024}B\n")
            elif blob.endswith("MB"):
                _r=int(blob.replace("MB",""))
                sys.stdout.write(f"{_r/1024/1024/1024}PB\n")
                sys.stdout.write(f"{_r/1024/1024}TB\n")
                sys.stdout.write(f"{_r/1024}GB\n")
                sys.stdout.write(f"{_r}MB\n")
                sys.stdout.write(f"{_r*1024}KB\n")
                sys.stdout.write(f"{_r*1024*1024}B\n")
            elif blob.endswith("KB"):
                _r=int(blob.replace("KB",""))
                sys.stdout.write(f"{_r/1024/1024/1024/1024}PB\n")
                sys.stdout.write(f"{_r/1024/1024/1024}TB\n")
                sys.stdout.write(f"{_r/1024/1024}GB\n")
                sys.stdout.write(f"{_r/1024}MB\n")
                sys.stdout.write(f"{_r}KB\n")
                sys.stdout.write(f"{_r*1024}B\n")
            elif blob.endswith("B") and blob.replace("B","").isdigit():
                _r=int(blob.replace("B",""))
                sys.stdout.write(f"{_r/1024/1024/1024/1024/1024}PB\n")
                sys.stdout.write(f"{_r/1024/1024/1024/1024}TB\n")
                sys.stdout.write(f"{_r/1024/1024/1024}GB\n")
                sys.stdout.write(f"{_r/1024/1024}MB\n")
                sys.stdout.write(f"{_r/1024}KB\n")
                sys.stdout.write(f"{_r}B\n")
            else:
                sys.stdout.write
# ---------------------- Terminal text editor (like posix nano)
    def TerminalEditor(self):
        if self.last_settings.get("help",False) or self.last_settings.get("h",False):
            xEditor.showHelp()
            return;
        else:
            xEditor._Editor(fName=self.get(self.last_params,0,None),settings=self.last_settings)
# ---------------------- Some help for any command implemented into  (like posix nano)
    def help(self):
        _commas:list[str]=[i for i in self.commands.keys()]
        sys.stdout.write(f"{Fore.GREEN}<{Fore.CYAN}PgUp{Fore.GREEN}>{Fore.WHITE} - Go up\n{Fore.GREEN}<{Fore.CYAN}PgDn{Fore.GREEN}>{Fore.WHITE} - Go down{Fore.RESET}\n")
        cmd_=CI.ChoiceInput(_commas,True,up=Key.up,down=Key.down,color=Style.BRIGHT+Fore.MAGENTA+Back.CYAN).get()

    def execute(self,parameters:"list[str]"=None,settings:"dict[str,str]"=None):
        formats.update()
        if settings is None:
            try:settings:"dict[str,str]" = self.parsed[0]
            except:settings={}
        if parameters is None:
            try:parameters:"list[str]" = self.parsed[1]
            except:parameters=[]
        if not parameters.__len__():
            return;
        command=parameters.pop(0)
        self.last_settings=settings
        self.last_params=parameters
        self.last_command=command
        for name,func in self.commands.items():
            if name==command:
                try:
                    func()
                except Exception as e:
                    sys.stdout.write(RUN_ERR)
                    raise e
                break;
        else:
            try:
                RESP=eval(self.last)
                if RESP is not None:
                    sys.stdout.write(f"{RESP}\n")
            except Exception as e:
                try:
                    comma=self.last
                    if "def"==self.last.split()[0] and len(self.last.split())>1:
                        funcName=self.last.split()[1]
                        if "(" in funcName:
                            funcName=funcName.split("(")[0]
                        try:
                            comma+=f"\nconst['{funcName}']={funcName}"
                        except:pass
                    exec(comma,globals())
                    return
                except Exception as e:pass
                PWRESPONSE=pwsh.run(f"powershell \"{self.last}\"")
                CODE=PWRESPONSE.returncode
                if self.isSilent()=="False":
                    if self.showCode()=="True":
                        if not CODE:
                            sys.stdout.write(f"Command executed successfully with status:{Fore.GREEN}{CODE}\n{Fore.RESET}")
                        else:
                            sys.stdout.write(f"Command returned error status:{Fore.RED}{CODE}\n{Fore.RESET}")
                    else:
                        if not CODE:
                            sys.stdout.write(f"{Fore.GREEN}{formats.formatOptions['$CH2']} {Fore.RESET}")
                        else:
                            sys.stdout.write(f"{Fore.RED}{formats.formatOptions['$CH3']} {Fore.RESET}")
        self.update()

    def sVar(self,parameters:"list[str]"=None,settings:"dict[str,str]"=None):
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

        vAlloc="null"
        for i in self.last_params:
            if i=="=":
                vAlloc=self.get(self.last_params,self.last_params.index("=")-1,"null")
                vContent=self.get(self.last_params,self.last_params.index("=")+1,"")
                return;
    def readInput(self)->str:
        return pwsh.run("powershell Read-Host",stdout=pwsh.PIPE).stdout.decode(errors="ignore").replace("\r","").replace("\n","") if ("--raw-input" in sys.argv or "-r" in sys.argv) else input()
    def update(self):
        self.variables.update(
            {
                "#CWD":os.getcwd(),
            }
        )
        formats.update()
    def press(self,key):
        if key==kb.Key.tab:
            sys.stdout.write("\n")
            self.execute(["List-Dir"])
            sys.stdout.write(formats.formatStr(self.variables.get("#FORMAT")))
    def run(self):
        with kb.Listener(on_press=self.press) as Listener:
            while True:
                try:
                    sys.stdout.write(formats.formatStr(self.variables.get("#FORMAT")))
                    self.last=self.readInput()
                    self.parsed=[ArgumentParser.FindSettings(self.last),ArgumentParser.FindParams(self.last)]
                    if self.last.startswith("set"):
                        self.sVar()
                    else:
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
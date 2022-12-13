import os,sys

from colorama import init,Back,Fore

init(autoreset=True)

try:
    from AP import FindParams,FindSettings
except:
    from .ObjParser import FindParams, FindSettings

class argvParser:
    def __init__(self,initialOptions:"dict[str,str|bool]"={},argv:"list[str]"=sys.argv) -> None:
        self.argv=" ".join(argv)
        self.listargv=argv
        self.options={}
        self.params=FindParams(self.argv)
        self.settings=FindSettings(self.argv)
        for i in self.settings:
            self.add(name=i,default=self.settings[i]["value"])
        self.options.update(initialOptions)
    def add(self,
        name:str=None,
        default:str=None,
        help:str=f"{Back.RED}Undocumented/Not existent{Back.RESET}",
    ):
        if self.options.get(name,None) == None:
            self.options[name]={
                "value":default
            }
        self.options[name]["help"]=help
    def __str__(self) -> str:
        return "Options:"+str(["--"+i for i in self.settings])+"\nParameters provided:"+str(self.params)
    def GetOption(self,name:str=None,default:str=False):
        return self.options.get(name,{"value":default})["value"]
    def GetArgs(self):
        return self.params
    def help(self):
        r="\n".join(["\t--%-15s-\t%10s"%(_,a["help"]) for _,a in self.options.items()])
        return r

if __name__=="__main__":
    parser=argvParser()
    parser.add(name="help",help="shows this tab right here")
    parser.add(name="colored",help="display colored text")
    print(parser)
    print(parser.help())
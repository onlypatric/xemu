import curses,sys
import os
from editor.editor import Editor

class _Editor:
    def __init__(self,fName=None) -> None:
        if fName==None:
            fName="untilted.txt"
        self.fName=fName
        curses.wrapper(self.main)
        

    def main(self,stdscr):
        self.editor=Editor(stdscr,title="XeX, Text editor",box=False,win_location=(5,5),save=self.save)
        try:
            self.editor()
        except:pass
        self.save()

    def save(self):
        if not os.path.exists(self.fName):
            try:
                open(self.fName,"x")
            except:
                self.fName="untilted.txt"
                open(self.fName,"x")
        open(self.fName,"w").write(self.getText())

    def getText(self):
        r="\n".join([i for i in ["".join(j) for j in self.editor.text]])

        return r

if __name__=="__main__":
    _Editor()

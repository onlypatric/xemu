## XEmu - Shell Emulator

a shell emulator made to implement some things we love about linux and improve the terminal's usage

**Built for Windows and Linux, MacOS is not tested**

----------
Required Dependencies:
 - PowerShell 7.0+

Optional Dependencies:
 - GCC compiler
 - G++ compiler
 - Python3.x interpreter
 - NodeJS
 - JDK

```python
python "main.py" <--raw-input>
# raw-input option is used to get input 
# without using powershell's built-in 
# Read-Host Method, just by __builtins__.input
```

each command has few options to play with, it is made to be very simple to get used to

also integrated **Terminal Editor** (inspired by nano), which is made to work both on Windows and Linux (not guaranteed for MacOS)

shell interpreter has also a built-in python interpreter, you can create your own functions using the global dictionary called "const", for example:
```python
const["hellomsg"]="hello world"
print(const["hellomsg"])
```
any method that is passed through gets saved into const dict
```python
def main(object):print(object)
const["main"](23) # gives 23 as output
```
execute python files also with 
```python
exec(<str>)
```
for example:
```python
exec(open("main.py").read())
```

so not only this shell interpreter has some very cool built-ins, it also handles python objects directly typed into the terminal's input (plus takes formulas, conditions and evaluates them if needed with `eval()` method), and you got all the powershell's latest and most powerful features, xemu is made to adapt itself to any powershell 7.0+ version, so **have fun with XEmu**!
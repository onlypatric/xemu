from pynput import keyboard
def showPressed(key):
    print(key)
with keyboard.Listener(on_press=showPressed,suppress=True) as listener:
    listener.join()
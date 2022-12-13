import os

def login():
    try:
        return os.getlogin()
    except:
        return "root"
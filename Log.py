from datetime import datetime
from pathlib import Path
from os import makedirs

def Now():
    now = datetime.now()
    return f"{str(Path.home())}\\Documents\\ChannelNotif\\{now.year}-{now.month}-{now.day}-{now.hour}_{now.minute}.log"

class Logger:
    def __init__(self):
        try:
            try:
                self.File = open(Now(), "x")
            except FileExistsError:
                self.File = open(Now(), "a")
        except FileNotFoundError:
            makedirs(str(Path.home()) + "\\Documents\\ChannelNotif\\")
            self.File = open(Now(), "x")
        
    def Log(self, S: str):
        self.File.write("[LOG] " + S + "\n")
from ManiaplanetAPI import *
from datetime import datetime
from ToastWrapper import Notify
from frontend import Launch
from SettingsHandler import Settings
from pathlib import Path
from os import makedirs

Hour = datetime.now().hour
PHour = Hour

try:
    open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "x").write(Settings().ToJson())
except FileNotFoundError:
    makedirs(str(Path.home()) + "\\Documents\\ChannelNotif\\")
    open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "x").write(Settings().ToJson())
except FileExistsError:
    open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "w").write(Settings().ToJson())

# Notify('New channel', DictToChannel(GetChannelA()).Name, lambda: print("hi"))

# while True:
#     Hour = datetime.now().hour
#     if PHour != Hour:
#         Notify('New channel', DictToChannel(GetChannelA()).Name, lambda: print("hi"))
#     PHour = Hour
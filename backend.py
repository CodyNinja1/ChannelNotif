from ManiaplanetAPI import *
from datetime import datetime
from ToastWrapper import Notify
from frontend import Launch
Hour = datetime.now().hour
PHour = Hour

if Notify('New channel', RemoveTMFormatting(GetChannelA()['program_name']), "ChannelNotif"):
    Launch()

while True:
    Hour = datetime.now().hour
    if PHour != Hour:
        Notify('New channel', RemoveTMFormatting(GetChannelA()['program_name']), "ChannelNotif")
    PHour = Hour
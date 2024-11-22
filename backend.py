from ManiaplanetAPI import *
from datetime import datetime
from ToastWrapper import Notify
from SettingsHandler import GetSettings
from time import sleep
from Frontend import Launch

tz = pytz.timezone(get_localzone_name())

Hour = datetime.now().hour
PHour = Hour

while True:
    Settings = GetSettings()
    Hour = datetime.now().hour

    if PHour != Hour:
        if Settings.Notifications.AlertEveryChannel:
            if Notify('New trackmania channel', DictToChannel(GetChannelA()).Name):
                if Settings.Notifications.PerformOnClick():
                    Launch()
            if Notify('New shootmania channel', DictToChannel(GetChannelA(True)).Name):
                if Settings.Notifications.PerformOnClick():
                    Launch()
        else:
            Day = datetime.now(tz=tz).weekday()
            HourTZ = datetime.now(tz=tz).hour
            Trackmania = Settings.Favourites.Favourites[0][Day][Hour]
            Shootmania = Settings.Favourites.Favourites[1][Day][Hour]

            if Trackmania:
                if Notify('New trackmania channel', DictToChannel(GetChannelA()).Name):
                    if Settings.Notifications.PerformOnClick():
                        Launch()
            if Shootmania:
                if Notify('New shootmania channel', DictToChannel(GetChannelA(True)).Name):
                    if Settings.Notifications.PerformOnClick():
                        Launch()

    sleep(1)
    PHour = Hour
from ManiaplanetAPI import *
from datetime import datetime
from ToastWrapper import Notify
from SettingsHandler import GetSettings
from time import sleep

tz = pytz.timezone(get_localzone_name())

Hour = datetime.now(tz=tz).hour
PHour = Hour

while True:
    Settings = GetSettings()
    Hour = datetime.now(tz=tz).hour

    if PHour != Hour:
        if Settings.Notifications.AlertEveryChannel:
            Notify('New trackmania channel', DictToChannel(GetChannelA()).Name, Settings.Notifications.PerformOnClick)
            Notify('New shootmania channel', DictToChannel(GetChannelA(True)).Name, Settings.Notifications.PerformOnClick)
        else:
            Day = datetime.now(tz=tz).weekday()
            Trackmania = Settings.Favourites.Favourites[0][Day][Hour]
            Shootmania = Settings.Favourites.Favourites[1][Day][Hour]

            if Trackmania:
                Notify('New trackmania channel', DictToChannel(GetChannelA()).Name, Settings.Notifications.PerformOnClick)
            if Shootmania:
                Notify('New shootmania channel', DictToChannel(GetChannelA(True)).Name, Settings.Notifications.PerformOnClick)

    sleep(1)
    PHour = Hour
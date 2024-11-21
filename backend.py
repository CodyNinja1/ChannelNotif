from ManiaplanetAPI import *
from datetime import datetime
from ToastWrapper import Notify
from Frontend import Launch
from SettingsHandler import GetSettings

Hour = datetime.now().hour
PHour = Hour

Notify('Test', '123', GetSettings().Notifications.PerformOnClick)
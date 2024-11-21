from ManiaplanetAPI import *
from datetime import datetime
from ToastWrapper import Notify
from Frontend import Launch
from SettingsHandler import GetSettings, SetSettings

Hour = datetime.now().hour
PHour = Hour

print(GetSettings().ToJson())

S = GetSettings()
S.Notifications.AlertEveryChannel = True
SetSettings(S)

print(GetSettings().ToJson())
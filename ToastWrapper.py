from win11toast import toast
from SettingsHandler import GetSettings
def Notify(Title: str, Description: str) -> bool:
    return type(toast(Title, Description, on_click="http:", app_id=GetSettings().Notifications.AppId)) == dict
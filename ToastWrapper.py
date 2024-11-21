from win11toast import toast
def Notify(Title: str, Description: str, Func) -> None:
    if type(toast(Title, Description, on_click="http:", app_id="ChannelNotif")) == dict: Func()
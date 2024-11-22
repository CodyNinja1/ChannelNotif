from win11toast import toast
def Notify(Title: str, Description: str) -> bool:
    return type(toast(Title, Description, on_click="http:", app_id="ChannelNotif")) == dict
import json
from typing import Literal

class NotifSettings:
    def __init__(self):
        self.AppId: str = "ChannelNotif"
        self.OnClick: Literal["Steam", "Exe", "Frontend", "Nothing"] = "Frontend"
        self.Game: Literal["Lagoon", "Valley", "Storm", "Stadium", "Canyon"] = "Lagoon"
        self.AlertEveryChannel: bool = False
    
    def ToJson(self):
        return json.dumps({
            "appid": self.AppId,
            "onclick": self.OnClick,
            "game": self.Game,
            "alerteverychannel": self.AlertEveryChannel
        }, indent=4)

    def FromJson(self, JsonStr: str):
        try:
            data = json.loads(JsonStr)
            if "appid" in data and isinstance(data["appid"], str):
                self.AppId = data["appid"]
            if "onclick" in data and data["onclick"] in {"Steam", "Exe", "Frontend", "Nothing"}:
                self.OnClick = data["onclick"]
            if "game" in data and data["game"] in {"Lagoon", "Valley", "Storm", "Stadium", "Canyon"}:
                self.Game = data["game"]
            if "alerteverychannel" in data and isinstance(data["alerteverychannel"], bool):
                self.AlertEveryChannel = data["alerteverychannel"]
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")


class UpdateSettings:
    def __init__(self):
        self.AutoCheckForUpdates: bool = True
        self.Version: str = "v1.0"

    def ToJson(self):
        return json.dumps({
            "autocheckforupdates": self.AutoCheckForUpdates,
            "version": self.Version
        }, indent=4)

    def FromJson(self, JsonStr: str):
        try:
            data = json.loads(JsonStr)
            if "autocheckforupdates" in data and isinstance(data["autocheckforupdates"], bool):
                self.AutoCheckForUpdates = data["autocheckforupdates"]
            if "version" in data and isinstance(data["version"], str):
                self.Version = data["version"]
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")

class Settings:
    def __init__(self):
        self.Notifications = NotifSettings()
        self.Updates = UpdateSettings()
    
    def ToJson(self):
        return json.dumps({
            "notifications": json.loads(self.Notifications.ToJson()),
            "updates": json.loads(self.Updates.ToJson())
        }, indent=4)

    def FromJson(self, JsonStr: str):
        try:
            data = json.loads(JsonStr)
            if "notifications" in data and isinstance(data["notifications"], dict):
                self.Notifications.FromJson(json.dumps(data["notifications"]))
            if "updates" in data and isinstance(data["updates"], dict):
                self.Updates.FromJson(json.dumps(data["updates"]))
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")
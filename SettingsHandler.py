import json
from typing import Literal
from pathlib import Path
from os import makedirs, system
from subprocess import Popen
from ManiaplanetAPI import GetChannelsByGameA

class NotifSettings:
    def __init__(self):
        self.SteamAppIdTable: dict[Literal["Lagoon", "Valley", "Storm", "Stadium", "Canyon"], int] = {"Lagoon": "600720", "Valley": "243360", "Stadium": "232910", "Storm": "229870", "Canyon": "228760"}
        self.AppId: str = "ChannelNotif"
        self.OnClick: Literal["Steam", "Exe", "Frontend", "Nothing"] = "Frontend"
        self.Game: Literal["Lagoon", "Valley", "Storm", "Stadium", "Canyon"] = "Lagoon"
        self.Exe: str = ""
        self.AlertEveryChannel: bool = False
    
    def ToJson(self):
        return json.dumps({
            "appid": self.AppId,
            "onclick": self.OnClick,
            "game": self.Game,
            "exe": self.Exe,
            "alerteverychannel": self.AlertEveryChannel
        }, indent=4)

    def FromJson(self, JsonStr: str):
        try:
            Data = json.loads(JsonStr)
            if "appid" in Data and isinstance(Data["appid"], str):
                self.AppId = Data["appid"]
            if "onclick" in Data and Data["onclick"] in {"Steam", "Exe", "Frontend", "Nothing"}:
                self.OnClick = Data["onclick"]
            if "game" in Data and Data["game"] in {"Lagoon", "Valley", "Storm", "Stadium", "Canyon"}:
                self.Game = Data["game"]
            if "exe" in Data:
                self.Exe = Data["exe"]
            if "alerteverychannel" in Data and isinstance(Data["alerteverychannel"], bool):
                self.AlertEveryChannel = Data["alerteverychannel"]
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")

    def PerformOnClick(self, Shootmania: bool = False) -> bool:
        match self.OnClick:
            case "Steam":
                system("explorer steam://rungameid/" + self.SteamAppIdTable[self.Game])
                return False
            case "Frontend":
                return True
            case "Exe":
                Popen(self.Exe + " /join=" + GetChannelsByGameA(Shootmania)[0]["login"] + "@" + GetChannelsByGameA(Shootmania)[0]["title"])
            case "Nothing":
                pass
        return False

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
            Data = json.loads(JsonStr)
            if "autocheckforupdates" in Data and isinstance(Data["autocheckforupdates"], bool):
                self.AutoCheckForUpdates = Data["autocheckforupdates"]
            if "version" in Data and isinstance(Data["version"], str):
                self.Version = Data["version"]
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")

class FavouriteSettings:
    def __init__(self):
        self.Favourites: dict[int, list[list[bool]]] = {0: [
            [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ]], 1: [
            [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ], [False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False, 
             False, False
            ]]}
    
    def ToJson(self):
        # Convert the dictionary into JSON format
        return json.dumps(self.Favourites, indent=4)

    def FromJson(self, JsonStr: str):
        try:
            data = json.loads(JsonStr)
            if isinstance(data, dict):
                # Validate that keys are integers and values are lists of lists of booleans
                validated_data = {}
                for key, value in data.items():
                    if isinstance(key, str) and key.isdigit():
                        key = int(key)  # Convert string keys to integers
                    if isinstance(key, int) and isinstance(value, list) and all(
                        isinstance(sublist, list) and all(isinstance(item, bool) for item in sublist)
                        for sublist in value
                    ):
                        validated_data[key] = value
                self.Favourites = validated_data
            else:
                print("Error: JSON does not represent a dictionary.")
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")

class UiSettings:
    def __init__(self):
        self.IsDarkMode = True
        self.ColorPalette = [
            (0, 0.922, 0.451), 
            (0, 0.78, 0.376), 
            (0, 0.62, 0.298), 
            (0, 0.459, 0.224), 
            (0, 0.302, 0.149)
        ]

    def ToJson(self):
        return json.dumps({
            "IsDarkMode": self.IsDarkMode,
            "ColorPalette": self.ColorPalette
        })

    def FromJson(self, JsonStr: str):
        try:
            data = json.loads(JsonStr)
            if "IsDarkMode" in data and isinstance(data["IsDarkMode"], bool):
                self.IsDarkMode = data["IsDarkMode"]
            if "ColorPalette" in data and isinstance(data["ColorPalette"], list):
                self.ColorPalette = [tuple(color) for color in data["ColorPalette"]]
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")

class Settings:
    def __init__(self):
        self.Notifications = NotifSettings()
        self.Updates = UpdateSettings()
        self.Favourites = FavouriteSettings()
        self.Ui = UiSettings()

    def ToJson(self):
        return json.dumps({
            "Notifications": json.loads(self.Notifications.ToJson()),
            "Updates": json.loads(self.Updates.ToJson()),
            "Favourites": json.loads(self.Favourites.ToJson()),
            "Ui": json.loads(self.Ui.ToJson())
        }, indent=4)

    def FromJson(self, JsonStr: str):
        try:
            data = json.loads(JsonStr)
            if "Notifications" in data and isinstance(data["Notifications"], dict):
                self.Notifications.FromJson(json.dumps(data["Notifications"]))
            if "Updates" in data and isinstance(data["Updates"], dict):
                self.Updates.FromJson(json.dumps(data["Updates"]))
            if "Favourites" in data and isinstance(data["Favourites"], dict):
                self.Favourites.FromJson(json.dumps(data["Favourites"]))
            if "Ui" in data and isinstance(data["Ui"], dict):
                self.Ui.FromJson(json.dumps(data["Ui"]))
        except (json.JSONDecodeError, TypeError) as e:
            print(f"Error decoding JSON: {e}")
    
    def FromFile(self, FilePath: str):
        try:
            with open(FilePath, "r") as File:
                Json = File.read()
                self.FromJson(Json)
        except FileNotFoundError:
            print(f"Error: The file '{FilePath}' does not exist.")
        except IOError as e:
            print(f"Error reading file '{FilePath}': {e}")

def ResetSettings():
    try:
        try:
            open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "x").write(Settings().ToJson())
        except FileNotFoundError:
            makedirs(str(Path.home()) + "\\Documents\\ChannelNotif\\")
            open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "x").write(Settings().ToJson())
    except FileExistsError:
        open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "w").write(Settings().ToJson())

def SetSettings(Setting: Settings):
    try:
        try:
            open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "x").write(Setting.ToJson())
        except FileNotFoundError:
            makedirs(str(Path.home()) + "\\Documents\\ChannelNotif\\")
            open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "x").write(Setting.ToJson())
    except FileExistsError:
        open(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json", "w").write(Setting.ToJson())

def GetSettings():
    Setting = Settings()
    Setting.FromFile(str(Path.home()) + "\\Documents\\ChannelNotif\\settings.json")
    return Setting
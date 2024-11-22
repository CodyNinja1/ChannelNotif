from Log import Logger
from Ui import *
from ManiaplanetAPI import GetChannelA, DictToChannel, Channel
from SettingsHandler import GetSettings, Settings

Tooltip = ""
ChannelTM = Channel("", -1, "")
ChannelSM = Channel("", -1, "")

def InitUi(UiMgr: UiManager, Log: Logger):
    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", 16)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", 11)
    Log.Log("[FRONTEND] Fonts loaded")

    # Main Menu
    UiMgr.CreateButton() # PlayTM
    UiMgr.CreateButton() # PlaySM
    UiMgr.CreateButton() # Settings

    # Settings
    UiMgr.CreateButton() # Back

    # Schedule
    UiMgr.CreateButton()

def SetTooltip(String: str):
    global Tooltip
    if String == "":
        Tooltip = "Description:"
    else:
        Tooltip = f"Description:\n\n{String}"

def MenuMain(UiMgr: UiManager, Setting: Settings):
    global ChannelTM, ChannelSM
    pass

def MenuSettings(UiMgr: UiManager, Setting: Settings):
    pass

def MenuSchedule(UiMgr: UiManager, Setting: Settings):
    pass

def RenderTooltip(UiMgr: UiManager):
    global Tooltip
    UiMgr.TextWrapped(Tooltip, Nat2(360, 160), 1)

def Launch():
    global Tooltip
    Log = Logger()
    Log.Log("[FRONTEND] Frontend Launched.")

    global ChannelTM, ChannelSM
    ChannelTM = DictToChannel(GetChannelA())
    ChannelSM = DictToChannel(GetChannelA(True))
    Log.Log("[FRONTEND] Channels loaded from API")
    UiMgr = UiManager()

    InitUi(UiMgr, Log)
    Setting = GetSettings()

    Log.Log("[FRONTEND] Hello, world!")
    Log.Log(f"[FRONTEND] ChannelNotif {Setting.Updates.Version}")

    while UiMgr.Running:
        sdl2.SDL_RenderClear(UiMgr.Renderer)
        UiMgr.Rect(Nat2(0, 0), Nat2(848, 480), Color=Vec4(0, 0, 0, 1))

        match UiMgr.ActiveMenu:
            case "Main":
                MenuMain(UiMgr, Setting)
            case "Settings":
                MenuSettings(UiMgr, Setting)
            case "Schedule":
                MenuSchedule(UiMgr, Setting)
        RenderTooltip(UiMgr)

        UiMgr.MainLoop()
    
    Log.Log("[FRONTEND] Exiting")
    UiMgr.Quit()

if __name__ == "__main__":
    Launch()
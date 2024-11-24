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

def SetTooltip(String: str):
    global Tooltip
    if String == "":
        Tooltip = "Description:"
    else:
        Tooltip = f"Description:\n\n{String}"

def MenuMain(UiMgr: UiManager, Setting: Settings):
    global ChannelTM, ChannelSM
    SetTooltip("Tooltip. Hover over an\nelement to view its\ndescription.")  

    ButtonRect, Clicked, ButtonHovered = UiMgr.Button(UiMgr.GetModeIcon(), Nat2(100, 100), UiMgr.SwitchMode, FontIdx=1)
    if ButtonHovered:
        SetTooltip("Dark/light mode switch.")
    Checked, CheckboxHovered = UiMgr.Checkbox("Testing", Nat2(100, 160))
    if CheckboxHovered:
        SetTooltip(f"Checkbox.\nIt is{"n't" if not Checked else ""} checked.")

def MenuSettings(UiMgr: UiManager, Setting: Settings):
    pass

def MenuSchedule(UiMgr: UiManager, Setting: Settings):
    pass

def RenderTooltip(UiMgr: UiManager):
    global Tooltip
    UiMgr.TextWrapped(Tooltip, Nat2(600, 10), 1, 0)

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
        UiMgr.Rect(Nat2(0, 0), Nat2(848, 480), ColorIdx=-1)

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
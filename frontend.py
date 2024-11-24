from Log import Logger
from Ui import *
from ManiaplanetAPI import GetChannelA, DictToChannel, Channel
from SettingsHandler import GetSettings, Settings

Tooltip = ""
ChannelTM = Channel("", -1, "")
ChannelSM = Channel("", -1, "")

# MARK: InitUi

def InitUi(UiMgr: UiManager, Log: Logger):
    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", "Large", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", "Medium", 16)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", "SmallIcons", 11)
    Log.Log("[FRONTEND] Fonts loaded")

# MARK: Tooltip

def RenderTooltip(UiMgr: UiManager):
    global Tooltip
    UiMgr.TextWrapped(Tooltip, Nat2(600, 10), "Medium", 0)

def SetTooltip(String: str):
    global Tooltip
    if String == "":
        Tooltip = "Description:"
    else:
        Tooltip = f"Description:\n\n{String}"

# MARK: MenuMain

def MenuMain(UiMgr: UiManager, Setting: Settings):
    global ChannelTM, ChannelSM
    SetTooltip("Tooltip. Hover over an\nelement to view its\ndescription.")  

    UiMgr.Text("Hello, world!", Nat2(10, 10), "Large")

    ButtonRect, Clicked, ButtonHovered = UiMgr.Button(UiMgr.GetModeIcon(), Nat2(100, 100), "Medium", UiMgr.SwitchMode)
    if ButtonHovered:
        SetTooltip("Dark/light mode switch.")
    Checked, CheckboxHovered = UiMgr.Checkbox("Testing", Nat2(100, 160), "Medium")
    if CheckboxHovered:
        SetTooltip(f"Checkbox.\nIt is{"n't" if not Checked else ""} checked.")

# MARK: MenuSettings

def MenuSettings(UiMgr: UiManager, Setting: Settings):
    pass

# MARK: MenuSchedule

def MenuSchedule(UiMgr: UiManager, Setting: Settings):
    pass

# MARK: MainLoop

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
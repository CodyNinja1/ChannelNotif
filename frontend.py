from Log import Logger
from Ui import *
from ManiaplanetAPI import GetChannelA, DictToChannel, Channel
from SettingsHandler import GetSettings, Settings

Tooltip = ""
ChannelTM = Channel("", -1, "")
ChannelSM = Channel("", -1, "")

def InitUi(UiMgr: UiManager, Log: Logger):
    global ChannelTM, ChannelSM
    ChannelTM = DictToChannel(GetChannelA())
    ChannelSM = DictToChannel(GetChannelA(True))

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
    global Tooltip
    UiMgr.Text("ChannelNotif", Nat2(40, 40), 0)

    ButtonRect = UiMgr.Button(f"Play Trackmania (via {Setting.Notifications.OnClick})", Nat2(50, 220), Setting.Notifications.PerformOnClick, 0, 1)
    ButtonRect = UiMgr.Button(f"Play Shootmania (via {Setting.Notifications.OnClick})", Nat2(50, 261), lambda: Setting.Notifications.PerformOnClick(True), 1, 1)
    SettingsButtonPos = Nat2(50, 220)
    SettingsButtonPos = Nat2(SettingsButtonPos.X + ButtonRect.WH.X, SettingsButtonPos.Y)
    UiMgr.Button("", SettingsButtonPos, lambda: UiMgr.ChangeActiveMenu("Settings"), 2, 2)

    if UiMgr.Buttons[2][1]:
        SetTooltip("Settings.")
    elif UiMgr.Buttons[1][1]:
        SetTooltip("Shootmania channel:\n" + ChannelSM.Name)
    elif UiMgr.Buttons[0][1]:
        SetTooltip("Trackmania channel:\n" + ChannelTM.Name)
    else:
        SetTooltip("")

def MenuSettings(UiMgr: UiManager, Setting: Settings):
    UiMgr.Button("", Nat2(818, 455), lambda: UiMgr.ChangeActiveMenu("Main"), 3, 2)
    UiMgr.Text("Settings", Nat2(40, 40), 0)
    Ate = UiMgr.Checkbox("Option 1", Nat2(100, 100), Vec4(0.8, 0.8, 0.8, 1), Vec4(0.3, 1, 0.3, 1))
    if Ate:
        UiMgr.TextWrapped("Some sort of warning that\ntakes multiple lines to make", 
                        Nat2(115, 130), 1)
        UiMgr.Checkbox("Option 2", Nat2(100, 180), Vec4(0.8, 0.8, 0.8, 1), Vec4(1, 0.3, 0.3, 1))

def MenuSchedule(UiMgr: UiManager, Setting: Settings):
    UiMgr.Button("", Nat2(818, 455), lambda: UiMgr.ChangeActiveMenu("Main"), 2, 2)
    UiMgr.Text("Schedule", Nat2(40, 40), 0)

def RenderTooltip(UiMgr: UiManager):
    global Tooltip
    UiMgr.TextWrapped(Tooltip, Nat2(360, 160), 1)

def Launch():
    global Tooltip
    Log = Logger()
    Log.Log("[FRONTEND] Frontend Launched.")

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
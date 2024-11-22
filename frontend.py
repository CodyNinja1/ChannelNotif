from Log import Logger
from Ui import *
from ManiaplanetAPI import GetChannelA, DictToChannel
from SettingsHandler import GetSettings, Settings

def InitUi(UiMgr: UiManager, Log: Logger):
    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", 16)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", 11)
    Log.Log("[FRONTEND] Fonts loaded")

    # Main Menu
    UiMgr.CreateButton() # Play
    UiMgr.CreateButton() # Settings

    # Settings
    UiMgr.CreateButton() # Back

def MenuMain(UiMgr: UiManager, Setting: Settings):
    UiMgr.Text("ChannelNotif", Nat2(40, 160), 0)

    ButtonRect = UiMgr.Button(f"Play ({Setting.Notifications.OnClick})", Nat2(50, 220), Setting.Notifications.PerformOnClick, 0, 1)
    SettingsButtonPos = Nat2(50, 220)
    SettingsButtonPos = Nat2(SettingsButtonPos.X + ButtonRect.WH.X, SettingsButtonPos.Y)
    UiMgr.Button("", SettingsButtonPos, lambda: UiMgr.ChangeActiveMenu("Settings"), 1, 2)

    UiMgr.TextWrapped("Message de test..\nbalblalba...\nthis is a message,\ndo you want to machiner le bordel,\nou dou you prefer to stroumpher le strouchmpf?\nplease say!", 
                      Nat2(360, 160), 1)

def MenuSettings(UiMgr: UiManager, Setting: Settings):
    UiMgr.Button("", Nat2(818, 455), lambda: UiMgr.ChangeActiveMenu("Main"), 2, 2)

def MenuSchedule(UiMgr: UiManager, Setting: Settings):
    UiMgr.Button("", Nat2(818, 455), lambda: UiMgr.ChangeActiveMenu("Main"), 2, 2)

def Launch():
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

        UiMgr.MainLoop()
    
    Log.Log("[FRONTEND] Exiting")
    UiMgr.Quit()

if __name__ == "__main__":
    Launch()
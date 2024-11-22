from Log import Logger
from Ui import *
from ManiaplanetAPI import GetChannelA, DictToChannel
from SettingsHandler import GetSettings
from time import sleep

def Launch():
    Log = Logger()
    Log.Log("[FRONTEND] Frontend Launched.")

    ChannelTM = DictToChannel(GetChannelA())
    ChannelSM = DictToChannel(GetChannelA(True))

    Log.Log("[FRONTEND] Channels loaded from API")
    UiMgr = UiManager()
    UiMgr.LoadImageFromUrl(ChannelTM.ImageUrl + "?width=424&height=240")

    Settings = GetSettings()

    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", 16)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLightManiaIcons.ttf", 11)
    Log.Log("[FRONTEND] Fonts loaded")
    UiMgr.CreateButton()
    UiMgr.CreateButton()

    Log.Log("[FRONTEND] Hello, world!")
    Log.Log(f"[FRONTEND] ChannelNotif {Settings.Updates.Version}")

    while UiMgr.Running:
        # Clear the screen
        sdl2.SDL_RenderClear(UiMgr.Renderer)
        
        # Draw the background rectangle (black)
        UiMgr.Rect(Nat2(0, 0), Nat2(848, 480), Color=Vec4(0, 0, 0, 1))

        if UiMgr.ActiveMenu == "Main":
            # Draw text for the app name
            UiMgr.Text("ChannelNotif", Nat2(40, 160), 0)
            
            # Draw buttons for play and settings
            UiMgr.Button(f"Play ({Settings.Notifications.OnClick})", Nat2(50, 220), Settings.Notifications.PerformOnClick, 0, 1)
            UiMgr.Button("", Nat2(200, 220), lambda: UiMgr.ChangeActiveMenu("Settings"), 1, 2)

            # Draw active channel info
            UiMgr.Text("Active channel:", Nat2(380, 130), 1)

            # Render the image at the specified position (380, 160)
            UiMgr.RenderImage(0, Nat2(380, 160))
        
        # Update the UI state (handles events, etc.)
        UiMgr.MainLoop()
    
    Log.Log("[FRONTEND] Exiting")
    UiMgr.Quit()

if __name__ == "__main__":
    Launch()
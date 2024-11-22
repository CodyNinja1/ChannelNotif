from Log import Logger
from Ui import UiManager, Nat2, Vec4
from random import randint

Log = Logger()

def Launch():
    Log.Log("[FRONTEND] Frontend Launched.")
    UiMgr = UiManager()

    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 64)
    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLight.ttf", 16)

    while UiMgr.Running:
        UiMgr.Rect(Nat2(0, 0), Nat2(848, 480), Color=Vec4(0, 0, 0, 1))
        
        UiMgr.Text("ChannelNotif", Nat2(40, 120), 0, Vec4(1, 1, 1, 1))

        UiMgr.MainLoop()
    
    UiMgr.Quit()

if __name__ == "__main__":
    Launch()
from Log import Logger
from Ui import *
from random import randint

Log = Logger()

TextRect = Rect(Nat2(0, 0), Nat2(0, 0))

def Launch():
    global TextRect
    Log.Log("[FRONTEND] Frontend Launched.")
    UiMgr = UiManager()

    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 64)
    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLight.ttf", 16)

    while UiMgr.Running:
        UiMgr.Rect(Nat2(0, 0), Nat2(848, 480), Color=Vec4(0, 0, 0, 1))
        
        Color = Vec4(0, 1, 0, 1) if UiMgr.PointInsideRect(UiMgr.GetCursorPosition(), TextRect.XY, TextRect.WH) else Vec4(1, 0, 0, 1)
        TextRect = UiMgr.Text("ChannelNotif", Nat2(40, 120), 0, Color)

        UiMgr.MainLoop()
    
    UiMgr.Quit()

if __name__ == "__main__":
    Launch()
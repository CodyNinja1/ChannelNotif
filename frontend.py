from Log import Logger
from Ui import *

Log = Logger()

Text = "Test"
i = 0

def ChangeText():
    global Text, i
    i += 1
    Text = f"Test {i}"

def Launch():
    Log.Log("[FRONTEND] Frontend Launched.")
    UiMgr = UiManager()

    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 64)
    UiMgr.LoadFont("Fonts/GeistMonoLight.ttf", 32)
    UiMgr.LoadFont("Fonts/GeistMonoExtraLight.ttf", 16)
    UiMgr.CreateButton()

    while UiMgr.Running:
        UiMgr.Rect(Nat2(0, 0), Nat2(848, 480), Color=Vec4(0, 0, 0, 1))
        
        UiMgr.Button("Button", Nat2(40, 120), ChangeText, 0)
        UiMgr.Text(Text, Nat2(40, 280), 0)

        UiMgr.MainLoop()
    
    UiMgr.Quit()

if __name__ == "__main__":
    Launch()
from typing import Literal
import sdl2
import sdl2.ext as sdl2ext
import sdl2.sdlttf as sdlttf
import ctypes
from SettingsHandler import GetSettings

class Nat2:
    def __init__(self, X: int, Y: int):
        self.X = X
        self.Y = Y
    
    def __add__(self, other):
        # If adding another Nat2 instance
        if isinstance(other, Nat2):
            return Nat2(self.X + other.X, self.Y + other.Y)
        # If adding an integer to both X and Y
        elif isinstance(other, int):
            return Nat2(self.X + other, self.Y + other)
        # If adding an unsupported type, raise an error
        else:
            return NotImplemented
    
    def __repr__(self):
        return f'Nat2({self.X}, {self.Y})'
        
class Rect:
    def __init__(self, XY: Nat2, WH: Nat2):
        self.XY = XY
        self.WH = WH

class Vec4:
    def __init__(self, X: float, Y: float, Z: float, W: float = 1):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.W = W

    def ToSdl2Color(self):
        return sdl2ext.Color(int(self.X * 255), int(self.Y * 255), int(self.Z * 255), int(self.W * 255))

def TupleToVec4(t: tuple[int, int, int]) -> Vec4:
    return Vec4(t[0], t[1], t[2])

def ColorPaletteToVec4(l: list[tuple]) -> list[Vec4]:
    return list([TupleToVec4(tup) for tup in l])

class UiManager:
    def __init__(self):
        # Initialize SDL and TTF
        sdl2.SDL_Init(sdl2.SDL_INIT_VIDEO)
        sdlttf.TTF_Init()
        
        self.Window = sdl2.SDL_CreateWindow(
            b"ChannelNotif",
            sdl2.SDL_WINDOWPOS_CENTERED,
            sdl2.SDL_WINDOWPOS_CENTERED,
            848, 480, sdl2.SDL_WINDOW_SHOWN
        )
        
        # Use SDL_RENDERER_PRESENTVSYNC for smooth rendering and double buffering
        self.Renderer = sdl2.SDL_CreateRenderer(self.Window, -1, sdl2.SDL_RENDERER_ACCELERATED | sdl2.SDL_RENDERER_PRESENTVSYNC)
        
        # Get window surface for legacy purposes (if needed later)
        self.Surface = sdl2.SDL_GetWindowSurface(self.Window)
        
        self.Event = sdl2.SDL_Event()
        self.Running: bool = True
        self.Fonts = []
        self.Buttons: list[bool] = []
        self.ActiveMenu: Literal["Main", "Settings", "Schedule"] = "Main"
        
        # Initialize the list to store images and textures
        self.Images: list = []  # List to store surfaces
        self.Textures: list = []  # List to store textures
        self.CheckboxStates: dict = {}

        self.ColorPalette: list[Vec4] = ColorPaletteToVec4(GetSettings().Ui.ColorPalette)
        self.IsDarkMode: bool = GetSettings().Ui.IsDarkMode

    def GetModeIcon(self):
        return "" if not self.IsDarkMode else ""

    def SwitchMode(self):
        self.IsDarkMode = not self.IsDarkMode

    def ColorPaletteMode(self) -> list[Vec4]:
        return self.ColorPalette[::-1] if self.IsDarkMode else self.ColorPalette

    def RectBorder(self, Pos: Nat2, Size: Nat2, ColorIdx: int, Thickness: int = 1):
        """
        Draws a border for a rectangle at a specified position and size using `self.Rect`.

        Parameters:
            Pos (Nat2): Top-left position of the rectangle.
            Size (Nat2): Width and height of the rectangle.
            Color (Vec4): RGBA color of the border.
            Thickness (int): Thickness of the border lines.
        """
        # Top border
        self.Rect(Pos, Nat2(Size.X, Thickness), ColorIdx)
        # Left border
        self.Rect(Pos, Nat2(Thickness, Size.Y), ColorIdx)
        # Bottom border
        self.Rect(Nat2(Pos.X, Pos.Y + Size.Y - Thickness), Nat2(Size.X, Thickness), ColorIdx)
        # Right border
        self.Rect(Nat2(Pos.X + Size.X - Thickness, Pos.Y), Nat2(Thickness, Size.Y), ColorIdx)

    def Checkbox(self, Label: str, Pos: Nat2, ColorBorderIdx: int, ColorInnerIdx: int, ColorInnerHoverIdx: int, ColorTextIdx: int) -> bool:
        ColorBorder = ColorBorderIdx
        ColorInner = ColorInnerIdx
        """
        Render a checkbox UI component and toggle its state when clicked.

        Parameters:
            Label (str): The label to display next to the checkbox.
            Pos (Nat2): The position of the checkbox (top-left corner of the checkbox).
            ColorBorder (Vec4): The color of the checkbox border.
            ColorInner (Vec4): The color of the checkbox when checked.

        Returns:
            bool: The current state of the checkbox (True for checked, False for unchecked).
        """
        # Define the checkbox size
        CheckboxSize = Nat2(20, 20)

        # Define the checkbox rectangle
        CheckboxRect = Rect(Pos, CheckboxSize)

        # Draw the checkbox border
        self.RectBorder(Pos, CheckboxSize, ColorIdx=ColorBorder, Thickness=2)

        # Initialize the checkbox states and mouse state tracker if not already
        if not hasattr(self, "CheckboxStates"):
            self.CheckboxStates = {}
        if Label not in self.CheckboxStates:
            self.CheckboxStates[Label] = {"checked": False, "mouse_down": False}

        # Handle mouse hover and click for toggling the state
        if self.RectIsHover(CheckboxRect):
            if not self.CheckboxStates[Label]["checked"]:
                self.Rect(Pos + Nat2(4, 4), Nat2(CheckboxSize.X - 8, CheckboxSize.Y - 8), ColorIdx=ColorInnerHoverIdx)
            if self.CheckboxStates[Label]["checked"]:
                self.Rect(Pos + Nat2(4, 4), Nat2(CheckboxSize.X - 8, CheckboxSize.Y - 8), ColorIdx=ColorInner)
            if self.IsClick("Left"):
                # Only toggle state when the mouse button transitions from "up" to "down"
                if not self.CheckboxStates[Label]["mouse_down"]:
                    self.CheckboxStates[Label]["checked"] = not self.CheckboxStates[Label]["checked"]
                    self.CheckboxStates[Label]["mouse_down"] = True
            else:
                # Reset the "mouse_down" state when the button is released
                self.CheckboxStates[Label]["mouse_down"] = False

        # Draw the filled rectangle if checked
        if self.CheckboxStates[Label]["checked"]:
            self.Rect(Pos + Nat2(4, 4), Nat2(CheckboxSize.X - 8, CheckboxSize.Y - 8), ColorIdx=ColorInner)

        # Render the label
        LabelPos = Pos + Nat2(CheckboxSize.X + 10, 0)
        self.Text(Label, LabelPos, FontIdx=1, ColorIdx=ColorTextIdx)

        return self.CheckboxStates[Label]["checked"]

    def ChangeActiveMenu(self, MenuName: str):
        self.ActiveMenu = MenuName

    def GetMouseState(self):
        """Get the current cursor position and mouse button states."""
        x_pos = ctypes.c_int(0)
        y_pos = ctypes.c_int(0)
        
        # Get the mouse position and button states
        button_state = sdl2.SDL_GetMouseState(ctypes.byref(x_pos), ctypes.byref(y_pos))
        
        return x_pos.value, y_pos.value, button_state

    def IsClick(self, Button: Literal["Left", "Right", "Middle"]) -> bool:
        """Check if the specified mouse button is currently clicked."""
        _, _, button_state = self.GetMouseState()

        if Button == "Left":
            return bool(button_state & sdl2.SDL_BUTTON(sdl2.SDL_BUTTON_LEFT))
        elif Button == "Right":
            return bool(button_state & sdl2.SDL_BUTTON(sdl2.SDL_BUTTON_RIGHT))
        elif Button == "Middle":
            return bool(button_state & sdl2.SDL_BUTTON(sdl2.SDL_BUTTON_MIDDLE))
        else:
            raise ValueError("Button must be 'Left', 'Right', or 'Middle'")

    def RectIsHover(self, TRect: Rect):
        return self.PointInsideRect(self.GetCursorPosition(), TRect.XY, TRect.WH)

    def ColorOnHover(self, TRect: Rect, Color1Idx: int, Color2Idx: int):
        return Color1Idx if self.RectIsHover(TRect) else Color2Idx

    def PointInsideRect(self, Point: Nat2, RectPos: Nat2, RectSize: Nat2) -> bool:
        return RectPos.X <= Point.X <= RectPos.X + RectSize.X and RectPos.Y <= Point.Y <= RectPos.Y + RectSize.Y

    def GetCursorPosition(self):
        """Get the current cursor position relative to the window."""
        x_pos = ctypes.c_int(0)
        y_pos = ctypes.c_int(0)
        sdl2.SDL_GetMouseState(ctypes.byref(x_pos), ctypes.byref(y_pos))
        return Nat2(x_pos.value, y_pos.value)

    def Update(self):
        """Update the display surface."""
        sdl2.SDL_UpdateWindowSurface(self.Window)

    def CreateButton(self):
        self.Buttons.append([False, False])

    def Button(self, Label: str, Pos: Nat2, OnClick: any, ButtonIdx: int, ColorTextIdx: int, ColorHoverIdx: int, ColorNormalIdx: int, FontIdx: int = 0):
        TextRect: Rect = self.Text(Label, Pos, FontIdx, ColorTextIdx, NoDraw=True)
        ButtonRect: Rect = Rect(TextRect.XY + -10, TextRect.WH + 20)

        Color = self.ColorOnHover(ButtonRect, ColorHoverIdx, ColorNormalIdx)

        if self.RectIsHover(ButtonRect):
            self.Buttons[ButtonIdx][1] = True
            if self.IsClick("Left") and not self.Buttons[ButtonIdx][0]:
                OnClick()
                self.Buttons[ButtonIdx][0] = True
            elif not self.IsClick("Left") and self.Buttons[ButtonIdx][0]:
                self.Buttons[ButtonIdx][0] = False
        else:
            self.Buttons[ButtonIdx][0] = False
            self.Buttons[ButtonIdx][1] = False

        self.Rect(Pos + -10, ButtonRect.WH, ColorIdx=Color)
        self.Text(Label, Pos, FontIdx, ColorTextIdx)  

        return Rect(Pos + -10, ButtonRect.WH) 

    def Rect(self, Pos: Nat2, Size: Nat2, ColorIdx: int):
        """Draw a rectangle on the surface."""
        Color = self.ColorPaletteMode()[ColorIdx]
        ColorSdl = Color.ToSdl2Color()
        RectSdl = sdl2.SDL_Rect(Pos.X, Pos.Y, Size.X, Size.Y)
        sdl2.SDL_FillRect(self.Surface, RectSdl, sdl2.SDL_MapRGBA(self.Surface.contents.format,
                                                                  ColorSdl.r, ColorSdl.g, ColorSdl.b, ColorSdl.a))
    
    def LoadFont(self, Filepath: str, Size: int = 24, Bold: bool = False):
        """Load a TTF font into the UiManager."""
        Font = sdlttf.TTF_OpenFont(Filepath.encode('utf-8'), Size)
        if Bold:
            sdl2.sdlttf.TTF_SetFontStyle(Font, sdl2.sdlttf.TTF_STYLE_BOLD)
        self.Fonts.append(Font)
        if not Font:
            raise RuntimeError(f"Failed to load font from {Filepath}: {sdl2.SDL_GetError().decode('utf-8')}")

    def Text(self, Str: str, Pos: Nat2, FontIdx: int, ColorIdx: int, NoDraw: bool = False) -> Rect:
        """Render text on the surface."""
        Color = self.ColorPaletteMode()[ColorIdx]
        if len(self.Fonts) == 0:
            raise RuntimeError("No font loaded. Use LoadFont() before rendering text.")
        
        # Convert the color
        ColorSdl = sdl2.SDL_Color(int(Color.X * 255), int(Color.Y * 255), int(Color.Z * 255), int(Color.W * 255))
        
        # Render the text to an SDL surface
        TextSurface = sdlttf.TTF_RenderUTF8_Blended(self.Fonts[FontIdx], Str.encode('utf-8'), ColorSdl)
        if not TextSurface:
            raise RuntimeError(f"Failed to render text: {sdl2.SDL_GetError().decode('utf-8')}")
        
        # Blit the text surface onto the window surface
        TextRect = sdl2.SDL_Rect(Pos.X, Pos.Y, TextSurface.contents.w, TextSurface.contents.h)
        Rxy = Nat2(TextRect.x, TextRect.y)
        Rwh = Nat2(TextRect.w, TextRect.h)
        RRect = Rect(Rxy, Rwh)
        if not NoDraw: sdl2.SDL_BlitSurface(TextSurface, None, self.Surface, TextRect)
        
        # Free the temporary text surface
        sdl2.SDL_FreeSurface(TextSurface)
        return RRect

    def TextWrapped(self, Str: str, Pos: Nat2, FontIdx: int, ColorIdx: int):
        Strings = Str.split("\n")
        for Idx, String in enumerate(Strings):
            if String == "":
                continue
            self.Text(String, Pos + Nat2(0, Idx * 16), FontIdx=FontIdx, ColorIdx=ColorIdx)

    def MainLoop(self):
        """Render each frame."""
        while sdl2.SDL_PollEvent(ctypes.byref(self.Event)) != 0:
            if self.Event.type == sdl2.SDL_QUIT:
                self.Running = False
                break
        
        sdl2.SDL_RenderPresent(self.Renderer)
        self.Update()
        sdl2.SDL_Delay(1)

    def Quit(self):
        """Clean up resources."""
        for Font in self.Fonts:
            sdlttf.TTF_CloseFont(Font)
        sdl2.SDL_DestroyWindow(self.Window)
        sdl2.SDL_Quit()
        sdlttf.TTF_Quit()
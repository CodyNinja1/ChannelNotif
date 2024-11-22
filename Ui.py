from typing import Literal
import sdl2
import sdl2.ext as sdl2ext
import sdl2.sdlttf as sdlttf
import ctypes

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
        
class Rect:
    def __init__(self, XY: Nat2, WH: Nat2):
        self.XY = XY
        self.WH = WH

class Vec4:
    def __init__(self, X: float, Y: float, Z: float, W: float):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.W = W

    def ToSdl2Color(self):
        return sdl2ext.Color(int(self.X * 255), int(self.Y * 255), int(self.Z * 255), int(self.W * 255))

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
        self.Surface = sdl2.SDL_GetWindowSurface(self.Window)
        self.Event = sdl2.SDL_Event()
        self.Running: bool = True
        self.Fonts = []
        self.Buttons: list[bool] = []

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

    def ColorOnHover(self, TRect: Rect, Color1: Vec4, Color2: Vec4):
        return Color1 if self.PointInsideRect(self.GetCursorPosition(), TRect.XY, TRect.WH) else Color2

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
        self.Buttons.append(False)

    def Button(self, Label: str, Pos: Nat2, OnClick: any, ButtonIdx: int):
        TextRect: Rect = self.Text(Label, Pos, 0, Vec4(0.8, 0.8, 0.8, 1), NoDraw=True)
        ButtonRect: Rect = Rect(TextRect.XY + -20, TextRect.WH + 40)

        Color = self.ColorOnHover(ButtonRect, Vec4(0.4, 0.4, 0.4, 1), Vec4(0.2, 0.2, 0.2, 1))

        if self.RectIsHover(ButtonRect):
            if self.IsClick("Left") and not self.Buttons[ButtonIdx]:
                OnClick()
                self.Buttons[ButtonIdx] = True
            elif not self.IsClick("Left") and self.Buttons[ButtonIdx]:
                self.Buttons[ButtonIdx] = False
        else:
            self.Buttons[ButtonIdx] = False

        self.Rect(Pos + -20, (TextRect.WH + 40), Color=Color)
        self.Text(Label, Pos, 0, Vec4(0.8, 0.8, 0.8, 1))   

    def Rect(self, Pos: Nat2, Size: Nat2, Color: Vec4 = Vec4(1, 0, 1, 1)):
        """Draw a rectangle on the surface."""
        ColorSdl = Color.ToSdl2Color()
        RectSdl = sdl2.SDL_Rect(Pos.X, Pos.Y, Size.X, Size.Y)
        sdl2.SDL_FillRect(self.Surface, RectSdl, sdl2.SDL_MapRGBA(self.Surface.contents.format,
                                                                  ColorSdl.r, ColorSdl.g, ColorSdl.b, ColorSdl.a))
    def RectGradientHorizontal(self, Pos: Nat2, Size: Nat2, StartColor: Vec4, EndColor: Vec4):
        """Draw a rectangle with a horizontal gradient, supporting transparency."""
        # Enable blending on the surface for transparency
        
        for x in range(Size.X):
            # Interpolate the color for this column
            t = x / Size.X  # Interpolation factor (0.0 to 1.0)
            interpolated_color = Vec4(
                StartColor.X + t * (EndColor.X - StartColor.X),
                StartColor.Y + t * (EndColor.Y - StartColor.Y),
                StartColor.Z + t * (EndColor.Z - StartColor.Z),
                StartColor.W + t * (EndColor.W - StartColor.W),
            )
            
            # Convert to SDL_Color
            ColorSdl = interpolated_color.ToSdl2Color()
            
            # Draw a vertical line (1-pixel wide rect)
            VerticalRect = sdl2.SDL_Rect(Pos.X + x, Pos.Y, 1, Size.Y)
            sdl2.SDL_FillRect(self.Surface, VerticalRect, sdl2.SDL_MapRGBA(
                self.Surface.contents.format,
                ColorSdl.r, ColorSdl.g, ColorSdl.b, ColorSdl.a
            ))
    def LoadFont(self, Filepath: str, Size: int = 24, Bold: bool = False):
        """Load a TTF font into the UiManager."""
        Font = sdlttf.TTF_OpenFont(Filepath.encode('utf-8'), Size)
        if Bold:
            sdl2.sdlttf.TTF_SetFontStyle(Font, sdl2.sdlttf.TTF_STYLE_BOLD)
        self.Fonts.append(Font)
        if not Font:
            raise RuntimeError(f"Failed to load font from {Filepath}: {sdl2.SDL_GetError().decode('utf-8')}")

    def Text(self, Str: str, Pos: Nat2, FontIdx: int, Color: Vec4 = Vec4(0.8, 0.8, 0.8, 1), NoDraw: bool = False) -> Rect:
        """Render text on the surface."""
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

    def MainLoop(self):
        """Render each frame."""
        self.Update()
        while sdl2.SDL_PollEvent(ctypes.byref(self.Event)) != 0:
            if self.Event.type == sdl2.SDL_QUIT:
                self.Running = False
                break
        sdl2.SDL_Delay(10)

    def Quit(self):
        """Clean up resources."""
        for Font in self.Fonts:
            sdlttf.TTF_CloseFont(Font)
        sdl2.SDL_DestroyWindow(self.Window)
        sdl2.SDL_Quit()
        sdlttf.TTF_Quit()
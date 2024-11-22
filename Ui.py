from typing import Literal
import sdl2
import sdl2.ext as sdl2ext
import sdl2.sdlttf as sdlttf
import ctypes
import requests
from PIL import Image
from io import BytesIO

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

    def LoadImageFromUrl(self, Url: str):
        """Load an image from the given URL and store it in the Images list."""
        # Fetch the image data from the URL
        response = requests.get(Url)
        response.raise_for_status()  # Raise an error if the request failed
        
        # Open the image using PIL
        img = Image.open(BytesIO(response.content))
        img = img.convert("RGBA")  # Ensure the image is in RGBA format
        
        # Get the image width and height
        width, height = img.size
        
        # Convert the image to raw bytes and create an SDL surface
        img_data = img.tobytes()
        sdl_surface = sdl2.SDL_CreateRGBSurfaceFrom(
            img_data, width, height, 32, width * 4, 0x000000FF, 0x0000FF00, 0x00FF0000, 0xFF000000
        )
        
        # Check if surface creation succeeded
        if not sdl_surface:
            raise RuntimeError(f"Failed to create SDL surface from image: {sdl2.SDL_GetError().decode('utf-8')}")

        # Create a texture from the SDL surface
        texture = sdl2.SDL_CreateTextureFromSurface(self.Renderer, sdl_surface)
        
        # Check if texture creation succeeded
        if not texture:
            raise RuntimeError(f"Failed to create texture from surface: {sdl2.SDL_GetError().decode('utf-8')}")

        # Append the surface and texture to their respective lists
        self.Images.append(sdl_surface)
        self.Textures.append(texture)

    def RenderImage(self, ImageIdx: int, Pos: Nat2):
        """Render the image stored at ImageIdx to the window at the specified position."""
        if ImageIdx < 0 or ImageIdx >= len(self.Textures):
            raise ValueError(f"Image index {ImageIdx} is out of range.")
        
        # Get the texture from the Textures list
        texture = self.Textures[ImageIdx]
        
        # Get the width and height of the image from the corresponding SDL surface
        sdl_surface = self.Images[ImageIdx]
        image_width = sdl_surface.contents.w
        image_height = sdl_surface.contents.h
        
        # Define the SDL_Rect for the position and size of the image
        image_rect = sdl2.SDL_Rect(Pos.X, Pos.Y, image_width, image_height)
        
        # Clear the screen once at the start of the frame
        sdl2.SDL_RenderClear(self.Renderer)
        
        # Render the texture to the window
        sdl2.SDL_RenderCopy(self.Renderer, texture, None, ctypes.byref(image_rect))
        
        # Present the renderer (update the screen with the new frame)
        sdl2.SDL_RenderPresent(self.Renderer)

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

    def ColorOnHover(self, TRect: Rect, Color1: Vec4, Color2: Vec4):
        return Color1 if self.RectIsHover(TRect) else Color2

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

    def Button(self, Label: str, Pos: Nat2, OnClick: any, ButtonIdx: int, FontIdx: int = 0):
        TextRect: Rect = self.Text(Label, Pos, FontIdx, Vec4(0.8, 0.8, 0.8, 1), NoDraw=True)
        ButtonRect: Rect = Rect(TextRect.XY + -10, TextRect.WH + 20)

        Color = self.ColorOnHover(ButtonRect, Vec4(0.4, 0.4, 0.4, 1), Vec4(0.2, 0.2, 0.2, 1))

        if self.RectIsHover(ButtonRect):
            if self.IsClick("Left") and not self.Buttons[ButtonIdx]:
                OnClick()
                self.Buttons[ButtonIdx] = True
            elif not self.IsClick("Left") and self.Buttons[ButtonIdx]:
                self.Buttons[ButtonIdx] = False
        else:
            self.Buttons[ButtonIdx] = False

        self.Rect(Pos + -10, ButtonRect.WH, Color=Color)
        self.Text(Label, Pos, FontIdx, Vec4(0.8, 0.8, 0.8, 1))  

        return Rect(Pos + -10, ButtonRect.WH) 

    def Rect(self, Pos: Nat2, Size: Nat2, Color: Vec4 = Vec4(1, 0, 1, 1)):
        """Draw a rectangle on the surface."""
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

    def TextWrapped(self, Str: str, Pos: Nat2, FontIdx: int, Color: Vec4 = Vec4(0.8, 0.8, 0.8, 1)):
        Strings = Str.split("\n")
        for Idx, String in enumerate(Strings):
            self.Text(String, Pos + Nat2(0, Idx * 16), FontIdx=FontIdx, Color=Color)

    def MainLoop(self):
        """Render each frame."""
        while sdl2.SDL_PollEvent(ctypes.byref(self.Event)) != 0:
            if self.Event.type == sdl2.SDL_QUIT:
                self.Running = False
                break
        
        sdl2.SDL_RenderPresent(self.Renderer)
        self.Update()
        sdl2.SDL_Delay(10)

    def Quit(self):
        """Clean up resources."""
        for Font in self.Fonts:
            sdlttf.TTF_CloseFont(Font)
        sdl2.SDL_DestroyWindow(self.Window)
        sdl2.SDL_Quit()
        sdlttf.TTF_Quit()
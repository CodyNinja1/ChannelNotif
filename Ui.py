import pygame

class Vec4:
    def __init__(self, X: float, Y: float, Z: float, W: float):
        self.X = X
        self.Y = Y
        self.Z = Z
        self.W = W
    
    def ToPygameColor(self) -> pygame.Color:
        return pygame.Color(int(self.X * 255), int(self.Y * 255), int(self.Z * 255), a=int(self.W * 255))

class Vec2:
    def __init__(self, X: float, Y: float):
        self.X = X
        self.Y = Y
    
    def ToPygameCoord(self):
        return (self.X, self.Y)

class UiElement:
    def __init__(self, Pos: Vec2, Size: Vec2, Color: Vec4=Vec4(1, 0, 1, 1)):
        self.Pos = Pos
        self.Size = Size
        self.Color = Color
    
    def Render(self):
        pass

class UiRect(UiElement):
    def __init__(self, Pos: Vec2, Size: Vec2, Color: Vec4=Vec4(1, 0, 1, 1)):
        super().__init__(Pos, Size, Color)
    
    def Render(self, Screen: pygame.Surface):
        pygame.draw.rect(Screen, self.Color.ToPygameColor(), pygame.Rect(self.Pos.ToPygameCoord(), self.Size.ToPygameCoord()))

class UiPage:
    def __init__(self):
        self.Elements: list[UiElement] = []
    
    def Render(self, Screen: pygame.Surface):
        for Element in self.Elements:
            Element.Render(Screen)
from Log import Logger
import pygame
from Ui import *

Log = Logger()

ActivePage: UiPage = None

def Launch():
    global ActivePage
    Log.Log("[FRONTEND] Frontend launched.")

    pygame.init()
    pygame.font.init()
    screen = pygame.display.set_mode((828, 480))
    pygame.display.set_caption("ChannelNotif")
    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill("black")

        if ActivePage == None:
            ActivePage = UiPage()
            ActivePage.Elements.append(UiRect(Vec2(10, 10), Vec2(100, 100)))
        
        ActivePage.Render(Screen=screen)

        pygame.display.flip()

        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    Launch()
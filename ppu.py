# Example file showing a basic pygame "game loop"
import pygame

import keyboard as k

r = k.KEY_MAPPINGS


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()
running = True
def Drawpixel(x,y):

    PIXEL_ON = pygame.Rect(x * 16, y * 16 , 16, 16 ) #each pixle from the 64*32 is rescaled to 1024 * 512
    pygame.draw.rect(screen, "white", PIXEL_ON)

def Deletepixel(x,y):
    PIXEL_ON = pygame.Rect(x * 16, y * 16 , 16, 16 ) #each pixle from the 64*32 is rescaled to 1024 * 512
    pygame.draw.rect(screen, "black", PIXEL_ON)

def clear():
    for i in range(1,17):
        for j in range(1,17):
            Deletepixel(i,j)
while running:
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # RENDER YOUR GAME HERE
    Drawpixel(3, 3) # any pixel you want just multiply it with 16
    # flip() the display to put your work on screen
    pygame.display.flip()


    clock.tick(60)  # limits FPS to 60

pygame.quit()

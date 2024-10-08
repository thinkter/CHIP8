# Example file showing a basic pygame "game loop"
import pygame

import keyboard as k




#============================CHIP8 DEFINATIONS=======================

class Chip8():
    memory = [0] * 4096
    reg = [0]* 16 
    display = [0] * 64*32
    key_inputs = [0]*16
    soundTimer = 0
    delayTimer = 0
    index = 0
    pc = 0
    stack = []
    opcode = 0
    shouldDraw = False
    fonts = [0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
           0x20, 0x60, 0x20, 0x20, 0x70, # 1
           0xF0, 0x10, 0xF0, 0x80, 0xF0, # 2
           0xF0, 0x10, 0xF0, 0x10, 0xF0, # 3
           0x90, 0x90, 0xF0, 0x10, 0x10, # 4
           0xF0, 0x80, 0xF0, 0x10, 0xF0, # 5
           0xF0, 0x80, 0xF0, 0x90, 0xF0, # 6
           0xF0, 0x10, 0x20, 0x40, 0x40, # 7
           0xF0, 0x90, 0xF0, 0x90, 0xF0, # 8
           0xF0, 0x90, 0xF0, 0x10, 0xF0, # 9
           0xF0, 0x90, 0xF0, 0x90, 0x90, # A
           0xE0, 0x90, 0xE0, 0x90, 0xE0, # B
           0xF0, 0x80, 0x80, 0x80, 0xF0, # C
           0xE0, 0x90, 0x90, 0x90, 0xE0, # D
           0xF0, 0x80, 0xF0, 0x80, 0xF0, # E
           0xF0, 0x80, 0xF0, 0x80, 0x80  # F
           ]
    
#   push this to the initializing part    
    for i in range(0,80):
        memory[i] = fonts[i]


    def loadRom(self, rom_path):
        binary = open(rom_path , "rb").read()
        for i in range(len(binary)):
            self.memory[0x200 + i] = binary[i]

#    def cycle(self):            



#=============================PPU================================================
r = k.KEY_MAPPINGS


# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()
running = True
#====================DRAW AND DELETE FUNCTIONS====================================


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



#======================THE RENDERING HAPPENS THERE================================
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

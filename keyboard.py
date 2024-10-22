import pygame


import sys

 
 
KEY_MAPPINGS = {
    pygame.K_q : 0x1,
    pygame.K_w : 0x2,
    pygame.K_e : 0x0,
    pygame.K_r : 0x3,
    pygame.K_t : 0x4,
    pygame.K_y : 0x5,
    pygame.K_u : 0x6,
    pygame.K_i : 0x7,
    pygame.K_o : 0x8,
    pygame.K_p : 0x9,
    pygame.K_a : 0xA,
    pygame.K_s : 0xB,
    pygame.K_d : 0xC,
    pygame.K_f : 0xD,
    pygame.K_g : 0xE,
    pygame.K_h : 0xF,
    }
# importing sys module
# importing sys module
# initialising pygame
pygame.init()
 
# creating display
display = [0] * 64 * 32
screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()
def Drawpixel(x,y):
    PIXEL_ON = pygame.Rect(x * 16, y * 16 , 16, 16 ) #each pixle from the 64*32 is rescaled to 1024 * 512
    pygame.draw.rect(screen, "white", PIXEL_ON)
    if x > 64:
        x = x - 64
    elif x < 0:
        x = 64 + x
    if y > 32:
        y = y - 32
    elif y < 0:
        y = 32 + y

    pixelLoc = x + (y*64) 
    display[pixelLoc] = display[pixelLoc] ^ 1



def CLS():
    display = [0] * 64 * 32
#    for i in range(0, 64):
#        for j in range(0, 32):
#            PIXEL_ON = pygame.Rect(i * 16, j * 16 , 16, 16 ) #each pixle from the 64*32 is rescaled to 1024 * 512
#            pygame.draw.rect(screen, "black", PIXEL_ON)

# creating a running loop
Drawpixel(63 ,31)
while True:

    #screen.fill("black")
    
    # creating a loop to check events that
    # are occurring
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
         
        # checking if keydown event happened or not
        if event.type == pygame.KEYDOWN:
            key = event.key

            if key in KEY_MAPPINGS:
                print("haah") 
                PIXEL_ON = pygame.Rect(63 * 16, 31 * 16 , 16, 16 ) #each pixle from the 64*32 is rescaled to 1024 * 512
                pygame.draw.rect(screen, "black", PIXEL_ON)
            # if keydown event happened
            # than printing a string to output
            print("A key has been pressed")


    
    pygame.display.flip()
    clock.tick(60)

pygame.quit()

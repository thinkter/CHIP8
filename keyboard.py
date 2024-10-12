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
display = pygame.display.set_mode((300, 300))
 
fps = 60
# creating a running loop
while True:
    fpsInterval = 1000/fps

    
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
            # if keydown event happened
            # than printing a string to output
            print("A key has been pressed")
import pygame
import random as r
import time

display = [0] * 64 * 32
registers = [0] * 16
stack = [0] * 16
keypad = [0] * 16
opcode = 0
screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()
fps = 60
index = 0
memory = [0] * 4096
randByte = r.randint(0, 255)

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

START_ADDRESS = 0x200
FONT_START_ADDRESS = 0x50

j = 0
while j < 80:
    memory[FONT_START_ADDRESS + j] = fonts[j]
    j += 1


#6XNN (set register VX) done
#1NNN (jump) done
#00E0 (clear screen) done
#7XNN (add value to register VX) done
#ANNN (set index register I) done
#DXYN (display/draw) ig done? gotta figure it outtt

def CLS():
    display = [0] * 64 * 32
    screen.fill("black")   

def JMP():
    #jump location to NNN
    #interpreter sets pc to nnn
    addr = opcode and 0x0FFF

    pc = addr

def OP_6xkk():
    # puts kk into register x
    Vx = (opcode and 0x0f00) >> 8
    byte = opcode and 0x00ff

    registers[Vx] = byte

def OP_7xkk():
    Vx = (opcode and 0x0f00) >> 8
    byte = opcode and 0x00ff

    registers[Vx] += byte
def OP_Annn():
    addr = opcode and 0x0fff
    index = addr


#this shit is incomplete
#figure out the draw and few more opcodes and then figure out cycle and other shit
def Draw():
    Vx = (opcode and 0x0f00) >> 8
    Vy = (opcode and 0x00f0) >> 4
    height = opcode and 0x000f

    xPos = registers[Vx] % 64
    yPos = registers[Vy] % 32

    registers[0xF] = 0

    row = 0
    while row < height:
        row +=1
        spriteByte = memory[index + row]

        col = 0
        while col > 8:
            col += 1
            spritePixel = spriteByte and (0x80 >> col)
            screenPixel = display[(yPos + row) * 64 + (xPos + col)]
            
            if(spritePixel):
                if(spritePixel == 0xFFFFFFFF):
                    registers[0xf] = 1

                screenPixel = screenPixel ^ 0xFFFFFFFF

def loadRom(rom_path):
    binary = open(rom_path , "rb").read()
    for i in range(len(binary)):
        memory[START_ADDRESS + i] = binary[i]

def Drawpixel(x,y):
    PIXEL_ON = pygame.Rect(x * 16, y * 16 , 16, 16 ) #each pixel from the 64*32 is rescaled to 1024 * 512
    pygame.draw.rect(screen, "white", PIXEL_ON)

def cycle(pc):
    opcode = memory[pc] << 8 | memory[pc + 1]
    #print(memory[pc])
    #print(memory[pc])
    time.sleep(0.1)

    print(hex(opcode))
   # print(hex(pc))
    if opcode == 0x00e0:
        CLS()
        print("CLS")
    elif (opcode and 0xF000) == 0x1000:
        #JUMP
        JMP()
        print("JMP")
    elif (opcode and 0xF000) == 0x6000:
        #set register
        OP_6xkk()
        print("6XNN")
    elif (opcode and 0xF000) == 0x7000:
        #add value to register
        OP_7xkk()
        print("7XNN")
    elif (opcode and 0xf0) == 0xa0:
        #set index register
        OP_Annn()
        print("ANNN")

running = True
screen.fill("black")
#Drawpixel(10,10)

#loadRom("IBM Logo.ch8")


memory[0x201]= 0xa2
pc = START_ADDRESS
while running:
    
    #figure out how to keep checking display for changes and draw the pixels which get updated in it
    #formulae display index = x + (y-1) * 64
    #loop through display and check which all pixels are 1
    #find their x and y through index
    #display index should return x and y coords of the pixel
    #display that value

    #yeah so this fucking works which is sickkkk
    for i in range(0 , len(display)):
        if display[i] == 1:
            y = i // 64
            x = i -(y * 64)
            Drawpixel(x,y)

    cycle(pc)
    pc = pc + 2  
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            key = event.key
            if key in KEY_MAPPINGS:
                print("maa chudao maa chudao garam hai garma hai")
    pygame.display.flip()
    clock.tick(fps)

pygame.quit()
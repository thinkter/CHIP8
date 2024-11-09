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


#6XNN (set register VX) done registers storing is working
#1NNN (jump) idk
#00E0 (clear screen) done
#7XNN (add value to register VX) done
#ANNN (set index register I) actually works 
#DXYN (display/draw) i

def CLS():
    display = [0] * 64 * 32
    screen.fill("black")   

def JMP(opcode):
    #jump location to NNN
    #interpreter sets pc to nnn
    addr = opcode &  0x0FFF
    return addr
    #pc = addr

def OP_6xkk(opcode):
    # puts kk into register x
    global registers
    Vx = (opcode & 0x0f00) >> 8
    byte = opcode & 0x00ff

    registers[Vx] = byte
    #print(hex(byte))
    #print(registers)

def OP_7xkk(opcode):
    global registers
    Vx = (opcode & 0x0f00) >> 8
    byte = opcode & 0x00ff
    registers[Vx] += byte
    #print(hex(byte))
    #print(registers)
def OP_Annn(opcode):
    addr = opcode & 0x0fff
    return addr
    #print(hex(index))


# ADD THESE TO THE cycle
    
def OP_Call(opcode):
    #2nnn
    global pc
    global stack
    global sp
    stack[sp] = pc
    sp = sp + 1 
    pc = (opcode & 0xfff)


def OP_RET(opcode):
    global sp
    global pc
    sp = sp - 1
    stack[sp] = pc

def OP_3xkk(opcode):
    global pc
    Vx = (opcode & 0x0f00) >> 8
    kk = opcode & 0xff

    if (Vx == kk):
        pc = pc + 2
def OP_4xkk(opcode):
    global pc

    Vx = (opcode & 0x0f00) >> 8
    kk = opcode & 0xff

    if(Vx != kk):
        pc = pc + 2

def OP_5xy0(opcode):
    global pc

    vx = (opcode & 0x0f00 )>> 8
    vy = (opcode & 0x00f0) >> 4

    if vx == vy:
        pc = pc + 2
def OP_8xy0(opcode):
    global registers

    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4

    registers[Vx] = registers[Vy]
def OP_8xy1(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4

    registers[Vx] = registers[Vx] | registers[Vy]
def OP_8xy2(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4

    registers[Vx] = registers[Vx] & registers[Vy]
def OP_8xy3(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4

    registers[Vx] = registers[Vx] ^ registers[Vy]
def OP8xy4(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    x = registers[Vx]
    y = registers[Vy]

    registers[0xf] = 0
    add = x + y

    if add > 255:
        registers[0xf] = 1
    registers[Vx] = add

def OP_8xy5(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    x = registers[Vx]
    y = registers[Vy]
    registers[0xf] = 0
 
    registers[Vx] = x - y

    if(x > y):
        registers[0xf] = 1
def OP_8xy6(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    x = registers[Vx]
    y = registers[Vy]

    registers[0xf] = registers[Vx] & 0x1
    registers[Vx] = registers[Vy]

    registers[Vx] = registers[Vx] > 1
def OP_8xy7(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    x = registers[Vx]
    y = registers[Vy]

    registers[Vx] = y- x
    registers[0xf] = 0

    if y > x:
        registers[0xf] = 1
def OP_8xyE(opcode):
    global registers 
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    x = registers[Vx]
    y = registers[Vy]
    registers[0xf] = (x & 0x80)

    registers[Vx] = x << 1

def OP_9xy0(opcode):
    global registers 
    global pc
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    x = registers[Vx]
    y = registers[Vy]

    if x != y:
        pc = pc + 2

def OP_Bnnn(opcode):
    global registers
    global pc
    n = opcode & 0xfff
    pc = n + registers[0]

def OP_Cxkk(opcode):
    global registers
    k = opcode & 0xff
    Vx = (opcode & 0xf00) >> 8
    registers[Vx] = r.randint(0,255) & k

def OP_Ex9E(opcode):


def setPixel(x, y):
    if x > 64:
        x = x - 64
    elif x < 0:
        x = 64 + x
    if y > 32:
        y = y - 32
    elif y < 0:
        y = 32 + y
    display[x + (y * 64)] ^= 1
    return display[x + (y * 64)] != 1

#this shit is incomplete
#figure out the draw and few more opcodes and then figure out cycle and other shit
#nah this shit is dumb as fuck gotta remake this goddamn bull shit

def Draw(opcode):
    global registers
    global memory
    global index
    Vx = (opcode & 0x0f00) >>  8
    Vy = (opcode & 0x00f0) >> 4 
    height = opcode & 0x000f
    width = 8
    registers[0xf] = 0
    col = 8 
    row = 0
    while row < height:
        row = row + 1
        sprite = memory[index + row]
        col = 0
        while col < width:
            col = col + 1 
            if (sprite & 0x80) > 0 :
                if(setPixel(registers[Vx] + col , registers[Vy] + row )):
                    registers[0xf] = 1
            sprite = sprite << 1
"""
def Draw(opcode):

    global registers
    global display
    Vx = (opcode & 0x0f00) >> 8
    Vy = (opcode & 0x00f0) >> 4
    height = opcode & 0x000f
#    print(height, "height")
    xPos = registers[Vx] % 64
    yPos = registers[Vy] % 32
#    print(xPos , "XPOS" , yPos, "YPOS")
    registers[0xF] = 0

    row = 0
    while row < height:
        row +=1
        spriteByte = memory[index + row]

        col = 0
        while col < 8:
            col += 1
            spritePixel = spriteByte & (0x80 >> col)
            print(display[(yPos + row) * 64 + (xPos + col)])
            screenPixel = display[(yPos + row) * 64 + (xPos + col)]
            
            if(spritePixel):
                if(spritePixel == 0xFFFFFFFF):
                    registers[0xf] = 1

                screenPixel = screenPixel ^ 0xFFFFFFFF
"""

def loadRom(rom_path):
    binary = open(rom_path , "rb").read()
    for i in range(len(binary)):
        memory[START_ADDRESS + i] = binary[i]

def Drawpixel(x,y):
    PIXEL_ON = pygame.Rect(x * 16, y * 16 , 16, 16 ) #each pixel from the 64*32 is rescaled to 1024 * 512
    pygame.draw.rect(screen, "white", PIXEL_ON)

def cycle():
    global index
    global pc
    opcode = memory[pc] << 8 | memory[pc + 1]
    #print(memory[pc])
    #print(memory[pc])
    #time.sleep(0.1)
    pc = pc + 2
    print(hex(opcode))
   # print(hex(pc))
    if opcode == 0x00e0:
        CLS()
        print("CLS")
   
    elif (opcode & 0xf000) == 0xa000:
        #set index register
        #OP_Annn(opcode, index)
        index = OP_Annn(opcode)
        #print(hex(index))
        print("ANNN")
    elif (opcode & 0xF000) == 0x1000:
        #JUMP
        pc = JMP(opcode)
        print("JMP")
    elif (opcode & 0xF000) == 0x6000:
        #set register
        OP_6xkk(opcode)
        print("6XNN")
    elif (opcode & 0xF000) == 0x7000:
        #add value to register
        OP_7xkk(opcode)
        print("7XNN")
    elif(opcode & 0xF000) == 0xD000:
        #draw
        Draw(opcode)
        print("DXYN")


running = True
screen.fill("black")
#Drawpixel(10,10)

loadRom("IBM Logo.ch8")
#memory[0x201] = 0xe0

pc = START_ADDRESS
sp = 0 
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
    #print(hex(index))
#    print(hex(pc))
    print(registers)
    #for j in display:
    #    if j == 1:
    #        print(j , "a pixel has been active")
    cycle()
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

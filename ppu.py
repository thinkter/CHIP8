# Example file showing a basic pygame "game loop"
import pygame
import random as r

#=========================KEYBOARD==============================================
class Keyboard():
   
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

    keysPressed = []
    onNextKeyPressed = 0




#============================CHIP8 DEFINATIONS=======================

keysPressed = Keyboard.keysPressed
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
    paused = False
    speed = 10
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

    def executeInstruction(_opcode):
        #print(_opcode)
        pc = pc + 2
        x = (opcode & 0x0f00) >> 8
        y = (opcode & 0x00f0) >> 4


        match opcode & 0xf000:
            case 0x0000:
                match opcode:
                    case 0x00e0:
                        Clear()
                    case 0x00ee:
                        pc = stack.pop()
            case 0x1000:
                pc = opcode & 0x0fff
            case 0x2000:
                stack.append(pc)
                pc = opcode & 0x0fff
            case 0x3000:
                if reg[x] == (opcode & 0xff):
                    pc = pc + 2
            case 0x4000:
                if reg[x] != (opcode & 0xff):
                    pc = pc + 2
            case 0x5000:
                if reg[x] == reg[y]:
                    pc = pc + 2
            case 0x6000:
                reg[x] = (opcode & 0xff)
            case 0x7000:
                reg[x] = reg[x] + (opcode & 0xff)
            case 0x8000:
                match opcode & 0xf:
                    case 0x0:
                        reg[x] = reg[y]
                    case 0x1:
                        reg[x] = reg[x] or reg[y]
                    case 0x2:
                        reg[x] = reg[x] and reg[y]
                    case 0x3:
                        reg[x] = reg[x] ^ reg[y]
                    case 0x4:
                        sum = reg[x] + reg[y]

                        reg[0xf] = 0

                        if sum > 0xff:
                            reg[0xf] = 1
                        reg[x] = sum
                    case 0x5:
                        reg[0xf] = 0
                        if reg[x] > reg[y]:
                            reg[0xf] = 1
                        reg[x] = reg[x] - reg[y]
                    case 0x6:
                        reg[0xf] = reg[x] & 1
                        reg[x] = reg[x] >> 1
                    case 0x7:
                        reg[0xf] = 0

                        if reg[y] > reg[x]:
                            reg[0xf] = 1

                        reg[x] = reg[y] - reg[x]
                    case 0xE:
                        reg[0xf] = reg[x] & 0x80
                        reg[x] = reg[x] << 1
            case 0x9000:
                if reg[x] != reg[y]:
                    pc = pc + 2
            case 0xA000:
                index = opcode & 0xfff
            case 0xB000:
                pc = (opcode & 0xfff) + reg[0]
            case 0xC000:
                rand = r.randint(0,255) * 0xff

                reg[x] = rand & (opcode & 0xff)
            case 0xD000:
                #draw vx, vy, nibble
                width = 8
                height = opcode & 0xf

                reg[0xf] = 0
                row = 0
                while row<height:
                    row = row + 1
                    sprite = memory[index + row]

                    col = 0
                    while col<width:
                        col = col + 1
                        if (sprite & 0x80) > 0:
                            if (Drawpixel(reg[x] + col, reg[y] + row)):
                                reg[0xf] = 1

                        sprite = sprite << 1
            case 0xE000:
                match opcode & 0xff:
                    case 0x9E:
                        pc = pc + 2
                    case 0xA1:
                        if(keysPressed[reg[x]] == 0):
                            pc = pc + 2
            case 0xF000:
                match opcode & 0xff:
                    case 0x07:
                        reg[x] = delayTimer
                    case 0x0A:
                        paused = True


                    case 0x15:
                        print("asd")
                    case 0x18:
                        print("asd")
                    case 0x1E:
                        print("asd")
                    case 0x29:
                        print("asd")
                    case 0x33:
                        print("asd")
                    case 0x55:
                        print("asd")
                    case 0x65:
                        print("asd")
            case _:
                print("UNKNOWN OPCODE" + opcode)
    def updateTimers():
        if delayTimer > 0:
            delayTimer = delayTimer - 1
    def loadRom(self, rom_path):
        binary = open(rom_path , "rb").read()
        for i in range(len(binary)):
            self.memory[0x200 + i] = binary[i]

    #here is where the instrucrions are implemented
    def cycle():
        i = 0
        while i < speed:
            if (paused == False):
               opcode = memory[pc] << 8 | memory[pc + 1]
               executeInstruction(opcode)
            i = i + 1 



#=============================PPU================================================

#====================DRAW AND DELETE FUNCTIONS====================================


def Drawpixel(x,y):
    display = Chip8.display
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


def Deletepixel(x,y):
    display = Chip8.display
    PIXEL_ON = pygame.Rect(x * 16, y * 16 , 16, 16 ) #each pixle from the 64*32 is rescaled to 1024 * 512
    pygame.draw.rect(screen, "black", PIXEL_ON)
    pixelLoc = x + (y*64)
    display[pixelLoc] = display[pixelLoc] & 0

def Clear():
    display = Chip8.display
    for i in range(1,17):
        for j in range(1,17):
            Deletepixel(i,j)
    display = [0] * 64 * 32

keymaps = Keyboard.KEY_MAPPINGS



#======================THE RENDERING HAPPENS THERE================================

# pygame setup
pygame.init()
screen = pygame.display.set_mode((1024, 512))
clock = pygame.time.Clock()
running = True
fps = 60

mem = Chip8.memory
Chip8().loadRom("TETRIS")
print(mem)
while running:
    fpsInterval = 1000/fps
    # poll for events
    # pygame.QUIT event means the user clicked X to close your window
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            key = event.key

            if key in keymaps:
                keysPressed.append(keymaps[key])
                print(keysPressed)

    # fill the screen with a color to wipe away anything from last frame
    screen.fill("black")
    # RENDER YOUR GAME HERE
    Drawpixel(1, 1) # any pixel you want just multiply it with 16
    # flip() the display to put your work on screen
    pygame.display.flip()
    clock.tick(fps)  # limits FPS to 60

pygame.quit()

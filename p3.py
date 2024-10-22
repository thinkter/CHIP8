import sys
import pygame
import random

# Constants
SCREEN_WIDTH = 64
SCREEN_HEIGHT = 32
SCALE = 10
MEMORY_SIZE = 4096
REGISTER_COUNT = 16
STACK_SIZE = 16
KEY_COUNT = 16
FONTSET_START_ADDRESS = 0x50
FONTSET_SIZE = 80

# CHIP-8 fontset
FONTSET = [
    0xF0, 0x90, 0x90, 0x90, 0xF0, # 0
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

class Chip8:
    def __init__(self):
        self.memory = [0] * MEMORY_SIZE
        self.V = [0] * REGISTER_COUNT
        self.I = 0
        self.pc = 0x200
        self.gfx = [0] * (SCREEN_WIDTH * SCREEN_HEIGHT)
        self.delay_timer = 0
        self.sound_timer = 0
        self.stack = [0] * STACK_SIZE
        self.sp = 0
        self.key = [0] * KEY_COUNT
        self.draw_flag = False

        # Load fontset
        for i in range(FONTSET_SIZE):
            self.memory[FONTSET_START_ADDRESS + i] = FONTSET[i]

    def load_program(self, program):
        for i in range(len(program)):
            self.memory[0x200 + i] = program[i]
    def loadRom(self , rom_path):
        binary = open(rom_path , "rb").read()
        for i in range(len(binary)):
            self.memory[0x200 + i] = binary[i]
    def emulate_cycle(self):
        opcode = self.memory[self.pc] << 8 | self.memory[self.pc + 1]
        self.pc += 2
        print(opcode)
        # Decode and execute opcode
        # (This is a simplified example, you need to implement all CHIP-8 opcodes)
        if opcode == 0x00E0:  # CLS
            self.gfx = [0] * (SCREEN_WIDTH * SCREEN_HEIGHT)
            self.draw_flag = True
        elif opcode == 0x00EE:  # RET
            self.sp -= 1
            self.pc = self.stack[self.sp]
        elif opcode & 0xF000 == 0x1000:  # JP addr
            self.pc = opcode & 0x0FFF
        elif opcode & 0xF000 == 0x6000:  # LD Vx, byte
            x = (opcode & 0x0F00) >> 8
            self.V[x] = opcode & 0x00FF
        elif opcode & 0xF000 == 0xA000:  # LD I, addr
            self.I = opcode & 0x0FFF
        elif opcode & 0xF000 == 0xD000:  # DRW Vx, Vy, nibble
            x = self.V[(opcode & 0x0F00) >> 8]
            y = self.V[(opcode & 0x00F0) >> 4]
            height = opcode & 0x000F
            self.V[0xF] = 0
            for yline in range(height):
                pixel = self.memory[self.I + yline]
                for xline in range(8):
                    if (pixel & (0x80 >> xline)) != 0:
                        if self.gfx[(x + xline + ((y + yline) * SCREEN_WIDTH))] == 1:
                            self.V[0xF] = 1
                        self.gfx[x + xline + ((y + yline) * SCREEN_WIDTH)] ^= 1
            self.draw_flag = True

        # Update timers
        if self.delay_timer > 0:
            self.delay_timer -= 1
        if self.sound_timer > 0:
            if self.sound_timer == 1:
                print("BEEP!")
            self.sound_timer -= 1

def main():
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH * SCALE, SCREEN_HEIGHT * SCALE))
    pygame.display.set_caption("CHIP-8 Emulator")
    clock = pygame.time.Clock()

    chip8 = Chip8()

    # Load a program (this should be replaced with actual program loading)
    program = [0x60, 0x00, 0x61, 0x00, 0xA2, 0x0A, 0xD0, 0x11]
    chip8.loadRom("random_number_test.ch8")

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        chip8.emulate_cycle()

        if chip8.draw_flag:
            screen.fill((0, 0, 0))
            for y in range(SCREEN_HEIGHT):
                for x in range(SCREEN_WIDTH):
                    if chip8.gfx[x + (y * SCREEN_WIDTH)] == 1:
                        pygame.draw.rect(screen, (255, 255, 255), (x * SCALE, y * SCALE, SCALE, SCALE))
            pygame.display.flip()
            chip8.draw_flag = False

        clock.tick(60)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
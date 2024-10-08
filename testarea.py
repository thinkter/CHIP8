memory = [0] * 4096


def loadRom(rom_path):
    binary = open(rom_path , "rb").read()
    for i in range(len(binary)):
        memory[0x200 + i] = binary[i]
loadRom("TETRIS")

print(memory)

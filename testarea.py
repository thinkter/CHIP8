#memory = [0] * 4096


#def loadRom(rom_path):
#    binary = open(rom_path , "rb").read()
#    for i in range(len(binary)):
#        memory[0x200 + i] = binary[i]
##loadRom("TETRIS")

#binary = open("TETRIS" , "rb").read()
#or i in range(len(binary)):
#    memory[0x200 + i] = binary[i]



#print(memory)

a = int(input("enter a number"))

global c = 10
def ash():
    c = c + 2
    print(c)
ash()

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

a = input("enter a number")

match a:
    case 0x1000:
        print("gay")

    case 2:
        print("gaygay")
    case 3:
        print("gaygaygay")
    case 4:
        print("gaygaygaygay")
    case _:
        print("askdaksjdkadskamsoidaoiwn")
memory = [0] * 4096


binary = open("IBM Logo.ch8" , "rb").read()
for i in range(len(binary)):
    memory[0x200 + i] = binary[i]


for j in memory:
    if (j != 0): 
        print(hex(j))

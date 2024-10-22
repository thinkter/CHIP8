8bit stack pointer keeps track of the the stack

there are 16 levels of stack

fetch
decode
execute

700 instructions per second

fetchL
read instruction from pc. the instruction is 2 bytes so we have to read 
two successive byte from the memory and combine them both into one 16bit instruction

increment pc with 2


decode
basically a huge if else if statement where we are doing different things
depending on the what the first number is

execute
just do what the operation is supposed to do lmfao

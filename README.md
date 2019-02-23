# LogisimCPU

In this project, I created a Turing-complete CPU in Logisim. From this, I created some documentation showing the functionality. Running code on the CPU is difficult, as it required writing machine code. To solve this, I created a basic Assembly language that includes loading, writing, and setting values in one of a 3 registers (`REG A`, `REG B`, and `MemAddrReg`), making conditional and nonconditional jumps, and basic arithmetic (+, -, x, /). 

## The CPU


The CPU I've designed is by no means the most efficient design, but its purpose isn't to be the most efficient or the fastest, but rather as a learning experience. The design is not the same as most low-powered CPUs, as there are separate memory banks for the instructions and the usable memory. There is functionality to manipulate the contents of the instruction bank, but that is purely to alter the course of the program. Each 8-bit memory bank can hold 256 bytes of information, leading to a maximum program size of 256 bytes, and a total of 256 bytes of usable memory. There are various registers in the CPU that can each hold a small amount of information. Registers A and B can each hold a byte of information, the Memory Address Register can hold half a byte (a nibble) of information, and the Carry On Operation Register can hold a measely 1 bit of information. Combining these memory registers, there is a total of 514.625 bytes (4117 bits) of information stored at any given moment, 258 bytes being usable between the memory bank, and two main registers.

## Assembly

Abstracting the instructions from a byte of information into a language is not an easy task, but necessary for any development on a new CPU. By learning the Assembly language for a particular CPU, we can learn more about the inner workings without memorizing machine codes. The current version of the Assembly language I have put together uses 16 commands to work on the CPU. Writing out a command name and a parameter separated by a space on each line translates to a unique command from the table below. A collection of lines like this constitute a program in Assembly. Because this CPU works with 8 bit numbers, yet can only provide a nibble for a command and as a parameter, some of the commands below are required to write larger values, such as LS REG. 

| Code |   Name  | Function                             |    Input |  Output |
|:----:|:-------:|--------------------------------------|---------:|--------:|
|   0  | SET MEM | Set the 4 MSBs of the mem addr       | Mem Addr | Mem Reg |
|   1  |  LOAD A | Load from cache into Register A      |    Cache |   Reg A |
|   2  |  LOAD B | Load from cache into Register B      |    Cache |   Reg B |
|   3  | WRITE A | Write to cache from Register A       |    Reg A |   Cache |
|   4  | WRITE B | Write to cache from Register B       |    Reg B |   Cache |
|   5  | ADD A B | Write A+B to cache                   | Reg A, B |   Cache |
|   6  | SUB A B | Write A-B to cache                   | Reg A, B |   Cache |
|   7  |  SET A  | Set the value in Register A          | Mem Addr |     N/a |
|   8  |  SET B  | Set the value in Register B          | Mem Addr |     N/a |
|   9  | NC JUMP | Jump to line                         | Mem Addr |     N/a |
|   a  |  C JUMP | Jump if carry bit is 0, cont. when 1 | Mem Addr |     N/a |
|   b  | MUL A B | Write A×B to cache                   | Reg A, B |   Cache |
|   c  | DIV A B | Write A÷B to cache                   | Reg A, B |   Cache |
|   d  |  MOD IR | Write Reg A to a IR at MA in Reg B   |      N/a |      IR |
|   e  |  LS REG | Write A << 4 + B to cache            |      N/a |   Cache |
|   f  |   HALT  | Program Halts                        |      N/a |     N/a |


## The Compiler

The compiler is a way to convert the above Assembly code into machine code. Since the CPU is developed in Logisim, the file format chosen was the file format that allows reading and writing to the built in RAM modules. Below is a sample program that adds the values `e` and `a` (Decimal `14` and `10`) and stores the value in memory address 0, halting with exit code 0.

```
v2.0 raw
7e 8a 50 f0 
```

This compiler is written in python, due to its flexibility and lightweight code (the full compiler, with warnings and system argument parsing is still less than 2KB, less than the cluster size on MacOS and some other operating systems). Relative to the size of the programs this compiler is working on, the file size is daunting, being 4 times the size, but if the CPU were able to handle more information, by moving from 4 to 8 or even 16 bits, the compiler would only increase enough to accommodate any new commands.

## Integrated Development Environment

Sometimes the compiler for a language is not enough. For decent code production, an integrated development environment (IDE) is required. I built mine to be able to open, save, compile and run sample programs. This IDE is limited, but so is the language, and so is the CPU. 

# What I'm Learning
- Functionality of Turing-complete CPUs
- How to go about writing a programming language
- How to create a compiler
- How to create a simple IDE


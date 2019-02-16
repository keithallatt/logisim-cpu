"""

SIMULATED_CPU.PY



A python script that emulates the behaviour of the 4 bit CPU designed in
Logisim. As versions of the CPU evolve, this script will need to reflect those
changes.

"""
from enum import Enum, unique
import math
import time

@unique
class Instructions(Enum):
        SET_MEM = "0"
        LOAD_A = "1"
        LOAD_B = "2"
        WRITE_A = "3"
        WRITE_B = "4"
        ADD_A_B = "5"
        SUB_A_B = "6"
        SET_A = "7"
        SET_B = "8"
        NC_JUMP = "9"
        C_JUMP = "a"
        MUL_A_B = "b"
        DIV_A_B = "c"
        MOD_IR = "d"
        LS_REG = "e"
        HALT = "f"

        @staticmethod
        def find_instruction(value):
            for i in Instructions:
                if i.value == value:
                    return i


@unique
class BitWidth(Enum):
    ONE_BIT = 1
    TWO_BIT = 2  # not used
    FOUR_BIT = 4
    EIGHT_BIT = 8
    SIXTEEN_BIT = 16  # not used
    THIRTY_TWO_BIT = 32  # not used

    def max_value(self):
        return 2 ** self.value - 1

    def place_values(self) -> int:
        return int(math.ceil(math.log(self.max_value(), 16)))


class Register:
    def __init__(self, bit_width: BitWidth):
        self.bit_width = bit_width
        self.max_value = bit_width.max_value()
        self.value = 0

    def __str__(self):
        return hex(self.value)

    def set_value(self, value):
        assert 0 <= value <= self.max_value

        self.value = value


class RAM:
    def __init__(self, address_width: BitWidth, data_width: BitWidth):
        self.addressWidth = address_width
        self.dataWidth = data_width

        self.memory = dict()

    def read(self, address):
        assert 0 <= address <= self.addressWidth.max_value()

        return self.memory.get(address, 0)

    def write(self, address, value):
        assert 0 <= address <= self.addressWidth.max_value()
        assert 0 <= value <= self.dataWidth.max_value()

        self.memory[address] = value

    def __str__(self):
        output_str = ""
        for row in range(32):
            for col in range(8):
                output_str += hex(self.read(row*8 + col))[2:]+"\t"
            output_str += "\n"

        return output_str


class CPU:
    def __init__(self):
        self.reg_a = Register(BitWidth.EIGHT_BIT)
        self.reg_b = Register(BitWidth.EIGHT_BIT)

        self.mem_reg = Register(BitWidth.FOUR_BIT)

        self.instructions = RAM(BitWidth.EIGHT_BIT, BitWidth.EIGHT_BIT)
        self.memory = RAM(BitWidth.EIGHT_BIT, BitWidth.EIGHT_BIT)

        self.carry_on_op_reg = Register(BitWidth.ONE_BIT)

        # when halt reached,
        self.enable = True

        self.program_counter = 0

        # no instruction yet
        self.current_instruction = None

    def set_instructions(self, commands: list):
        # instructions are in hex form,
        commands = [int(c, 16) for c in commands]

        self.program_counter = 0
        self.mem_reg.set_value(0)
        self.reg_a.set_value(0)
        self.reg_b.set_value(0)

        for i in range(self.instructions.addressWidth.max_value()+1):
            self.instructions.write(i, commands[i] if i < len(commands) else 0)

    def is_enabled(self):
        return self.enable

    def fetch(self):
        self.current_instruction = self.instructions.read(self.program_counter)

    def decode(self):
        instr, param = list(hex(self.current_instruction)[2:].zfill(2))

        instruction = Instructions.find_instruction(instr)

        self.current_instruction = (instruction, int(param, 16))

    def execute(self):
        i, p = self.current_instruction

        #                               LS 4bits | RS 4 bits
        memory_address = self.mem_reg.value * 16 + p

        if i == Instructions.SET_MEM:
            self.mem_reg.set_value(p)
        elif i == Instructions.LOAD_A:
            self.reg_a.set_value(self.memory.read(memory_address))
        elif i == Instructions.LOAD_B:
            self.reg_b.set_value(self.memory.read(memory_address))
        elif i == Instructions.WRITE_A:
            self.memory.write(memory_address, self.reg_a.value)
        elif i == Instructions.WRITE_B:
            self.memory.write(memory_address, self.reg_b.value)
        elif i == Instructions.ADD_A_B:
            value = self.reg_a.value + self.reg_b.value

            max_value = self.memory.dataWidth.max_value()

            carry = 0
            while value > max_value:
                carry = 1
                value -= max_value

            self.memory.write(memory_address, value)
            self.carry_on_op_reg.set_value(carry)
        elif i == Instructions.SUB_A_B:
            value = self.reg_a.value - self.reg_b.value
            max_value = self.memory.dataWidth.max_value()

            carry = 0
            while value < max_value:
                carry = 1
                value += max_value

            self.memory.write(memory_address, value)
            self.carry_on_op_reg.set_value(carry)
        elif i == Instructions.SET_A:
            self.reg_a.set_value(p)
        elif i == Instructions.SET_B:
            self.reg_b.set_value(p)
        elif i == Instructions.NC_JUMP:
            self.program_counter = memory_address
            return  # dont add one later
        elif i == Instructions.C_JUMP:
            # jump if carry = 0
            if self.carry_on_op_reg.value == 0:
                memory_address = self.mem_reg.value * 16 + p
                self.program_counter = memory_address
                return
        elif i == Instructions.MUL_A_B:
            value = self.reg_a.value * self.reg_b.value
            max_value = self.memory.dataWidth.max_value()

            carry = 0
            while value > max_value:
                carry = 1
                value -= max_value

            self.memory.write(memory_address, value)
            self.carry_on_op_reg.set_value(carry)
        elif i == Instructions.DIV_A_B:
            value = self.reg_a.value // self.reg_b.value
            # never overflows in either, but just in case
            max_value = self.memory.dataWidth.max_value()

            while value > max_value:
                value -= max_value
            while value < max_value:
                value += max_value

            carry = 1 if self.reg_a.value % self.reg_b.value != 0 else 0

            self.memory.write(memory_address, value)
            self.carry_on_op_reg.set_value(carry)
        elif i == Instructions.MOD_IR:
            # Write Reg A to a IR at MA in Reg B
            self.instructions.write(self.reg_a.value, self.reg_b.value)
        elif i == Instructions.LS_REG:
            # Write A << 4 + B to cache
            a = self.reg_a.value
            b = self.reg_b.value

            a = (16*a) % 256 # leftshift 4 bits
            value = a+b

            self.memory.write(memory_address, value)
        elif i == Instructions.HALT:
            self.enable = False
            return

        self.program_counter += 1

    def __str__(self):
        output_str = ""

        output_str += "RegA:\t" + self.reg_a.__str__() + "\n"
        output_str += "RegB:\t" + self.reg_b.__str__() + "\n"
        output_str += "MReg:\t" + self.mem_reg.__str__() + "\n"
        output_str += "IR:\t\t" + self.mem_reg.__str__() + "\n"

        ram_lines = str(self.memory).split("\n")
        while True:
            if len(ram_lines) == 0:
                break

            line = ram_lines[-1]

            if set(line.split("\t")) == {'0', ''} or \
               set(line.split("\t")) == {'0'} or \
                            line == "\n" or \
                            line == "":
                ram_lines = ram_lines[:-1]
            else:
                break
        ram =  "\n\t\t".join(ram_lines)
        if ram.strip() == "":
            ram = "Empty"
        output_str += "RAM:\t" + ram

        return output_str


if __name__ == "__main__":
    testCommands = ["73", "84", "50", "ff"]

    cpu = CPU()

    cpu.set_instructions(testCommands)

    while cpu.is_enabled():
        cpu.fetch()
        cpu.decode()
        cpu.execute()

        print(cpu)
        time.sleep(0.5)


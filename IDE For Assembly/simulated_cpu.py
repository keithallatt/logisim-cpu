"""

SIMULATED_CPU.PY



A python script that emulates the behaviour of the 4 bit CPU designed in
Logisim. As versions of the CPU evolve, this script will need to reflect those
changes.

"""
from enum import Enum, unique
import math


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
    def __init__(self, addressWidth: BitWidth, dataWidth: BitWidth):
        self.addressWidth = addressWidth
        self.dataWidth = dataWidth

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


        pass

    def set_instructions(self, commands: list):
        # instructions are in hex form,
        commands = [int(c, 16) for c in commands]

        self.program_counter = 0
        self.mem_reg.set_value(0)
        self.reg_a.set_value(0)
        self.reg_b.set_value(0)

        for i in range(self.instructions.addressWidth.max_value()+1):
            self.instructions.write(i, commands[i] if i < len(commands) else 0)

        print(self.instructions)


    def read_status(self, register: Register):
        pass

    def __str__(self):
        output_str = ""

        output_str += "RegA:\t" + self.reg_a.__str__() + "\n"
        output_str += "RegB:\t" + self.reg_b.__str__() + "\n"
        output_str += "MReg:\t" + self.mem_reg.__str__() + "\n"
        output_str += "IR:\t" + self.mem_reg.__str__() + "\n"

        return output_str


if __name__ == "__main__":
    testCommands = ["73", "84", "50", "ff"]

    cpu = CPU()
    cpu.set_instructions(testCommands)

"""CPU functionality."""
# Day 1: review specs.
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        """Load a program into memory."""

        address = 0

        # For now, we've just hardcoded a program:

        program = [
            # From print8.ls8
            0b10000010, # LDI R0,8
            0b00000000,
            0b00001000,
            0b01000111, # PRN R0
            0b00000000,
            0b00000001, # HLT
        ]

        self.ram = [0] * len(program)

        for instruction in program:
            self.ram[address] = instruction
            address += 1
    
    def ram_read(self, i):
        return self.ram[i]


    def alu(self, op, reg_a=None, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "PRN":
            print(self.reg[reg_a])
        elif op == "LDI":
            self.reg[self.ram[reg_a]] = self.ram[reg_b]
        elif op == "HLT":
            pass
        else:
            raise Exception("Unsupported ALU operation")

    def trace(self):
        """
        Handy function to print out the CPU state. You might want to call this
        from run() if you need help debugging.
        """

        print(f"TRACE: %02X | %02X %02X %02X |" % (
            self.pc,
            #self.fl,
            #self.ie,
            self.ram_read(self.pc),
            self.ram_read(self.pc + 1),
            self.ram_read(self.pc + 2)
        ), end='')

        for i in range(8):
            print(" %02X" % self.reg[i], end='')

        print()

    def run(self):
        """Run the CPU."""
        running = True
        while running and self.pc < len(self.ram):
            this_instr = self.ram[self.pc]
            if this_instr == 0b00000001:
                self.alu("HLT")
                running = False
            if this_instr == 0b01000111:
                self.alu("PRN", self.ram[self.pc + 1])
                self.pc += 2
            if this_instr == 0b10000010:
                self.alu("LDI", self.pc + 1, self.pc + 2)
                self.pc += 3
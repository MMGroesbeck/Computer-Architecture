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

    def load(self, filename):
        program = []
        with open(filename, "r") as input:
            prog_lines = input.readlines()
        for line in prog_lines:
            split_line = line.split()
            if len(split_line) > 0 and line[0] != "#":
                program.append(split_line[0])
        address = 0
        self.ram = [0] * len(program)
        for instruction in program:
            self.ram[address] = int(instruction,2)
            address += 1

    def ram_read(self, i):
        return self.ram[i]
    
    def ram_write(self, i, v):
        self.ram[i] = j


    def alu(self, op, reg_a=None, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
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
        while running and (self.pc < len(self.ram)):
            this_instr = self.ram_read(self.pc)
            if this_instr == 0b00000001:
                running = False
            if this_instr == 0b01000111:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            if this_instr == 0b10000010:
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                self.pc += 3
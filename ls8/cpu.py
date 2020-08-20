"""CPU functionality."""
# Day 1: review specs.
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.pc = 0
        self.reg = [0] * 8
        self.stack = [0] * 256
        self.reg[7] = 256

    def load(self, filename):
        """Load a program into memory."""
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
            # self.ram[address] = int(instruction,2)
            self.ram_write(address, int(instruction,2))
            address += 1

    def ram_read(self, i):
        return self.ram[i]
    
    def ram_write(self, i, v):
        self.ram[i] = v
    
    def push(self):
        if self.reg[7] > 0:
            self.reg[7] -= 1
            self.stack[self.reg[7]] = self.reg[self.ram_read(self.pc + 1)]
            self.pc += 2
    
    def pop(self):
        if self.reg[7] < 256:
            # self.ram_write(self.ram_read(self.pc + 1), self.stack[self.reg[7]])
            self.reg[self.ram_read(self.pc + 1)] = self.stack[self.reg[7]]
            self.reg[7] += 1
            self.pc += 2

    def alu(self, op, reg_a=None, reg_b=None):
        """ALU operations."""

        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
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
            elif this_instr == 0b01000101:
                self.push()
            elif this_instr == 0b01000110:
                self.pop()
            elif this_instr == 0b01000111:
                print(self.reg[self.ram[self.pc + 1]])
                self.pc += 2
            elif this_instr == 0b10000010:
                self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
                self.pc += 3
            elif this_instr == 0b10100000:
                self.alu("ADD", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
            elif this_instr == 0b10100010:
                self.alu("MUL", self.ram[self.pc + 1], self.ram[self.pc + 2])
                self.pc += 3
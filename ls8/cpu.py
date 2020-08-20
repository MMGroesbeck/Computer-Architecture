"""CPU functionality."""
# Day 1: review specs.
import sys

class CPU:
    """Main CPU class."""

    def __init__(self):
        """Construct a new CPU."""
        self.ram = []
        self.running = False
        self.pc = 0
        self.reg = [0] * 8
        self.stack = [0] * 256
        self.reg[7] = 256
        self.commands = {
            0b00000001: self.halt,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01000111: self.prn,
            0b10000010: self.ldi,
            0b10100000: self.alu,
            0b10100010: self.alu
        }
        self.com_args = {
            0b10100000: "ADD",
            0b10100010: "MUL"
        }

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
            self.ram_write(address, int(instruction,2))
            address += 1
        self.pc = 0

    def ram_read(self, i):
        return self.ram[i]
    
    def ram_write(self, i, v):
        self.ram[i] = v
    
    def halt(self):
        self.running = False
    
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
    
    def prn(self):
        print(self.reg[self.ram[self.pc + 1]])
        self.pc += 2
    
    def ldi(self):
        self.reg[self.ram[self.pc+1]] = self.ram[self.pc+2]
        self.pc += 3

    def alu(self, op, reg_a=None, reg_b=None):
        """ALU operations."""
        if reg_a is None:
            reg_a = self.ram[self.pc + 1]
        if reg_b is None:
            reg_b = self.ram[self.pc + 2]
        if op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
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
        self.running = True
        while self.running and (self.pc < len(self.ram)):
            this_instr = self.ram_read(self.pc)
            if this_instr in self.com_args:
                self.commands[this_instr](self.com_args[this_instr])
            else:
                self.commands[this_instr]()
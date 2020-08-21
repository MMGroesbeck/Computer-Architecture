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
        self.interrupts = [0] * 8
        self.last_key = []
        self.flags = [0, 0, 0] #LGE
        self.commands = {
            0b00000000: self.nop,
            0b00000001: self.halt,
            0b00010001: self.ret,
            0b01000101: self.push,
            0b01000110: self.pop,
            0b01000111: self.prn,
            0b01001000: self.pra,
            0b01010000: self.call,
            0b01010100: self.jmp,
            0b01010101: self.jeq,
            0b01010110: self.jne,
            0b01010111: self.jgt,
            0b01011000: self.jlt,
            0b01011001: self.jle,
            0b01011010: self.jge,
            0b01101001: self.alu,
            0b10000010: self.ldi,
            0b10000100: self.st,
            0b10100000: self.alu,
            0b10100010: self.alu,
            0b10100100: self.alu,
            0b10100111: self.alu,
            0b10101000: self.alu,
            0b10101010: self.alu,
            0b10101011: self.alu,
            0b10101100: self.alu,
            0b10101101: self.alu
        }
        self.com_args = {
            0b01101001: ["NOT"],
            0b10100000: ["ADD"],
            0b10100010: ["MUL"],
            0b10100100: ["MOD"],
            0b10100111: ["CMP"],
            0b10101000: ["AND"],
            0b10101010: ["OR"],
            0b10101011: ["XOR"],
            0b10101100: ["SHL"],
            0b10101101: ["SHR"]
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
        self.ram = [0] * (len(program))
        address = 0
        for instruction in program:
            self.ram_write(address, int(instruction,2))
            address += 1
        self.pc = 0

    def ram_read(self, i):
        return self.ram[i]
    
    def ram_write(self, i, v):
        self.ram[i] = v
    
    def nop(self):
        self.pc += 1
    
    def halt(self):
        self.running = False
    
    def ret(self):
        if self.reg[7] >= 256:
            raise Exception("Cannot return; stack empty.")
        self.pc = self.stack[self.reg[7]]
        self.reg[7] += 1
    
    def push(self, v=None):
        if v is None:
            v = self.reg[self.ram_read(self.pc + 1)]
            self.pc += 2
        self.reg[7] -= 1
        self.stack[self.reg[7]] = v
    
    def pop(self, dest=None):
        if dest is None:
            dest = self.ram_read(self.pc + 1)
            self.pc += 2
        self.reg[dest] = self.stack[self.reg[7]]
        self.reg[7] += 1
    
    def prn(self):
        print(self.reg[self.ram_read(self.pc + 1)])
        self.pc += 2
    
    def pra(self):
        print(chr(self.reg[self.ram_read(self.pc + 1)]), end="")
        self.pc += 2
    
    def call(self):
        if self.reg[7] <= 0:
            raise Exception("Stack overflow.")
        self.push(self.pc + 2)
        self.pc = self.reg[self.ram_read(self.pc+1)]
    
    def jmp(self):
        self.pc = self.reg[self.ram_read(self.pc+1)]
    
    def jeq(self):
        if self.flags[2] == 1:
            self.jmp()
        else:
            self.pc += 2
    
    def jne(self):
        if self.flags[2] == 0:
            self.jmp()
        else:
            self.pc += 2
    
    def jgt(self):
        if self.flags[1] == 1:
            self.jmp()
        else:
            self.pc += 2
    
    def jlt(self):
        if self.flags[0] == 1:
            self.jmp()
        else:
            self.pc += 2
    
    def jle(self):
        if (self.flags[0] == 1) or (self.flags[2] == 1):
            self.jmp()
        else:
            self.pc += 2
    
    def jge(self):
        if (self.flags[1] == 1) or (self.flags[2] == 1):
            self.jmp()
        else:
            self.pc += 2
    
    def ldi(self):
        self.reg[self.ram_read(self.pc+1)] = self.ram_read(self.pc+2)
        self.pc += 3
    
    def st(self):
        self.reg[self.ram_read(self.pc+1)] = self.reg[self.ram_read(self.pc+2)]
        self.pc += 3

    def alu(self, op, reg_a=None, reg_b=None):
        """ALU operations."""
        if reg_a is None:
            reg_a = self.ram_read(self.pc + 1)
        if reg_b is None:
            reg_b = self.ram_read(self.pc + 2)
        a = self.reg[reg_a]
        b = self.reg[reg_b]
        if op == "NOT":
            self.reg[reg_a] = ~a
            self.pc += 2
        elif op == "ADD":
            self.reg[reg_a] += self.reg[reg_b]
            self.pc += 3
        elif op == "MUL":
            self.reg[reg_a] *= self.reg[reg_b]
            self.pc += 3
        elif op == "MOD":
            if b == 0:
                raise Exception("Divide-by-zero error in MOD.")
                self.halt()
            else:
                self.reg[reg_a] = a % b
                self.pc += 3
        elif op == "CMP":
            if a == b:
                self.flags = [0,0,1]
            elif a < b:
                self.flags = [1,0,0]
            elif a > b:
                self.flags = [0,1,0]
            self.pc += 3
        elif op == "AND":
            self.reg[reg_a] = a & b
            self.pc += 3
        elif op == "OR":
            self.reg[reg_a] = a | b
            self.pc += 3
        elif op == "XOR":
            self.reg[reg_a] = a ^ b
            self.pc += 3
        elif op == "SHL":
            self.reg[reg_a] = a << b
            self.pc += 3
        elif op == "SHR":
            self.reg[reg_a] = a >> b
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
                self.commands[this_instr](*self.com_args[this_instr])
            else:
                self.commands[this_instr]()
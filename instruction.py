import register
import sys
import types

def load_mask(num, bits, extend = False):
    negative_mask = 0xFFFFFFFF & (0xFFFFFFFF << bits)
    mask = ~negative_mask

    if extend and (mask & num.value) & (mask ^ (mask >> 1)):
        return types.Uint32(mask & num.value | negative_mask)

    return types.Uint32(types.Uint32(mask & num.value))

class Instruction():
    def __init__(self, reg):
        self.__registers = reg

    def add(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] + self.__registers[rs2]

    def sub(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] - self.__registers[rs2]

    def xor(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] ^ self.__registers[rs2]

    def or_(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] | self.__registers[rs2]

    def and_(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] & self.__registers[rs2]

    def sll(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] << self.__registers[rs2]

    def srl(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] >> self.__registers[rs2]

    def sra(rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1].arith_rshift(self.__registers[rs2])

    def slt(rd, rs1, rs2):
        self.__registers[rd] = 1 if self.__registers[rs1].toi32() < self.__registers[rs2].toi32() else 0

    def sltu(rd, rs1, rs2):
        self.__registers[rd] = 1 if self.__registers[rs1] < self.__registers[rs2] else 0


    def addi(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] + imm

    def xori(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] ^ imm

    def ori(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] | imm

    def andi(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] & imm

    def slli(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] << imm

    def srli(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] >> imm

    def srai(rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1].arith_rshift(imm)

    def slti(rd, rs1, imm):
        self.__registers[rd] = 1 if self.__registers[rs1].toi32() < imm else 0

    def sltiu(rd, rs1, imm):
        self.__registers[rd] = 1 if self.__registers[rs1] < imm else 0


    def lb(memory, rd, rs1, imm):
         self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 8, True)

    def lh(memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 16, True)

    def lw(memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 32, True)

    def lbu(memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 8)

    def lhu(memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 16)


    def sb(imm, rs2):
        memory[self.__registers[rs1] + imm] = load_mask(self.__registers[rs2], 8, True)

    def sh(imm, rs2):
        memory[self.__registers[rs1] + imm] = load_mask(self.__registers[rs2], 16, True)

    def sw(imm, rs2):
        memory[self.__registers[rs1] + imm] = load_mask(self.__registers[rs2], 32, True)


    def beq(rs1, rs2, imm):
        if self.__registers[rs1] == self.__registers[rs1]:
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def bne(rs1, rs2, imm):
        if self.__registers[rs1].toi32() != self.__registers[rs1].toi32():
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def blt(rs1, rs2, imm):
        if self.__registers[rs1].toi32() < self.__registers[rs1].toi32():
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def bge(rs1, rs2, imm):
        if self.__registers[rs1].toi32() >= self.__registers[rs1].toi32():
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def bltu(rs1, rs2, imm):
        if self.__registers[rs1] < self.__registers[rs1]:
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def bgeu(rs1, rs2, imm):
        if self.__registers[rs1] >= self.__registers[rs1]:
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def jal(rd, imm):
        self.__registers[rd] = self.__registers[register.PC] + 4
        self.__registers[register.PC] = self.__registers[register.PC] + imm

    def jal(rd, rs1, imm):
        self.__registers[rd] = self.__registers[register.PC] + 4
        self.__registers[register.PC] = self.__registers[rs1] + imm


    def lui(rd, imm):
        self.__registers[rd] = imm << 12

    def auipc(rd, imm):
        self.__registers[rd] = self.__registers[register.PC] + imm

    def ecall():
        sys.exit()

    def ebreak():
        raise Exception


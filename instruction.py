import register
import sys
import utypes

def load_mask(num, bits, extend = False):
    negative_mask = 0xFFFFFFFF & (0xFFFFFFFF << bits)
    mask = ~negative_mask

    if extend and (mask & num.value) & (mask ^ (mask >> 1)):
        return utypes.Uint32(mask & num.value | negative_mask)

    return utypes.Uint32(utypes.Uint32(mask & num.value))

class Instruction():
    def __init__(self, reg):
        self.__registers = reg

    def add(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] + self.__registers[rs2]

    def sub(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] - self.__registers[rs2]

    def xor(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] ^ self.__registers[rs2]

    def or_(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] | self.__registers[rs2]

    def and_(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] & self.__registers[rs2]

    def sll(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] << self.__registers[rs2]

    def srl(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1] >> self.__registers[rs2]

    def sra(self, rd, rs1, rs2):
        self.__registers[rd] = self.__registers[rs1].arith_rshift(self.__registers[rs2])

    def slt(self, rd, rs1, rs2):
        self.__registers[rd] = utypes.Uint32(1) if self.__registers[rs1].toi32() < self.__registers[rs2].toi32() else utypes.Uint32(0)

    def sltu(self, rd, rs1, rs2):
        self.__registers[rd] = utypes.Uint32(1) if self.__registers[rs1] < self.__registers[rs2] else utypes.Uint32(0)


    def addi(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] + imm

    def xori(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] ^ imm

    def ori(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] | imm

    def andi(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] & imm

    def slli(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] << imm

    def srli(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1] >> imm

    def srai(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[rs1].arith_rshift(imm)

    def slti(self, rd, rs1, imm):
        self.__registers[rd] = 1 if self.__registers[rs1].toi32() < imm else 0

    def sltiu(self, rd, rs1, imm):
        self.__registers[rd] = 1 if self.__registers[rs1] < imm else 0


    def lb(self, memory, rd, rs1, imm):
         self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 8, True)

    def lh(self, memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 16, True)

    def lw(self, memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 32, True)

    def lbu(self, memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 8)

    def lhu(self, memory, rd, rs1, imm):
        self.__registers[rd] = load_mask(memory[self.__registers[rs1] + imm], 16)


    def sb(self, memory, rs1, rs2, imm):
        memory[self.__registers[rs1] + imm] = load_mask(self.__registers[rs2], 8, True)

    def sh(self, memory, rs1, rs2, imm):
        memory[self.__registers[rs1] + imm] = load_mask(self.__registers[rs2], 16, True)

    def sw(self, memory, rs1, rs2, imm):
        memory[self.__registers[rs1] + imm] = load_mask(self.__registers[rs2], 32, True)


    def beq(self, rs1, rs2, imm):
        if self.__registers[rs1] == self.__registers[rs1]:
            self.__registers[register.PC] = utypes.Uint32(self.__registers[register.PC].toi32 + imm.toi32())

    def bne(self, rs1, rs2, imm):
        if self.__registers[rs1].toi32() != self.__registers[rs1].toi32():
            self.__registers[register.PC] = utypes.Uint32(self.__registers[register.PC].toi32 + imm.toi32())

    def blt(self, rs1, rs2, imm):
        if self.__registers[rs1].toi32() < self.__registers[rs1].toi32():
            self.__registers[register.PC] = utypes.Uint32(self.__registers[register.PC].toi32 + imm.toi32())

    def bge(self, rs1, rs2, imm):
        if self.__registers[rs1].toi32() >= self.__registers[rs1].toi32():
            self.__registers[register.PC] = utypes.Uint32(self.__registers[register.PC].toi32 + imm.toi32())

    def bltu(self, rs1, rs2, imm):
        if self.__registers[rs1] < self.__registers[rs1]:
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def bgeu(self, rs1, rs2, imm):
        if self.__registers[rs1] >= self.__registers[rs1]:
            self.__registers[register.PC] = self.__registers[register.PC] + imm

    def jal(self, rd, imm):
        self.__registers[rd] = self.__registers[register.PC] + 4
        self.__registers[register.PC] = self.__registers[register.PC] + imm

    def jalr(self, rd, rs1, imm):
        self.__registers[rd] = self.__registers[register.PC] + 4
        self.__registers[register.PC] = self.__registers[rs1] + imm


    def lui(self, rd, imm):
        self.__registers[rd] = imm

    def auipc(self, rd, imm):
        self.__registers[rd] = self.__registers[register.PC] + imm

    def ecall():
        sys.exit()

    def ebreak():
        raise Exception


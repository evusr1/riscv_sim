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
        self._registers = reg

    def add(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] + self._registers[rs2]

    def sub(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] - self._registers[rs2]

    def xor(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] ^ self._registers[rs2]

    def or_(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] | self._registers[rs2]

    def and_(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] & self._registers[rs2]

    def sll(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] << self._registers[rs2].value

    def srl(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] >> self._registers[rs2].value

    def sra(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1].arith_rshift(self._registers[rs2].value)

    def slt(self, rd, rs1, rs2):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1].toi32() < self._registers[rs2].toi32() else utypes.Uint32(0)

    def sltu(self, rd, rs1, rs2):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1] < self._registers[rs2] else utypes.Uint32(0)


    def addi(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] + imm

    def xori(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] ^ imm

    def ori(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] | imm

    def andi(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] & imm

    def slli(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] << imm.value

    def srli(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] >> imm.value

    def srai(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1].arith_rshift(imm.value)

    def slti(self, rd, rs1, imm):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1].toi32() < imm.toi32() else utypes.Uint32(0)

    def sltiu(self, rd, rs1, imm):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1] < imm else utypes.Uint32(0)


    def lb(self, memory, rd, rs1, imm):
        self._registers[rd] = load_mask(memory[(self._registers[rs1] + imm).value], 8, True)

    def lh(self, memory, rd, rs1, imm):
        self._registers[rd] = load_mask(memory[(self._registers[rs1] + imm).value], 16, True)

    def lw(self, memory, rd, rs1, imm):
        self._registers[rd] = load_mask(memory[(self._registers[rs1] + imm).value], 32, True)

    def lbu(self, memory, rd, rs1, imm):
        self._registers[rd] = load_mask(memory[(self._registers[rs1] + imm).value], 8)

    def lhu(self, memory, rd, rs1, imm):
        self._registers[rd] = load_mask(memory[(self._registers[rs1] + imm).value], 16)


    def sb(self, memory, rs1, rs2, imm):
        memory[self._registers[rs1].value + imm.value] |= load_mask(self._registers[rs2], 8)

    def sh(self, memory, rs1, rs2, imm):
        memory[self._registers[rs1].value + imm.value] |= load_mask(self._registers[rs2], 16)

    def sw(self, memory, rs1, rs2, imm):
        memory[self._registers[rs1].value + imm.value] |= load_mask(self._registers[rs2], 32)


    def beq(self, rs1, rs2, imm):
        if self._registers[rs1] == self._registers[rs2]:
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].toi32() + imm.toi32())

    def bne(self, rs1, rs2, imm):
        if self._registers[rs1].toi32() != self._registers[rs2].toi32():
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].toi32() + imm.toi32())

    def blt(self, rs1, rs2, imm):
        if self._registers[rs1].toi32() < self._registers[rs2].toi32():
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].toi32() + imm.toi32())

    def bge(self, rs1, rs2, imm):
        if self._registers[rs1].toi32() >= self._registers[rs2].toi32():
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].toi32() + imm.toi32())

    def bltu(self, rs1, rs2, imm):
        if self._registers[rs1] < self._registers[rs2]:
            self._registers[register.PC] = self._registers[register.PC] + imm

    def bgeu(self, rs1, rs2, imm):
        if self._registers[rs1] >= self._registers[rs2]:
            self._registers[register.PC] = self._registers[register.PC] + imm

    def jal(self, rd, imm):
        self._registers[rd] = self._registers[register.PC] + utypes.Uint32(4)
        self._registers[register.PC] = self._registers[register.PC] + imm

    def jalr(self, rd, rs1, imm):
        self._registers[rd] = self._registers[register.PC] + utypes.Uint32(4)
        self._registers[register.PC] = self._registers[rs1] + imm


    def lui(self, rd, imm):
        self._registers[rd] = imm

    def auipc(self, rd, imm):
        self._registers[rd] = self._registers[register.PC] + imm

    def ecall():
        sys.exit()

    def ebreak():
        raise Exception


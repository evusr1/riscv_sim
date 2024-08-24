import register
import sys
import utypes

class TransferException(Exception):
    pass

class ECALL(TransferException):
    pass

class EBREAK(TransferException):
    pass

def generate_negative_mask(bits):
    return 0xFFFFFFFF & (0xFFFFFFFF << bits)

def keep_number_bits(num, bits, extend = False):
    negative_mask = generate_negative_mask(bits)
    mask = ~negative_mask

    if extend and (mask & num.value) & (mask ^ (mask >> 1)):
        return utypes.Uint32(mask & num.value | negative_mask)

    return utypes.Uint32(utypes.Uint32(mask & num.value))

class Instruction():
    def __init__(self, reg):
        self._registers = reg

    def inc(self):
        self._registers[register.PC] = self._registers[register.PC] + utypes.Uint32(4)

    def add(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] + self._registers[rs2]

        self.inc()

    def sub(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] - self._registers[rs2]

        self.inc()

    def xor(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] ^ self._registers[rs2]

        self.inc()

    def or_(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] | self._registers[rs2]

        self.inc()

    def and_(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] & self._registers[rs2]

        self.inc()

    def sll(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] << keep_number_bits(self._registers[rs2], 5)

        self.inc()

    def srl(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1] >> keep_number_bits(self._registers[rs2], 5)

        self.inc()

    def sra(self, rd, rs1, rs2):
        self._registers[rd] = self._registers[rs1].arith_rshift(keep_number_bits(self._registers[rs2], 5))

        self.inc()

    def slt(self, rd, rs1, rs2):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1].toi32() < self._registers[rs2].toi32() else utypes.Uint32(0)

        self.inc()

    def sltu(self, rd, rs1, rs2):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1] < self._registers[rs2] else utypes.Uint32(0)

        self.inc()


    def addi(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] + imm

        self.inc()

    def xori(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] ^ imm

        self.inc()

    def ori(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] | imm

        self.inc()

    def andi(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] & imm

        self.inc()

    def slli(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] << imm.value

        self.inc()

    def srli(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1] >> imm.value

        self.inc()

    def srai(self, rd, rs1, imm):
        self._registers[rd] = self._registers[rs1].arith_rshift(imm.value)

        self.inc()

    def slti(self, rd, rs1, imm):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1].toi32() < imm.toi32() else utypes.Uint32(0)

        self.inc()

    def sltiu(self, rd, rs1, imm):
        self._registers[rd] = utypes.Uint32(1) if self._registers[rs1] < imm else utypes.Uint32(0)

        self.inc()


    def lb(self, memory, rd, rs1, imm):
        self._registers[rd] = keep_number_bits(memory[(self._registers[rs1] + imm).value], 8, True)

        self.inc()

    def lh(self, memory, rd, rs1, imm):
        self._registers[rd] = keep_number_bits(memory[(self._registers[rs1] + imm).value], 16, True)

        self.inc()

    def lw(self, memory, rd, rs1, imm):
        self._registers[rd] = keep_number_bits(memory[(self._registers[rs1] + imm).value], 32, True)

        self.inc()

    def lbu(self, memory, rd, rs1, imm):
        self._registers[rd] = keep_number_bits(memory[(self._registers[rs1] + imm).value], 8)

        self.inc()

    def lhu(self, memory, rd, rs1, imm):
        self._registers[rd] = keep_number_bits(memory[(self._registers[rs1] + imm).value], 16)

        self.inc()

    def sb(self, memory, rs1, rs2, imm):
        offset = self._registers[rs1].value + imm.toi32()
        memory[offset] = (memory[offset] & utypes.Uint32(generate_negative_mask(8))) | keep_number_bits(self._registers[rs2], 8)

        self.inc()

    def sh(self, memory, rs1, rs2, imm):
        offset = self._registers[rs1].value + imm.toi32()
        memory[offset] = (memory[offset] & utypes.Uint32(generate_negative_mask(16))) | keep_number_bits(self._registers[rs2], 16)

        self.inc()

    def sw(self, memory, rs1, rs2, imm):
        memory[self._registers[rs1].value + imm.toi32()] = keep_number_bits(self._registers[rs2], 32)

        self.inc()


    def beq(self, rs1, rs2, imm):
        if self._registers[rs1] == self._registers[rs2]:
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())
        else:
            self.inc()

    def bne(self, rs1, rs2, imm):
        if self._registers[rs1] != self._registers[rs2]:
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())
        else:
            self.inc()

    def blt(self, rs1, rs2, imm):
        if self._registers[rs1].toi32() < self._registers[rs2].toi32():
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())
        else:
            self.inc()

    def bge(self, rs1, rs2, imm):
        if self._registers[rs1].toi32() >= self._registers[rs2].toi32():
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())
        else:
            self.inc()

    def bltu(self, rs1, rs2, imm):
        if self._registers[rs1] < self._registers[rs2]:
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())
        else:
            self.inc()

    def bgeu(self, rs1, rs2, imm):
        if self._registers[rs1] >= self._registers[rs2]:
            self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())
        else:
            self.inc()

    def jal(self, rd, imm):
        self._registers[rd] = self._registers[register.PC] + utypes.Uint32(4)
        self._registers[register.PC] = utypes.Uint32(self._registers[register.PC].value + imm.toi32())

    def jalr(self, rd, rs1, imm):

        new_address = utypes.Uint32(self._registers[rs1].value + imm.toi32())
        self._registers[rd] = self._registers[register.PC] + utypes.Uint32(4)
        self._registers[register.PC] = new_address


    def lui(self, rd, imm):
        self._registers[rd] = imm

        self.inc()

    def auipc(self, rd, imm):
        self._registers[rd] = self._registers[register.PC] + imm

        self.inc()

    def ecall(self):
        raise ECALL

    def ebreak(self):
        raise EBREAK

    def nop(self):
        self.inc()

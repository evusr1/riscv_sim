from enum import Enum

class InstructionType(Enum):
    R = 1
    I = 2
    S = 3
    B = 4
    U = 5
    J = 6

class InstructionTypeOp(Enum):
    R = 0b0110011
    I = 0b0010011
    I2 = 0b0000011
    S = 0b0100011
    B = 0b1100011
    J = 0b1101111
    I3 = 0b1100111
    U = 0b0110111
    U2 = 0b0010111
    I4 = 0b1110011

def op(instruction):
    return instruction & 0b1111111

def get_type(instruction):
    opcode = op(instruction)

    match opcode:
        case InstructionTypeOp.R:
            return InstructionType.R
        case InstructionTypeOp.I | InstructionTypeOp.I2 | InstructionTypeOp.I3 | InstructionTypeOp.I4:
            return InstructionType.I
        case InstructionTypeOp.S:
            return InstructionType.S
        case InstructionTypeOp.B:
            return InstructionType.B
        case InstructionTypeOp.J:
            return InstructionType.J
        case InstructionTypeOp.U | InstructionTypeOp.U2:
            return InstructionType.U


def func3(instruction):
    return instruction & (0b111 << 11)

def func7(instruction):
    return instruction & (0b1111111 << 24)

def rd(instruction):
    return instruction & (0b11111 << 6)

def rs1(instruction):
    return instruction & (0b11111 << 14)

def rs2(instruction):
    return instruction & (0b11111 << 19)

def decode(instruction):
    i_type = get_type(instruction)

    match i_type:
        case InstructionType.R:
            pass
        case InstructionType.I:
            pass
        case InstructionType.S:
            pass
        case InstructionType.B:
            pass
        case InstructionType.J:
            pass
        case InstructionType.U:
            pass

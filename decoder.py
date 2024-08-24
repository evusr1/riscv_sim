from enum import Enum
import utypes

class InstructionType(Enum):
    NOP = 0
    R = 1
    I = 2
    I2 = 3
    S = 4
    B = 5
    J = 6
    I3 = 7
    U = 8
    U2 = 9
    I4 = 10

InstructionTypeOpsDict = dict(
        [(0b0110011, InstructionType.R),
        (0b0010011, InstructionType.I),
        (0b0000011, InstructionType.I2),
        (0b0100011, InstructionType.S),
        (0b1100011, InstructionType.B),
        (0b1101111, InstructionType.J),
        (0b1100111, InstructionType.I3),
        (0b0110111, InstructionType.U),
        (0b0010111, InstructionType.U2),
        (0b1110011, InstructionType.I4)]
    )

class Decoder():
    def op(self, instruction_in):
        return instruction_in & utypes.Uint32(0b1111111)

    def get_type(self, instruction_in):
        opcode = self.op(instruction_in)

        return InstructionTypeOpsDict[opcode.value]

    def imm_i_type1(self, instruction_in):
        imm = (instruction_in & utypes.Uint32(0b111111111111 << 20)) >> 20

        if (1 << 11) & imm.value:
            return imm | utypes.Uint32(0xFFFFFFFF & (0xFFFFFFFF << 12))

        return imm

    def imm_i_type2(self, instruction_in):
        return (instruction_in & utypes.Uint32(0b11111 << 20)) >> 20

    def imm_s(self, instruction_in):
        imm0_4 = (instruction_in & utypes.Uint32(0b11111 << 7)) >> 7
        imm5_11 = (instruction_in & utypes.Uint32(0b1111111 << 25)) >> 20

        combined_imm = imm0_4 | imm5_11

        if (1 << 11) & combined_imm.value:
             return combined_imm | utypes.Uint32(0xFFFFFFFF & (0xFFFFFFFF << 12))

        return combined_imm

    def imm_b(self, instruction_in):
        imm1_4 = (instruction_in & utypes.Uint32(0b1111 << 8)) >> 7
        imm11 = (instruction_in & utypes.Uint32(0b1 << 7)) << 4
        imm10_5 = (instruction_in & utypes.Uint32(0b111111 << 25)) >> 20
        imm12 = (instruction_in & utypes.Uint32(0b1 << 31)) >> 19

        combined_imm = imm1_4 | imm11 | imm10_5 | imm12

        if (1 << 12) & combined_imm.value:
             return combined_imm | utypes.Uint32(0xFFFFFFFF & (0xFFFFFFFF << 13))

        return combined_imm

    def imm_j(self, instruction_in):
        imm19_12 = (instruction_in & utypes.Uint32(0b11111111 << 12))
        imm11 = (instruction_in & utypes.Uint32(0b1 << 21)) >> 8
        imm1_10 =  (instruction_in & utypes.Uint32(0b11111111111 << 21)) >> 20
        imm20 = (instruction_in & utypes.Uint32(0b1 << 31)) >> 11
        return imm19_12 | imm11 | imm1_10 | imm20

    def imm_u(self, instruction_in):
        return instruction_in & utypes.Uint32(0b11111111111111111111 << 12)

    def rd(self, instruction_in):
        return (instruction_in.value & 0b11111 << 7) >> 7

    def rs1(self, instruction_in):
        return (instruction_in.value & 0b11111 << 15) >> 15

    def rs2(self, instruction_in):
        return (instruction_in.value & 0b11111 << 20) >> 20

    def get_func3(self, instruction_in):
        if self.get_type(instruction_in) in [InstructionType.J, InstructionType.U, InstructionType.U2]:
            return utypes.Uint32(0)
        return (instruction_in & utypes.Uint32(0b111 << 12)) >> 12

    def get_func7(self, instruction_in):
        instruction_type =  self.get_type(instruction_in)
        if instruction_type in [InstructionType.I, InstructionType.R, InstructionType.I4]:

            if instruction_type == InstructionType.I4:
                return self.imm_i_type1(instruction_in)

            if not instruction_type == InstructionType.I or self.get_func3(instruction_in).value in [0x1, 0x5]:
                return (instruction_in & utypes.Uint32(0b1111111 << 25)) >> 25

        return utypes.Uint32(0)

    def get_memorymap(self, instruction_in):
        return self._memorymap

    def __init__(self, instructions, memorymap):
            self._memorymap = memorymap
            self._instruction_table = [
                        None,
                        [   #R Type 1
                            [
                                [instructions.add, [self.rd, self.rs1, self.rs2]],
                                [instructions.sub, [self.rd, self.rs1, self.rs2]]
                            ], #0: 0, 0x20
                            [[instructions.sll, [self.rd, self.rs1, self.rs2]]], #1
                            [[instructions.slt, [self.rd, self.rs1, self.rs2]]], #2
                            [[instructions.sltu, [self.rd, self.rs1, self.rs2]]], #3
                            [[instructions.xor, [self.rd, self.rs1, self.rs2]]], #4
                            [
                                [instructions.srl, [self.rd, self.rs1, self.rs2]],
                                [instructions.sra, [self.rd, self.rs1, self.rs2]]
                            ], #5: 0, 0x20
                            [[instructions.or_, [self.rd, self.rs1, self.rs2]]], #6
                            [[instructions.and_, [self.rd, self.rs1, self.rs2]]] #7
                        ],
                        [   #I Type 2
                            [[instructions.addi, [self.rd, self.rs1, self.imm_i_type1]]], #0
                            [[instructions.slli, [self.rd, self.rs1, self.imm_i_type2]]], #1
                            [[instructions.slti, [self.rd, self.rs1, self.imm_i_type1]]], #2
                            [[instructions.sltiu, [self.rd, self.rs1, self.imm_i_type1]]], #3
                            [[instructions.xori, [self.rd, self.rs1, self.imm_i_type1]]], #4
                            [
                                [instructions.srli, [self.rd, self.rs1, self.imm_i_type2]],
                                [instructions.srai, [self.rd, self.rs1, self.imm_i_type2]]
                            ], #5: 0, 0x20
                            [[instructions.ori, [self.rd, self.rs1, self.imm_i_type1]]], #6
                            [[instructions.andi, [self.rd, self.rs1, self.imm_i_type1]]], #7
                        ],
                        [   #I2 Type 3
                            [[instructions.lb, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #0
                            [[instructions.lh, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #1
                            [[instructions.lw, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #2
                            None, #3
                            [[instructions.lbu, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #4
                            [[instructions.lhu, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #5
                        ],
                        [   #S Type 4
                            [[instructions.sb, [self.get_memorymap, self.rs1, self.rs2, self.imm_s]]], #0
                            [[instructions.sh, [self.get_memorymap, self.rs1, self.rs2, self.imm_s]]], #1
                            [[instructions.sw, [self.get_memorymap, self.rs1, self.rs2, self.imm_s]]], #2
                        ],
                        [   #B Type 5
                            [[instructions.beq, [self.rs1, self.rs2, self.imm_b]]], #0
                            [[instructions.bne, [self.rs1, self.rs2, self.imm_b]]], #1
                            None,
                            None,
                            [[instructions.blt, [self.rs1, self.rs2, self.imm_b]]], #4
                            [[instructions.bge, [self.rs1, self.rs2, self.imm_b]]], #5
                            [[instructions.bltu, [self.rs1, self.rs2, self.imm_b]]], #6
                            [[instructions.bgeu, [self.rs1, self.rs2, self.imm_b]]], #7
                        ],
                        [   #J Type 6
                            [[instructions.jal, [self.rd, self.imm_j]]], #0
                        ],
                        [   #I3 Type 7
                            [[instructions.jalr, [self.rd, self.rs1, self.imm_i_type1]]], #0
                        ] ,
                        [   #U Type 8
                            [[instructions.lui, [self.rd, self.imm_u]]]
                        ],
                        [   #U2 Type 9
                            [[instructions.auipc, [self.rd, self.imm_u]]]
                        ],
                        [   #I4 Type 10
                            [[instructions.ecall, []]], #0
                            [[instructions.ebreak, []]], #1
                        ]
            ]
            self.nop = instructions.nop


    def decode(self, instruction_in):
        try:
            func7 = 1 if self.get_func7(instruction_in).value else 0

            func3 = self.get_func3(instruction_in).value
            instruction_type = self.get_type(instruction_in).value

            args_list = self._instruction_table[instruction_type][func3][func7][1]
            args_list = map(lambda arg: arg(instruction_in), args_list)
            args_list = list(args_list)

            command = self._instruction_table[instruction_type][func3][func7][0]

            return [command, args_list]
        except:
            if instruction_in.value:
                print("Unimplemented", instruction_in)

            return [self.nop, []]

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
        return instruction_in[0:7]

    def get_type(self, instruction_in):
        opcode = self.op(instruction_in)

        return InstructionTypeOpsDict[opcode.value]

    def imm_i_type1(self, instruction_in):
        imm = instruction_in[20:32]
        print(imm)

        if (1 << 11) & imm.value:
            return imm | utypes.Uint32(0xFFFFFFFF & (0xFFFFFFFF << 12))

        return imm

    def imm_i_type2(self, instruction_in):
        return self.imm_i_type1(instruction_in)[0:5]

    def imm_s(self, instruction_in):
        imm0_4 = instruction_in[7:12]
        imm5_11 = instruction_in[25:32] << 5

        combined_imm = imm0_4 | imm5_11

        if combined_imm[11:12].value:
             return combined_imm | utypes.Uint32(0xFFFFFFFF & (0xFFFFFFFF << 12))

        return combined_imm

    def imm_b(self, instruction_in):
        imm1_4 = instruction_in[8:12] << 1
        imm11 = instruction_in[7:8] << 11
        imm10_5 = instruction_in[25:31] << 5
        imm12 = instruction_in[31:32] << 12

        combined_imm = imm1_4 | imm11 | imm10_5 | imm12

        if combined_imm[12:13].value:
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
        return instruction_in[7:12].value

    def rs1(self, instruction_in):
        return instruction_in[15:20].value

    def rs2(self, instruction_in):
        return instruction_in[20:25].value

    def get_func3(self, instruction_in):
        if self.get_type(instruction_in) in [InstructionType.J, InstructionType.U, InstructionType.U2]:
            return utypes.Uint32(0)
        return instruction_in[12:15]

    def get_func7(self, instruction_in):
        instruction_type =  self.get_type(instruction_in)
        if instruction_type in [InstructionType.I, InstructionType.R, InstructionType.I4]:

            if instruction_type == InstructionType.I4:
                return self.imm_i_type1(instruction_in)

            if not instruction_type == InstructionType.I or self.get_func3(instruction_in).value in [0x1, 0x5]:
                return self.imm_i_type1(instruction_in)[5:11]

        return utypes.Uint32(0)

    def get_memorymap(self, instruction_in):
        return self._memorymap

    def __init__(self, instructions, memorymap):
            self._memorymap = memorymap
            instruction_R_table =   [
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
                                    ]

            instruction_I_table =   [   #I Type 2
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
                                    ]

            instruction_I2_table =  [   #I2 Type 3
                                        [[instructions.lb, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #0
                                        [[instructions.lh, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #1
                                        [[instructions.lw, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #2
                                        None, #3
                                        [[instructions.lbu, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #4
                                        [[instructions.lhu, [self.get_memorymap, self.rd, self.rs1, self.imm_i_type1]]], #5
                                    ]

            instruction_S_table =   [   #S Type 4
                                        [[instructions.sb, [self.get_memorymap, self.rs1, self.rs2, self.imm_s]]], #0
                                        [[instructions.sh, [self.get_memorymap, self.rs1, self.rs2, self.imm_s]]], #1
                                        [[instructions.sw, [self.get_memorymap, self.rs1, self.rs2, self.imm_s]]], #2
                                    ]

            instruction_B_table =   [   #B Type 5
                                        [[instructions.beq, [self.rs1, self.rs2, self.imm_b]]], #0
                                        [[instructions.bne, [self.rs1, self.rs2, self.imm_b]]], #1
                                        None,
                                        None,
                                        [[instructions.blt, [self.rs1, self.rs2, self.imm_b]]], #4
                                        [[instructions.bge, [self.rs1, self.rs2, self.imm_b]]], #5
                                        [[instructions.bltu, [self.rs1, self.rs2, self.imm_b]]], #6
                                        [[instructions.bgeu, [self.rs1, self.rs2, self.imm_b]]], #7
                                    ]

            instruction_J_table =   [   #J Type 6
                                        [[instructions.jal, [self.rd, self.imm_j]]], #0
                                    ]

            instruction_I3_table =  [   #I3 Type 7
                                        [[instructions.jalr, [self.rd, self.rs1, self.imm_i_type1]]], #0
                                    ]

            instruction_U_table =   [   #U Type 8
                                        [[instructions.lui, [self.rd, self.imm_u]]]
                                    ]

            instruction_U2_table =  [   #U2 Type 9
                                        [[instructions.auipc, [self.rd, self.imm_u]]]
                                    ]

            instruction_I4_table =  [   #I4 Type 10
                                        [[instructions.ecall, []]], #0
                                        [[instructions.ebreak, []]], #1
                                    ]

            self._instruction_table = dict(
                        [(InstructionType.R, instruction_R_table),
                        (InstructionType.I, instruction_I_table),
                        (InstructionType.I2, instruction_I2_table),
                        (InstructionType.S, instruction_S_table),
                        (InstructionType.B, instruction_B_table),
                        (InstructionType.J, instruction_J_table),
                        (InstructionType.I3, instruction_I3_table),
                        (InstructionType.U, instruction_U_table),
                        (InstructionType.U2, instruction_U2_table),
                        (InstructionType.I4, instruction_I4_table)]
            )

            self.nop = instructions.nop


    def decode(self, instruction_in):
        try:
            func7 = 1 if self.get_func7(instruction_in).value else 0

            func3 = self.get_func3(instruction_in).value
            instruction_type = InstructionType(self.get_type(instruction_in).value)


            args_list = self._instruction_table[instruction_type][func3][func7][1]


            args_list = map(lambda arg: arg(instruction_in), args_list)
            args_list = list(args_list)

            command = self._instruction_table[instruction_type][func3][func7][0]

            return [command, args_list]
        except:
            if instruction_in.value:
                print("Unimplemented", instruction_in)

            return [self.nop, []]

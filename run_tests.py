def test(string, value,expected):
    print(string, ":", hex(value), "==", hex(expected))
    assert value == expected

import utypes

test("utypes.Uint32(-1).value", utypes.Uint32(-1).value, 0xFFFFFFFF)
test("utypes.Uint32(-1).toi32()", utypes.Uint32(-1).toi32(), -1)

test("utypes.Uint32(1).value", utypes.Uint32(1).value, 1)
test("utypes.Uint32(1).toi32()", utypes.Uint32(1).toi32(), 1)

test("utypes.Uint32(0) - utypes.Uint32(1)", (utypes.Uint32(0) - utypes.Uint32(1)).value, 0xFFFFFFFF)
test("utypes.Uint32(-1) - utypes.Uint32(-1)", (utypes.Uint32(-1) - utypes.Uint32(-2)).value, 1)
test("utypes.Uint32(-1) - utypes.Uint32(1)", (utypes.Uint32(-1) - utypes.Uint32(1)).value, 0xFFFFFFFE)

test("utypes.Uint32(1) + utypes.Uint32(1)", (utypes.Uint32(1) + utypes.Uint32(1)).value, 0x2)
test("utypes.Uint32(-1) + utypes.Uint32(-1)", (utypes.Uint32(-1) + utypes.Uint32(-1)).value, 0xFFFFFFFE)
test("utypes.Uint32(-1) + utypes.Uint32(1)", (utypes.Uint32(-1) + utypes.Uint32(1)).value, 0)

test("utypes.Uint32(0xFFFFFFFF).arith_rshift(1)", (utypes.Uint32(0xFFFFFFF7).arith_rshift(1)).value, 0xFFFFFFFB)
test("utypes.Uint32(0xFFFFFFFF) >> 1", (utypes.Uint32(0xFFFFFFF7) >> 1).value, 0x7FFFFFFB)
test("utypes.Uint32(0xFFFFFFFF) << 1", (utypes.Uint32(0xFFFFFFFF) << 1).value, 0xFFFFFFFE)
test("utypes.Uint32(0xDEAD0000) | utypes.Uint32(0xBEAF)", (utypes.Uint32(0xDEAD0000) | utypes.Uint32(0xBEAF)).value, 0xDEADBEAF)
test("utypes.Uint32(0xDEAD0000) & utypes.Uint32(0xBEAF)", (utypes.Uint32(0xDEAD0000) & utypes.Uint32(0xBEAF)).value, 0)
test("utypes.Uint32(0b1001) ^ utypes.Uint32(0b1101)", (utypes.Uint32(0b1001) ^ utypes.Uint32(0b1101)).value, 0b0100)
test("utypes.Uint32(1) > utypes.Uint32(0)", utypes.Uint32(1) > utypes.Uint32(0), True)
test("utypes.Uint32(1) >= utypes.Uint32(0)", utypes.Uint32(1) >= utypes.Uint32(0), True)

test("utypes.Uint32(1) < utypes.Uint32(0)", utypes.Uint32(1) < utypes.Uint32(0), False)
test("utypes.Uint32(1) <= utypes.Uint32(0)", utypes.Uint32(1) <= utypes.Uint32(0), False)

test("utypes.Uint32(1) == utypes.Uint32(0)", utypes.Uint32(1) == utypes.Uint32(0), False)
test("utypes.Uint32(1) != utypes.Uint32(0)", utypes.Uint32(1) != utypes.Uint32(0), True)

print("test ram")
import ram
print("Create Ram")
testram = ram.Ram(16)
print("Set Ram")
testram[1:4] = [1,2,3]
testram[4] = utypes.Uint32(0xDEADBEAF)

print("Validate Ram")
test("testram[0] == 0x03020100", testram[0].value, 0x03020100)
print(testram[0:9])
test("testram[0:9] == [0, 1, 2, 3, 0xAF, 0xBE, 0xAD, 0xDE, 0]", testram[0:9] == bytearray([0, 1, 2, 3, 0xAF, 0xBE, 0xAD, 0xDE, 0]), True)

print("test Memory map")
import memorymap
print("create Memory map")
testmap = memorymap.MemoryMap()
print("Add ram to devices")

testmap.add_device(testram, 0, 16)

testram2 = ram.Ram(32)
testmap.add_device(testram2, 32, 64)

print("test access banks")
test("testmap[4] == utypes.Uint32(0xDEADBEAF)", testmap[4] == utypes.Uint32(0xDEADBEAF), True)
test("testmap[0:9] == [0, 1, 2, 3, 0xAF, 0xBE, 0xAD, 0xDE, 0]", testmap[0:9] == bytearray([0, 1, 2, 3, 0xAF, 0xBE, 0xAD, 0xDE, 0]), True)
print("test different range, bank 2")
print("set")
testmap[32:36] = [0xDE, 0xAD, 0xBE, 0xAF]
test("testmap[32] == 0xAFBEADDE", testmap[32] == utypes.Uint32(0xAFBEADDE), True)
testmap[32] = utypes.Uint32(0xDEADBEAF)
test("testmap[32] == 0xDEADBEAF", testmap[32] == utypes.Uint32(0xDEADBEAF), True)

print("test instructions")



print("test reg")
import register

reg = register.Registers()

import instruction
test("keep_number_bits(utypes.Uint32(0xFFFFFFFF), 8) == 0xFF", instruction.keep_number_bits(utypes.Uint32(0xFFFFFFFF), 8).value, 0xFF)
test("keep_number_bits(utypes.Uint32(0xFFFFFFFF), 8, True) == 0xFFFFFFFF", instruction.keep_number_bits(utypes.Uint32(0xFFFFFFFF), 8, True).value, 0xFFFFFFFF)
test("keep_number_bits(utypes.Uint32(0xFFFFFFFF), 8, True) == 0xFFFFFF7F", instruction.keep_number_bits(utypes.Uint32(0xFFFFFF7F), 8, True).value, 0x7f)
instructions = instruction.Instruction(reg)


import decoder

decode = decoder.Decoder(instructions, testmap)


print("decode sll x6, x5, x7 (0x00729333)")
test("decode.get_type(utypes.Uint32(0x00729333)) ==  decoder.InstructionType.R", decode.get_type(utypes.Uint32(0x00729333)) == decoder.InstructionType.R, True)
test("decode.get_func3(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x1)", decode.get_func3(utypes.Uint32(0x00729333)) == utypes.Uint32(0x1), True)
test("decode.rd(utypes.Uint32(0x00729333)) ==  0x6", decode.rd(utypes.Uint32(0x00729333)) == 0x6, True)
test("decode.rs1(utypes.Uint32(0x00729333)) ==  0x5", decode.rs1(utypes.Uint32(0x00729333)) == 0x5, True)
test("decode.rs2(utypes.Uint32(0x00729333)) ==  0x7", decode.rs2(utypes.Uint32(0x00729333)) == 0x7, True)
test("decode.get_func7(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0x00729333)) == utypes.Uint32(0x0), True)

print("decode sra x6, x5, x7 (0x4072D333)")
test("decode.get_type(utypes.Uint32(0x4072D333)) ==  decoder.InstructionType.R", decode.get_type(utypes.Uint32(0x4072D333)) == decoder.InstructionType.R, True)
test("decode.get_func3(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x5)", decode.get_func3(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x5), True)
test("decode.rd(utypes.Uint32(0x4072D333)) ==  0x6", decode.rd(utypes.Uint32(0x4072D333)) == 0x6, True)
test("decode.rs1(utypes.Uint32(0x4072D333)) ==  0x5", decode.rs1(utypes.Uint32(0x4072D333)) == 0x5, True)
test("decode.rs2(utypes.Uint32(0x4072D333)) ==  0x7", decode.rs2(utypes.Uint32(0x4072D333)) == 0x7, True)
test("decode.get_func7(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x20)", decode.get_func7(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x20), True)

print("decode addi x6, x5, 20 (0x01428313)")
test("decode.get_type(utypes.Uint32(0x01428313)) ==  decoder.InstructionType.I", decode.get_type(utypes.Uint32(0x01428313)) == decoder.InstructionType.I, True)
test("decode.rd(utypes.Uint32(0x01428313)) ==  0x6", decode.rd(utypes.Uint32(0x01428313)) == 0x6, True)
test("decode.rs1(utypes.Uint32(0x01428313)) ==  0x5", decode.rs1(utypes.Uint32(0x01428313)) == 0x5, True)
test("decode.imm_i_type1(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x5)", decode.imm_i_type1(utypes.Uint32(0x01428313)) == utypes.Uint32(20), True)
test("decode.get_func3(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x0)", decode.get_func3(utypes.Uint32(0x01428313)) == utypes.Uint32(0x0), True)
test("decode.get_func7(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0x01428313)) == utypes.Uint32(0x0), True)

print("decode srai x6, x5, 20 (0x4142d313)")
test("decode.get_type(utypes.Uint32(0x4142d313)) ==  decoder.InstructionType.I", decode.get_type(utypes.Uint32(0x4142d313)) == decoder.InstructionType.I, True)
test("decode.rd(utypes.Uint32(0x4142d313)) ==  0x6", decode.rd(utypes.Uint32(0x4142d313)) == 0x6, True)
test("decode.rs1(utypes.Uint32(0x4142d313)) ==  0x5", decode.rs1(utypes.Uint32(0x4142d313)) == 0x5, True)
test("decode.imm_i_type2(utypes.Uint32(0x4142d313)) ==  utypes.Uint32(20)", decode.imm_i_type2(utypes.Uint32(0x4142d313)) == utypes.Uint32(20), True)
test("decode.get_func7(utypes.Uint32(0x4142d313)) ==  utypes.Uint32(0x20)", decode.get_func7(utypes.Uint32(0x4142d313)) == utypes.Uint32(0x20), True)

print("lw x6, 0x20(x5) (0x0202a303)")
test("decode.get_type(utypes.Uint32(0x0202a303)) ==  decoder.InstructionType.I2", decode.get_type(utypes.Uint32(0x0202a303)) == decoder.InstructionType.I2, True)
test("decode.rd(utypes.Uint32(0x0202a303)) ==  0x6", decode.rd(utypes.Uint32(0x0202a303)) == 0x6, True)
test("decode.rs1(utypes.Uint32(0x0202a303)) ==  0x5", decode.rs1(utypes.Uint32(0x0202a303)) == 0x5, True)
test("decode.imm_i_type1(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x20)", decode.imm_i_type1(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x20), True)
test("decode.get_func3(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x2)", decode.get_func3(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x2), True)
test("decode.get_func7(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x0), True)

print("sb x6, 0xaaa(x5) (0xaa628523)")
test("decode.get_type(utypes.Uint32(0xaa628523)) ==  decoder.InstructionType.S", decode.get_type(utypes.Uint32(0xaa628523)) == decoder.InstructionType.S, True)
test("decode.rs1(utypes.Uint32(0xaa628523)) ==  0x5", decode.rs1(utypes.Uint32(0xaa628523)) == 0x5, True)
test("decode.rs2(utypes.Uint32(0xaa628523)) ==  0x6", decode.rs2(utypes.Uint32(0xaa628523)) == 0x6, True)
test("decode.imm_s(utypes.Uint32(0xaa628523)).toi32() ==  -1366", decode.imm_s(utypes.Uint32(0xaa628523)).toi32(), -1366)
test("decode.get_func3(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0x0)", decode.get_func3(utypes.Uint32(0xaa628523)) == utypes.Uint32(0x0), True)
test("decode.get_func7(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0xaa628523)) == utypes.Uint32(0x0), True)

print("sb x6, 0xBEE(x5) (0xbe628723)")
test("decode.imm_s(utypes.Uint32(0xbe628723)).toi32() == -1042", decode.imm_s(utypes.Uint32(0xbe628723)).toi32(), -1042)

print("bgeu x6, x5, 0x1aaa (0xaa5375e3)")

test("decode.get_type(utypes.Uint32(0xaa5375e3)) ==  decoder.InstructionType.B", decode.get_type(utypes.Uint32(0xaa5375e3)) == decoder.InstructionType.B, True)
test("decode.rs1(utypes.Uint32(0xaa5375e3)) ==  0x5", decode.rs1(utypes.Uint32(0xaa5375e3)) == 0x6, True)
test("decode.rs2(utypes.Uint32(0xaa5375e3)) ==  0x6", decode.rs2(utypes.Uint32(0xaa5375e3)) == 0x5, True)
test("decode.imm_b(utypes.Uint32(0xaa5375e3)) == -1366", decode.imm_b(utypes.Uint32(0xaa5375e3)).toi32(), -1366)
test("decode.get_func3(utypes.Uint32(0xaa5375e3)) ==  0x7", decode.get_func3(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x7), True)
test("decode.get_func7(utypes.Uint32(0xaa5375e3)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x0), True)

print("bgeu x6, x5, 0xBEE (0x3e5377e3)")
test("decode.imm_b(utypes.Uint32(0x3e5377e3)) ==  3054", decode.imm_b(utypes.Uint32(0x3e5377e3)).toi32(), 3054)

print("jal x5, 0x1aaaaa (0xaabaa2ef)")
test("decode.get_type(utypes.Uint32(0xaabaa2ef)) ==  decoder.InstructionType.J", decode.get_type(utypes.Uint32(0xaabaa2ef)) == decoder.InstructionType.J, True)
test("decode.imm_j(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x1aaaaa)", decode.imm_j(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x1aaaaa), True)
test("decode.rd(utypes.Uint32(0xaabaa2ef)) ==  0x5", decode.rd(utypes.Uint32(0xaabaa2ef)) == 0x5, True)
test("decode.get_func3(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x0)", decode.get_func3(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x0), True)
test("decode.get_func7(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x0), True)

print("jal x5, 0x1BEEEE (0xeefbe2ef)")
test("decode.imm_j(utypes.Uint32(0xeefbe2ef)) ==  utypes.Uint32(0x1BEEEE)", decode.imm_j(utypes.Uint32(0xeefbe2ef)) == utypes.Uint32(0x1BEEEE), True)

print("jal x5, 0x1ABCDE (0xcdfab2ef)")
test("decode.imm_j(utypes.Uint32(0xcdfab2ef)) ==  utypes.Uint32(0x1ABCDE)", decode.imm_j(utypes.Uint32(0xcdfab2ef)) == utypes.Uint32(0x1ABCDE), True)

print("jalr x5, 0x20(x6)(0x020302e7)")
test("decode.get_type(utypes.Uint32(0x020302e7)) ==  decoder.InstructionType.I3", decode.get_type(utypes.Uint32(0x020302e7)) == decoder.InstructionType.I3, True)
test("decode.rd(utypes.Uint32(0x020302e7)) ==  0x5", decode.rd(utypes.Uint32(0x020302e7)) == 0x5, True)
test("decode.rs1(utypes.Uint32(0x020302e7)) ==  0x6", decode.rs1(utypes.Uint32(0x020302e7)) == 0x6, True)
test("decode.imm_i_type1(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0x20)", decode.imm_i_type1(utypes.Uint32(0x020302e7)) == utypes.Uint32(0x20), True)
test("decode.get_func3(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0)", decode.get_func3(utypes.Uint32(0x020302e7)) == utypes.Uint32(0), True)
test("decode.get_func7(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0)", decode.get_func7(utypes.Uint32(0x020302e7)) == utypes.Uint32(0), True)

print("ebreak (0x00100073)")
test("decode.get_type(utypes.Uint32(0x00100073)) ==  decoder.InstructionType.I4", decode.get_type(utypes.Uint32(0x00100073)) == decoder.InstructionType.I4, True)
test("decode.get_func3(utypes.Uint32(0x00100073)) ==  utypes.Uint32(0)", decode.get_func3(utypes.Uint32(0x00100073)) == utypes.Uint32(0), True)
test("decode.get_func7(utypes.Uint32(0x00100073)) ==  utypes.Uint32(0x1)", decode.get_func7(utypes.Uint32(0x00100073)) == utypes.Uint32(0x1), True)

print("auipc x5, 0xBEEEE (0xbeeee297)")
test("decode.get_type(utypes.Uint32(0xbeeee297)) ==  decoder.InstructionType.U2", decode.get_type(utypes.Uint32(0xbeeee297)) == decoder.InstructionType.U2, True)
test("decode.rd(utypes.Uint32(0xbeeee297)) ==  0x5", decode.rd(utypes.Uint32(0xbeeee297)) == 0x5, True)
test("decode.imm_u(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0xBEEEE)", decode.imm_u(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0xBEEEE) << 12, True)
test("decode.get_func3(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0)", decode.get_func3(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0), True)
test("decode.get_func7(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0)", decode.get_func7(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0), True)

import execute

cpu_execute = execute.Execute(decode)
print("addi x1, x1, 0x55 (0x05508093)")
cpu_execute.execute(utypes.Uint32(0x05508093))
test("reg[1] == utypes.Uint32(0x55)", reg[1] == utypes.Uint32(0x55), True)
print(reg)

print("addi x2, x1, 0x55")
cpu_execute.execute(utypes.Uint32(0x05508113))
test("reg[2] == utypes.Uint32(0x55 + 0x55)", reg[2] == utypes.Uint32(0x55 + 0x55), True)
print(reg)

print("sub x3, x2, x1 (0x401101b3)")
cpu_execute.execute(utypes.Uint32(0x401101b3))
test("reg[3] == utypes.Uint32(0x55)", reg[3] == utypes.Uint32(0x55), True)
print(reg)

print("xor x3, x2, x1 (0x001141b3)")
cpu_execute.execute(utypes.Uint32(0x001141b3))
test("reg[3] == utypes.Uint32(0x55 ^ (0x55 + 0x55))", reg[3] == utypes.Uint32(0x55 ^ (0x55 + 0x55)), True)
print(reg)

print("or x3, x2, x1 (0x001161b3)")
cpu_execute.execute(utypes.Uint32(0x001161b3))
test("reg[3] == utypes.Uint32(0x55 ^ (0x55 + 0x55))", reg[3] == utypes.Uint32(0x55 | (0x55 + 0x55)), True)
print(reg)

print("and x3, x2, x1 (0x001171b3)")
cpu_execute.execute(utypes.Uint32(0x001171b3))
test("reg[3] == utypes.Uint32(0x55 ^ (0x55 + 0x55))", reg[3] == utypes.Uint32(0x55 & (0x55 + 0x55)), True)
print(reg)

print("addi x4, x4, 0x1 (0x00120213)")
cpu_execute.execute(utypes.Uint32(0x00120213))
test("reg[4] == utypes.Uint32(1)", reg[4] == utypes.Uint32(1), True)
print(reg)

print("sll x3, x2, x4 (0x004111b3)")
cpu_execute.execute(utypes.Uint32(0x004111b3))
test("reg[3] == utypes.Uint32((0x55 + 0x55) << 1)", reg[3] == utypes.Uint32((0x55 + 0x55) << 1), True)
print(reg)

print("srl x3, x2, x4 (0x004151b3)")
cpu_execute.execute(utypes.Uint32(0x004151b3))
test("reg[3] == utypes.Uint32((0x55 + 0x55) >> 1)", reg[3] == utypes.Uint32((0x55 + 0x55) >> 1), True)
print(reg)

print("addi x4, x4, -1 (0xfff20213)")
cpu_execute.execute(utypes.Uint32(0xfff20213))
test("reg[4] == utypes.Uint32(0)", reg[4] == utypes.Uint32(0), True)
print(reg)

print("addi x4, x4, -1 (0xfff20213)")
cpu_execute.execute(utypes.Uint32(0xfff20213))
test("reg[4] == utypes.Uint32(-1)", reg[4] == utypes.Uint32(-1), True)
print(reg)

print("addi x5, x5, 1 (0x00128293)")
cpu_execute.execute(utypes.Uint32(0x00128293))
test("reg[5] == utypes.Uint32(1)", reg[5] == utypes.Uint32(1), True)
print(reg)

print("sra x3, x4, x5 (0x405251b3)")
cpu_execute.execute(utypes.Uint32(0x405251b3))
test("reg[3] == utypes.Uint32(-1)", reg[3] == utypes.Uint32(-1), True)
print(reg)

print("slt x3, x4, x1 (0x001221b3)")
cpu_execute.execute(utypes.Uint32(0x001221b3))
test("reg[3] == utypes.Uint32(1)", reg[3] == utypes.Uint32(1), True)
print(reg)


print("sltu x3, x4, x1 (0x001231b3)")
cpu_execute.execute(utypes.Uint32(0x001231b3))
test("reg[3] == utypes.Uint32(0)", reg[3] == utypes.Uint32(0), True)
print(reg)

print("xori x3, x1, 0x22 (0x0220c193)")
cpu_execute.execute(utypes.Uint32(0x0220c193))
test("reg[3] == utypes.Uint32(0x55 ^ 0x22)", reg[3] == utypes.Uint32(0x55 ^ 0x22), True)
print(reg)

print("ori x3, x1, 0x22 (0x0220e193)")
cpu_execute.execute(utypes.Uint32(0x0220e193))
test("reg[3] == utypes.Uint32(0x55 | 0x22)", reg[3] == utypes.Uint32(0x55 | 0x22), True)
print(reg)

print("andi x3, x1, 0x22 (0x0220f193)")
cpu_execute.execute(utypes.Uint32(0x0220f193))
test("reg[3] == utypes.Uint32(0x55 & 0x22)", reg[3] == utypes.Uint32(0x55 & 0x22), True)
print(reg)

print("slli x3, x1, 2 (0x00209193)")
cpu_execute.execute(utypes.Uint32(0x00209193))
test("reg[3] == utypes.Uint32(0x55 << 2)", reg[3] == utypes.Uint32(0x55 << 2), True)
print(reg)

print("srli x3, x1, 2 (0x0020d193)")
cpu_execute.execute(utypes.Uint32(0x0020d193))
test("reg[3] == utypes.Uint32(0x55 >> 2)", reg[3] == utypes.Uint32(0x55 >> 2), True)
print(reg)

print("srai x3, x4, 2 (0x40225193)")
cpu_execute.execute(utypes.Uint32(0x40225193))
test("reg[3] == utypes.Uint32(-1)", reg[3] == utypes.Uint32(-1), True)
print(reg)

print("slti x3, x1, -1 (0xfff0a193)")
cpu_execute.execute(utypes.Uint32(0xfff0a193))
test("reg[3] == utypes.Uint32(0)", reg[3] == utypes.Uint32(0), True)
print(reg)

print("sltiu x3, x1, -1 (0xfff0b193)")
cpu_execute.execute(utypes.Uint32(0xfff0b193))
test("reg[3] == utypes.Uint32(1)", reg[3] == utypes.Uint32(1), True)
print(reg)

testmap[4] = utypes.Uint32(0)

print("sb x4, 0x3(x3) (0x004181a3)")
cpu_execute.execute(utypes.Uint32(0x004181a3))
test("testmap[4] == utypes.Uint32(0xFF)", testmap[4] == utypes.Uint32(0xFF), True)
print(reg)


testmap[4] = utypes.Uint32(0)

print("sw x4, 3(x3) (0x0041a1a3)")
cpu_execute.execute(utypes.Uint32(0x0041a1a3))
test("testmap[4] == utypes.Uint32(0xFFFFFFFF)", testmap[4] == utypes.Uint32(0xFFFFFFFF), True)
print(reg)

testmap[4] = utypes.Uint32(0)

print("sh x4, 3(x3) (0x004191a3)")
cpu_execute.execute(utypes.Uint32(0x004191a3))
test("testmap[4] == utypes.Uint32(0xFFFF)", testmap[4] == utypes.Uint32(0xFFFF), True)
print(reg)

testmap[4] = utypes.Uint32(0xDEADBEAF)

print("andi x3, x3, 0 (0x0001f193)")
cpu_execute.execute(utypes.Uint32(0x0001f193))
test("reg[3] == utypes.Uint32(0)", reg[3] == utypes.Uint32(0), True)
print(reg)

print("lb x3, 3(x5) (0x00328183)")
cpu_execute.execute(utypes.Uint32(0x00328183))
test("reg[3] == utypes.Uint32(0xffffffaf)", reg[3] == utypes.Uint32(0xffffffaf), True)
print(reg)

print("lh x3, 3(x5) (0x00329183)")
cpu_execute.execute(utypes.Uint32(0x00329183))
test("reg[3] == utypes.Uint32(0xffffbeaf)", reg[3] == utypes.Uint32(0xffffbeaf), True)
print(reg)

print("lw x3, 3(x5) (0x0032a183)")
cpu_execute.execute(utypes.Uint32(0x0032a183))
test("reg[3] == utypes.Uint32(0)", reg[3] == utypes.Uint32(0xDEADBEAF), True)
print(reg)

print("lbu x3, 3(x5) (0x0032c183)")
cpu_execute.execute(utypes.Uint32(0x0032c183))
test("reg[3] == utypes.Uint32(0xaf)", reg[3] == utypes.Uint32(0xaf), True)
print(reg)

print("lhu x3, 3(x5) (0x0032d183)")
cpu_execute.execute(utypes.Uint32(0x0032d183))
test("reg[3] == utypes.Uint32(0xbeaf)", reg[3] == utypes.Uint32(0xbeaf), True)
print(reg)

reg[32] = utypes.Uint32(0)
print("beq x0 x6 0x10 (0x00600863)")
cpu_execute.execute(utypes.Uint32(0x00600863))
print(reg)

test("reg[32] == utypes.Uint32(0x10)", reg[32] == utypes.Uint32(0x10), True)

print("bne x0 x6 0x10 (0x00601863)")
cpu_execute.execute(utypes.Uint32(0x00601863))
test("reg[32] == utypes.Uint32(0x10)", reg[32] == utypes.Uint32(0x14), True)
print(reg)

reg[32] = utypes.Uint32(0x10)
print("blt x4 x1 0x10 (0x00124863)")
cpu_execute.execute(utypes.Uint32(0x00124863))
print(reg)
test("reg[32] == utypes.Uint32(0x20)", reg[32] == utypes.Uint32(0x20), True)

reg[32] = utypes.Uint32(0x20)
print("bge x4 x1 0x10 (0x00125863)")
cpu_execute.execute(utypes.Uint32(0x00125863))
test("reg[32] == utypes.Uint32(0x20)", reg[32] == utypes.Uint32(0x24), True)
print(reg)

reg[32] = utypes.Uint32(0x20)
print("bltu x4 x1 0x10 (0x00125863)")
cpu_execute.execute(utypes.Uint32(0x00126863))
test("reg[32] == utypes.Uint32(0x20)", reg[32] == utypes.Uint32(0x24), True)
print(reg)

reg[32] = utypes.Uint32(0x20)
print("bgeu x4 x1 0x10 (0x00127863)")
cpu_execute.execute(utypes.Uint32(0x00127863))
test("reg[32] == utypes.Uint32(0x30)", reg[32] == utypes.Uint32(0x30), True)
print(reg)

reg[32] = utypes.Uint32(0x30)
print("jal x3, 0x10 (0x010001ef)")
cpu_execute.execute(utypes.Uint32(0x010001ef))
test("reg[3] == utypes.Uint32(0x34)", reg[3] == utypes.Uint32(0x34), True)
test("reg[32] == utypes.Uint32(0x40)", reg[32] == utypes.Uint32(0x40), True)
print(reg)

reg[32] = utypes.Uint32(0x40)
print("jalr x3, 0x10(x3) (0x010181e7)")
cpu_execute.execute(utypes.Uint32(0x010181e7))
#test("reg[3] == utypes.Uint32(0x44)", reg[3] == utypes.Uint32(0x44), True)
#test("reg[32] == utypes.Uint32(0x54)", reg[32] == utypes.Uint32(0x54), True)
print(reg)

print("lui x3, 0x10 (0x000101b7)")
cpu_execute.execute(utypes.Uint32(0x000101b7))
print(reg)
test("reg[3] == utypes.Uint32((0x10 << 12)", reg[3] == utypes.Uint32((0x10 << 12)), True)

reg[32] = utypes.Uint32(0x54)
print("auipc x3, 0x10 (0x00010197)")
cpu_execute.execute(utypes.Uint32(0x00010197))
print(reg)
test("reg[3] == utypes.Uint32(0x54 + (0x10 << 12)", reg[3] == utypes.Uint32(0x54 + (0x10 << 12)), True)

reg[1] = utypes.Uint32(0);

print("addi x1, x1, 0xFFF (0xfff08093)")
cpu_execute.execute(utypes.Uint32(0xfff08093))
test("reg[1] == utypes.Uint32(-1)", reg[1].value , utypes.Uint32(-1).value)
print(reg)

try:
    print("ecall (0x00000073)")
    cpu_execute.execute(utypes.Uint32(0x00000073))
    assert("FAIL")
except instruction.ECALL:
    print("Success")

import os
RISCV_PATH = os.environ.get('RISCV', '/opt/riscv')
RISCV_TESTS_PATH = RISCV_PATH + "/target/share/riscv-tests/isa"

test("Checking if riscv-tests set up", os.path.isdir(RISCV_TESTS_PATH), True)
print("Listing tests...")

RISCV_TESTS = []

SKIP = ["rv32ui-p-fence_i"]

for f in os.listdir(RISCV_TESTS_PATH):
    if f in SKIP:
        continue
    if ".dump" in f:
        continue
    if "rv32ui-p" in f:
        print("Adding ", f)
        RISCV_TESTS.append(f)

import elfloader
import rv32i

ram_size = 1 * 1024 * 1024
reset_vector = 0x80000000
memmap = memorymap.MemoryMap()

print("Allocating ram", ram_size)
main_ram = ram.Ram(ram_size)
memmap.add_device(main_ram, reset_vector, reset_vector + ram_size)

print("Create rv32i")
cpu = rv32i.RV32I(memmap, reset_vector)


cpu_loader = elfloader.Loader(memmap)
print("Test load", RISCV_TESTS_PATH + "/rv32ui-p-addi")
cpu_loader.from_file(RISCV_TESTS_PATH + "/rv32ui-p-addi")


print(cpu.registers)
print("Test CPU run")
cpu.run()

print("PC", cpu.registers[register.PC])
print("A7", cpu.registers[register.A7])
print("A0", cpu.registers[register.A0])

test_number = 1

for test_file in RISCV_TESTS:
    cpu.reset()
    RISCV_TEST_PATH = RISCV_TESTS_PATH + "/" + test_file

    print("Test load", RISCV_TEST_PATH)
    cpu_loader.from_file(RISCV_TEST_PATH)

    cpu.run()
    print("PC", cpu.registers[register.PC])
    print("A7", cpu.registers[register.A7])
    print("A0", cpu.registers[register.A0])

    print(test_number, "/", len(RISCV_TESTS))
    test_number += 1
    test(RISCV_TEST_PATH + ", cpu.registers[register.A0] == 0", cpu.registers[register.A0].value, 0)

print("Congrats!")

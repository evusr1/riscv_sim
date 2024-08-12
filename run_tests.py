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
test("load_mask(utypes.Uint32(0xFFFFFFFF), 8) == 0xFF", instruction.load_mask(utypes.Uint32(0xFFFFFFFF), 8).value, 0xFF)
test("load_mask(utypes.Uint32(0xFFFFFFFF), 8, True) == 0xFFFFFFFF", instruction.load_mask(utypes.Uint32(0xFFFFFFFF), 8, True).value, 0xFFFFFFFF)
test("load_mask(utypes.Uint32(0xFFFFFFFF), 8, True) == 0xFFFFFF7F", instruction.load_mask(utypes.Uint32(0xFFFFFF7F), 8, True).value, 0x7f)
instructions = instruction.Instruction(reg)


import decoder

decode = decoder.Decoder(instructions, testmap)

print("decode sll x6, x5, x7 (0x00729333)")
test("decode.get_type(utypes.Uint32(0x00729333)) ==  decoder.InstructionType.R", decode.get_type(utypes.Uint32(0x00729333)) == decoder.InstructionType.R, True)
test("decode.get_func3(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x1)", decode.get_func3(utypes.Uint32(0x00729333)) == utypes.Uint32(0x1), True)
test("decode.rd(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x6)", decode.rd(utypes.Uint32(0x00729333)) == utypes.Uint32(0x6), True)
test("decode.rs1(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0x00729333)) == utypes.Uint32(0x5), True)
test("decode.rs2(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x7)", decode.rs2(utypes.Uint32(0x00729333)) == utypes.Uint32(0x7), True)
test("decode.get_func7(utypes.Uint32(0x00729333)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0x00729333)) == utypes.Uint32(0x0), True)

print("decode sra x6, x5, x7 (0x4072D333)")
test("decode.get_type(utypes.Uint32(0x4072D333)) ==  decoder.InstructionType.R", decode.get_type(utypes.Uint32(0x4072D333)) == decoder.InstructionType.R, True)
test("decode.get_func3(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x5)", decode.get_func3(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x5), True)
test("decode.rd(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x6)", decode.rd(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x6), True)
test("decode.rs1(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x5), True)
test("decode.rs2(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x7)", decode.rs2(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x7), True)
test("decode.get_func7(utypes.Uint32(0x4072D333)) ==  utypes.Uint32(0x20)", decode.get_func7(utypes.Uint32(0x4072D333)) == utypes.Uint32(0x20), True)

print("decode addi x6, x5, 20 (0x01428313)")
test("decode.get_type(utypes.Uint32(0x01428313)) ==  decoder.InstructionType.I", decode.get_type(utypes.Uint32(0x01428313)) == decoder.InstructionType.I, True)
test("decode.rd(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x6)", decode.rd(utypes.Uint32(0x01428313)) == utypes.Uint32(0x6), True)
test("decode.rs1(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0x01428313)) == utypes.Uint32(0x5), True)
test("decode.imm_i_type1(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x5)", decode.imm_i_type1(utypes.Uint32(0x01428313)) == utypes.Uint32(20), True)
test("decode.get_func3(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x0)", decode.get_func3(utypes.Uint32(0x01428313)) == utypes.Uint32(0x0), True)
test("decode.get_func7(utypes.Uint32(0x01428313)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0x01428313)) == utypes.Uint32(0x0), True)

print("decode srai x6, x5, 20 (0x4142d313)")
test("decode.get_type(utypes.Uint32(0x4142d313)) ==  decoder.InstructionType.I", decode.get_type(utypes.Uint32(0x4142d313)) == decoder.InstructionType.I, True)
test("decode.rd(utypes.Uint32(0x4142d313)) ==  utypes.Uint32(0x6)", decode.rd(utypes.Uint32(0x4142d313)) == utypes.Uint32(0x6), True)
test("decode.rs1(utypes.Uint32(0x4142d313)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0x4142d313)) == utypes.Uint32(0x5), True)
test("decode.imm_i_type2(utypes.Uint32(0x4142d313)) ==  utypes.Uint32(20)", decode.imm_i_type2(utypes.Uint32(0x4142d313)) == utypes.Uint32(20), True)
test("decode.get_func7(utypes.Uint32(0x4142d313)) ==  utypes.Uint32(0x20)", decode.get_func7(utypes.Uint32(0x4142d313)) == utypes.Uint32(0x20), True)

print("lw x6, 0x20(x5) (0x0202a303)")
test("decode.get_type(utypes.Uint32(0x0202a303)) ==  decoder.InstructionType.I2", decode.get_type(utypes.Uint32(0x0202a303)) == decoder.InstructionType.I2, True)
test("decode.rd(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x6)", decode.rd(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x6), True)
test("decode.rs1(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x5), True)
test("decode.imm_i_type1(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x20)", decode.imm_i_type1(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x20), True)
test("decode.get_func3(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x2)", decode.get_func3(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x2), True)
test("decode.get_func7(utypes.Uint32(0x0202a303)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0x0202a303)) == utypes.Uint32(0x0), True)

print("sb x6, 0xaaa(x5) (0xaa628523)")
test("decode.get_type(utypes.Uint32(0xaa628523)) ==  decoder.InstructionType.S", decode.get_type(utypes.Uint32(0xaa628523)) == decoder.InstructionType.S, True)
test("decode.rs1(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0xaa628523)) == utypes.Uint32(0x5), True)
test("decode.rs2(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0x6)", decode.rs2(utypes.Uint32(0xaa628523)) == utypes.Uint32(0x6), True)
test("decode.imm_s(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0xaaa)", decode.imm_s(utypes.Uint32(0xaa628523)) == utypes.Uint32(0xaaa), True)
test("decode.get_func3(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0x0)", decode.get_func3(utypes.Uint32(0xaa628523)) == utypes.Uint32(0x0), True)
test("decode.get_func7(utypes.Uint32(0xaa628523)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0xaa628523)) == utypes.Uint32(0x0), True)

print("sb x6, 0xBEE(x5) (0xbe628723)")
test("decode.imm_s(utypes.Uint32(0xbe628723)) ==  utypes.Uint32(0xBEE)", decode.imm_s(utypes.Uint32(0xbe628723)) == utypes.Uint32(0xBEE), True)

print("bgeu x6, x5, 0x1aaa (0xaa5375e3)")

test("decode.get_type(utypes.Uint32(0xaa5375e3)) ==  decoder.InstructionType.B", decode.get_type(utypes.Uint32(0xaa5375e3)) == decoder.InstructionType.B, True)
test("decode.rs1(utypes.Uint32(0xaa5375e3)) ==  utypes.Uint32(0x5)", decode.rs1(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x6), True)
test("decode.rs2(utypes.Uint32(0xaa5375e3)) ==  utypes.Uint32(0x6)", decode.rs2(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x5), True)
test("decode.imm_b(utypes.Uint32(0xaa5375e3)) ==  utypes.Uint32(0x1aaa)", decode.imm_b(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x1aaa), True)
test("decode.get_func3(utypes.Uint32(0xaa5375e3)) ==  utypes.Uint32(0x7)", decode.get_func3(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x7), True)
test("decode.get_func7(utypes.Uint32(0xaa5375e3)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0xaa5375e3)) == utypes.Uint32(0x0), True)

print("bgeu x6, x5, 0xBEE (0x3e5377e3)")
test("decode.imm_b(utypes.Uint32(0x3e5377e3)) ==  utypes.Uint32(0xBEE)", decode.imm_b(utypes.Uint32(0x3e5377e3)) == utypes.Uint32(0xBEE), True)

print("jal x5, 0x1aaaaa (0xaabaa2ef)")
test("decode.get_type(utypes.Uint32(0xaabaa2ef)) ==  decoder.InstructionType.J", decode.get_type(utypes.Uint32(0xaabaa2ef)) == decoder.InstructionType.J, True)
test("decode.imm_j(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x1aaaaa)", decode.imm_j(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x1aaaaa), True)
test("decode.rd(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x5)", decode.rd(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x5), True)
test("decode.get_func3(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x0)", decode.get_func3(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x0), True)
test("decode.get_func7(utypes.Uint32(0xaabaa2ef)) ==  utypes.Uint32(0x0)", decode.get_func7(utypes.Uint32(0xaabaa2ef)) == utypes.Uint32(0x0), True)

print("jal x5, 0x1BEEEE (0xeefbe2ef)")
test("decode.imm_j(utypes.Uint32(0xeefbe2ef)) ==  utypes.Uint32(0x1BEEEE)", decode.imm_j(utypes.Uint32(0xeefbe2ef)) == utypes.Uint32(0x1BEEEE), True)

print("jal x5, 0x1ABCDE (0xcdfab2ef)")
test("decode.imm_j(utypes.Uint32(0xcdfab2ef)) ==  utypes.Uint32(0x1ABCDE)", decode.imm_j(utypes.Uint32(0xcdfab2ef)) == utypes.Uint32(0x1ABCDE), True)

print("jalr x5, 0x20(x6)(0x020302e7)")
test("decode.get_type(utypes.Uint32(0x020302e7)) ==  decoder.InstructionType.I3", decode.get_type(utypes.Uint32(0x020302e7)) == decoder.InstructionType.I3, True)
test("decode.rd(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0x5)", decode.rd(utypes.Uint32(0x020302e7)) == utypes.Uint32(0x5), True)
test("decode.rs1(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0x6)", decode.rs1(utypes.Uint32(0x020302e7)) == utypes.Uint32(0x6), True)
test("decode.imm_i_type1(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0x20)", decode.imm_i_type1(utypes.Uint32(0x020302e7)) == utypes.Uint32(0x20), True)
test("decode.get_func3(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0)", decode.get_func3(utypes.Uint32(0x020302e7)) == utypes.Uint32(0), True)
test("decode.get_func7(utypes.Uint32(0x020302e7)) ==  utypes.Uint32(0)", decode.get_func7(utypes.Uint32(0x020302e7)) == utypes.Uint32(0), True)

print("ebreak (0x00100073)")
test("decode.get_type(utypes.Uint32(0x00100073)) ==  decoder.InstructionType.I4", decode.get_type(utypes.Uint32(0x00100073)) == decoder.InstructionType.I4, True)
test("decode.get_func3(utypes.Uint32(0x00100073)) ==  utypes.Uint32(0)", decode.get_func3(utypes.Uint32(0x00100073)) == utypes.Uint32(0), True)
test("decode.get_func7(utypes.Uint32(0x00100073)) ==  utypes.Uint32(0x1)", decode.get_func7(utypes.Uint32(0x00100073)) == utypes.Uint32(0x1), True)

print("auipc x5, 0xBEEEE (0xbeeee297)")
test("decode.get_type(utypes.Uint32(0xbeeee297)) ==  decoder.InstructionType.U2", decode.get_type(utypes.Uint32(0xbeeee297)) == decoder.InstructionType.U2, True)
test("decode.rd(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0x5)", decode.rd(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0x5), True)
test("decode.imm_u(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0xBEEEE)", decode.imm_u(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0xBEEEE) << 12, True)
test("decode.get_func3(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0)", decode.get_func3(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0), True)
test("decode.get_func7(utypes.Uint32(0xbeeee297)) ==  utypes.Uint32(0)", decode.get_func7(utypes.Uint32(0xbeeee297)) == utypes.Uint32(0), True)

def test(string, value,expected):
    print(string, ":", hex(value), "==", hex(expected))
    assert value == expected

import types

test("types.Uint32(-1).value", types.Uint32(-1).value, 0xFFFFFFFF)
test("types.Uint32(-1).toi32()", types.Uint32(-1).toi32(), -1)

test("types.Uint32(1).value", types.Uint32(1).value, 1)
test("types.Uint32(1).toi32()", types.Uint32(1).toi32(), 1)

test("types.Uint32(0) - types.Uint32(1)", (types.Uint32(0) - types.Uint32(1)).value, 0xFFFFFFFF)
test("types.Uint32(-1) - types.Uint32(-1)", (types.Uint32(-1) - types.Uint32(-2)).value, 1)
test("types.Uint32(-1) - types.Uint32(1)", (types.Uint32(-1) - types.Uint32(1)).value, 0xFFFFFFFE)

test("types.Uint32(1) + types.Uint32(1)", (types.Uint32(1) + types.Uint32(1)).value, 0x2)
test("types.Uint32(-1) + types.Uint32(-1)", (types.Uint32(-1) + types.Uint32(-1)).value, 0xFFFFFFFE)
test("types.Uint32(-1) + types.Uint32(1)", (types.Uint32(-1) + types.Uint32(1)).value, 0)

test("types.Uint32(0xFFFFFFFF).arith_rshift(1)", (types.Uint32(0xFFFFFFF7).arith_rshift(1)).value, 0xFFFFFFFB)
test("types.Uint32(0xFFFFFFFF) >> 1", (types.Uint32(0xFFFFFFF7) >> 1).value, 0x7FFFFFFB)
test("types.Uint32(0xFFFFFFFF) << 1", (types.Uint32(0xFFFFFFFF) << 1).value, 0xFFFFFFFE)
test("types.Uint32(0xDEAD0000) | types.Uint32(0xBEAF)", (types.Uint32(0xDEAD0000) | types.Uint32(0xBEAF)).value, 0xDEADBEAF)
test("types.Uint32(0xDEAD0000) & types.Uint32(0xBEAF)", (types.Uint32(0xDEAD0000) & types.Uint32(0xBEAF)).value, 0)
test("types.Uint32(0b1001) ^ types.Uint32(0b1101)", (types.Uint32(0b1001) ^ types.Uint32(0b1101)).value, 0b0100)
test("types.Uint32(1) > types.Uint32(0)", types.Uint32(1) > types.Uint32(0), True)
test("types.Uint32(1) >= types.Uint32(0)", types.Uint32(1) >= types.Uint32(0), True)

test("types.Uint32(1) < types.Uint32(0)", types.Uint32(1) < types.Uint32(0), False)
test("types.Uint32(1) <= types.Uint32(0)", types.Uint32(1) <= types.Uint32(0), False)

test("types.Uint32(1) == types.Uint32(0)", types.Uint32(1) == types.Uint32(0), False)
test("types.Uint32(1) != types.Uint32(0)", types.Uint32(1) != types.Uint32(0), True)

import ram
print("Create Ram")
testram = ram.Ram(16)
print("Set Ram")
testram[1:4] = [1,2,3]
testram[4] = types.Uint32(0xDEADBEAF)

print("Validate Ram")
test("testram[0] == 0x03020100", testram[0].value, 0x03020100)
print(testram[0:9])
test("testram[0:9] == [0, 1, 2, 3, 0, 0, 0, 0, 0]", testram[0:9] == bytearray([0, 1, 2, 3, 0xAF, 0xBE, 0xAD, 0xDE, 0]), True)

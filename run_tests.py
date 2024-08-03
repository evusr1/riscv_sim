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

test("types.Uint32(0xFFFFFFFF).arith_rshift(1)", (types.Uint32(0xFFFFFFFF).arith_rshift(1)).value, 0xFFFFFFFF)
test("types.Uint32(0xFFFFFFFF) >> 1", (types.Uint32(0xFFFFFFFF) >> 1).value, 0x7FFFFFFF)
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


def sign(num):
    return num & ~0x7FFFFFFF

def tou32(num):
    if num > 0:
        return 0xFFFFFFFF & num

    return 0xFFFFFFFF & (~abs(num) + 1)

class Uint32():

    def __init__(self, value):
            if  type(value) is Uint32:
                self.value = value.value
                return

            if value > 0 and value <= 0xFFFFFFFF:
                self.value = value
            else:
                self.value = tou32(value)

    def __add__(self, num):
        ret = (num.value + self.value) & 0xFFFFFFFF

        if ret < 0:
            return Uint32(tou32(ret))

        return Uint32(ret)

    def __sub__(self, num):
        ret = (self.value - num.value) & 0xFFFFFFFF

        if ret < 0:
            return Uint32(tou32(ret))

        return Uint32(ret)

    def __rshift__(self, shift):
        if type(shift) is Uint32:
            shift = shift.value

        return Uint32(self.value >> shift)

    def __lshift__(self, shift):
        if type(shift) is Uint32:
            shift = shift.value

        return Uint32((self.value << shift) & 0xFFFFFFFF)

    def __and__(self, num):
        return Uint32(self.value & num.value)

    def __or__(self, num):
        return Uint32(self.value | num.value)

    def __xor__(self, num):
        return Uint32(self.value ^ num.value)

    def __lt__(self, num):
        return self.value < num.value

    def __gt__(self, num):
        return self.value > num.value

    def __le__(self, num):
        return self.value <= num.value

    def __ge__(self, num):
        return self.value >= num.value

    def __eq__(self, num):
        return self.value == num.value

    def __ne__(self, num):
        return self.value != num.value

    def __str__(self):
        return hex(self.value)

    def toi32(self):
        if not sign(self.value):
            return 0x7FFFFFFF & self.value

        return -(0xFFFFFFFF & (~self.value + 1))

    def arith_rshift(self, shift):
        if type(shift) is Uint32:
            shift = shift.value

        if not sign(self.value):
            return Uint32(self.value >> shift)

        mask = 0xFFFFFFFF << 32 - shift

        return Uint32((0xFFFFFFFF & mask) | (self.value >> shift))

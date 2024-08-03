ZERO = 0
RA = 1
SP = 2
GP = 3
TP = 4
T0 = 5
T1 = 6
T2 = 7
S0 = 8
FP = 8
S1 = 9
A0 = 10
A1 = 11
A2 = 12
A3 = 13
A4 = 14
A5 = 15
A6 = 16
A7 = 17
S2 = 18
S3 = 19
S4 = 20
S5 = 21
S6 = 22
S7 = 23
S8 = 24
S9 = 25
S10 = 26
S11 = 27
T3 = 28
T4 = 29
T5 = 30
T6 = 31

PC = 32

import types

class Registers():
    def __init__(self):
        self.registers = [types.uint32(0) for i in range(0,33)]
    def __setitem__(self, key, value):
        self.registers[key] = value
    def __getitem__(self, key):
        return self.registers[key]
    def __delitem__(self, key):
        del self.registers[key]

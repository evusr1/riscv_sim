import register
import instruction
import decoder
import utypes
import execute


class RV32I():
    def __init__(self, memorymap, reset_vector):
        self._memorymap = memorymap
        self.registers = register.Registers()
        self._instructions = instruction.Instruction(self.registers)
        self._decoder = decoder.Decoder(self._instructions, self._memorymap)
        self._execute = execute.Execute(self._decoder)
        self._reset_vector = reset_vector
        self.reset()

    def reset(self):
        self.registers.reset()
        self.registers[register.PC] = utypes.Uint32(self._reset_vector)


    def run(self):
        try:
            while True:
                PC = self.registers[register.PC].value
                current_instruction = self._memorymap[PC]

                self._execute.execute(current_instruction)
        except instruction.ECALL:
            print("CPU ECALL")




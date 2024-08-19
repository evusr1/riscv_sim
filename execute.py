class Execute():
    def __init__(self, decoder):
        self._decoder = decoder

    def execute(self, instruction_in):
        instruction = self._decoder.decode(instruction_in)
        instruction_func = instruction[0]
        instruction_args = instruction[1]

        return instruction_func(*instruction_args)

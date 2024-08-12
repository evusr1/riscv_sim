import utypes

class Ram:
    def __init__(self, size):
        self.__memory = bytearray(size)

    def __getitem__(self, key):
        if isinstance(key, slice):
            return self.__memory[key]

        if key < len(self.__memory) - 4:
            return utypes.Uint32((self.__memory[key + 3] << 24) | (self.__memory[key + 2] << 16) | (self.__memory[key + 1] << 8) | self.__memory[key])

        raise IndexError

    def __setitem__(self, key, data):
        if isinstance(key, slice):
            self.__memory[key] = data
            return

        if key < len(self.__memory) - 4:
            self.__memory[key] = data.value & 0xFF
            self.__memory[key + 1] = (data.value >> 8 ) & 0xFF
            self.__memory[key + 2] = (data.value >> 16 ) & 0xFF
            self.__memory[key + 3] = (data.value >> 24 ) & 0xFF
            return

        raise IndexError

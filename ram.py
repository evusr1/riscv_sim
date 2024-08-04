import types

class Ram:
    def __init__(self, size):
        self.__memory = bytearray(size)

    def __getitem__(self, key):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self.__memory))
            return bytearray(self.__memory[i] for i in range(start, stop, step))

        if key < len(self.__memory) - 4:
            return types.Uint32((self.__memory[key + 3] << 24) | (self.__memory[key + 2] << 16) | (self.__memory[key + 1] << 8) | self.__memory[key])

        raise IndexError

    def __setitem__(self, key, data):
        if isinstance(key, slice):
            start, stop, step = key.indices(len(self.__memory))
            j = 0
            for i in range(start, stop, step):
                 self.__memory[i] = data[j]
                 j += 1
            return

        if key < len(self.__memory) - 4:
            print(data)
            self.__memory[key] = data.value & 0xFF
            self.__memory[key + 1] = (data.value >> 8 ) & 0xFF
            self.__memory[key + 2] = (data.value >> 16 ) & 0xFF
            self.__memory[key + 3] = (data.value >> 24 ) & 0xFF
            return

        raise IndexError

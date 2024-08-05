import math

class MemoryMap():
    def __init__(self):
        self.__devices = {}

    def add_device(self, device, start_address, end_address):
        self.__devices[(start_address, end_address)] = device

    def get_device_range(self, address):
        for memory_range in self.__devices.keys():
            if address >= memory_range[0] and address < memory_range[1]:
                return memory_range

    def __convert_slice(self, key, device_range):
            memory_range = device_range[1] - device_range[0]

            if abs(key.stop) not in range(device_range[0], device_range[1] + 1):
                raise IndexError

            if abs(key.start) not in range(device_range[0], device_range[1] + 1):
                raise IndexError

            lower = key.start
            upper = key.stop

            if key.start > 0:
                lower = key.start - device_range[0]

            if key.stop > 0:
                upper = key.stop - device_range[0]

            return slice(lower, upper, key.step)
    def __getitem__(self, key):
        if isinstance(key, slice):
            device_range = self.get_device_range(key.start)
            new_slice = self.__convert_slice(key, device_range)
            return self.__devices[device_range][new_slice]

        device_range = self.get_device_range(key)
        return self.__devices[device_range][key - device_range[0]]

    def __setitem__(self, key, data):
        if isinstance(key, slice):
            device_range = self.get_device_range(key.start)
            new_slice = self.__convert_slice(key, device_range)
            self.__devices[device_range][new_slice] = data
            return

        device_range = self.get_device_range(key)
        self.__devices[device_range][key - device_range[0]] = data
        return

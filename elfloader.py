import os
from elftools.elf.elffile import ELFFile
from elftools.elf.segments import Segment

class Loader():
    def __init__(self, memorymap):
        self._memorymap = memorymap

    def from_file(self, path):
        print("LOAD ELF")

        with open(path, "rb") as file_stream:
            for segment in ELFFile(file_stream).iter_segments():
                if segment['p_type'] == "PT_LOAD":
                    p_vaddr = segment['p_vaddr']
                    p_offset = segment['p_offset']
                    p_filesz = segment['p_filesz']

                    file_stream.seek(p_offset, os.SEEK_SET)
                    print("p_vaddr", hex(p_vaddr))
                    print("p_offset", hex(p_offset))
                    print("p_filesz", hex(p_filesz))

                    self._memorymap[p_vaddr:p_vaddr + p_filesz] = file_stream.read(p_filesz)


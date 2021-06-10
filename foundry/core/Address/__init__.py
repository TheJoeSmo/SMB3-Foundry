def determine_pc_offset(cur_pc_offset: int, rom_offset: int) -> int:
    """Determines the 16 bit program counter."""
    if rom_offset >= 0:
        base_offset = rom_offset & 0b0001_1111_1111_1111
        pc_offset = cur_pc_offset & 0b1110_0000_0000_0000
        return pc_offset + base_offset
    else:
        return -1


def determine_rom_offset(pc_offset: int, cur_rom_offset: int) -> int:
    """Determines the global ROM offset from the change in the program counter"""
    if cur_rom_offset >= 0:
        base_offset = cur_rom_offset & 0b1111_1111_1111_1111_1110_0000_0000_0000
        pc_offset = pc_offset & 0b0001_1111_1111_1111
        return pc_offset + base_offset
    else:
        return -1

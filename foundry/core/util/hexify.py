

def hexify(number_to_be_hexed: int):
    """
    Produces a pretty hex value for display 6502 assembly in a more native form.
    :param number_to_be_hexed: The number that will be converted to a hex string
    :return: The asm6 format of a hex number
    """
    if number_to_be_hexed <= 0xFF:
        return f"${format(number_to_be_hexed, '02X')}"
    elif number_to_be_hexed <= 0xFFFF:
        return f"${format(number_to_be_hexed, '04X')}"
    return f"${hex(number_to_be_hexed)[:2]}"

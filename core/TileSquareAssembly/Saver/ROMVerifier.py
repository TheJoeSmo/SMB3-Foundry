from typing import Callable
from copy import copy

from core.TileSquareAssembly.ROM import ROM
from core.Saver.Verifier import Verifier


class ROMVerifier(Verifier):
    def __init__(self, resolver: Callable):
        self.resolver = resolver

    def is_like(self, primary: ROM, secondary: ROM) -> bool:
        """
        Determines if two savers are similar enough to one another to be considered the same.
        """
        p_data, s_data = primary.data[1:], secondary.data[1:]  # Ignore the name of the ROM

        for (p_tsa, s_tsa) in zip(p_data[0], s_data[0]):
            if p_tsa.tsa_offset != s_tsa.tsa_offset:
                return False

            for (p_block, s_block) in zip(p_tsa.blocks, s_tsa.blocks):
                if p_block.patterns != s_block.patterns:
                    return False

        return True

    def resolution(self, primary: ROM, secondary: ROM) -> ROM:
        """
        Resolves the conflict, by choosing one of the two.
        """
        return self.resolver(primary, secondary)

    def apply(self, primary: ROM, secondary: ROM) -> ROM:
        """
        Applies data from one saver to another.  Primary will attempt to write its data ontop of secondary.
        """
        primary_copy = copy(primary)
        primary_copy.from_copy(secondary)
        return primary_copy

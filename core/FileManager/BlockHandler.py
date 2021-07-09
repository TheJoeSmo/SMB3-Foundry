from dataclasses import astuple

from sqlalchemy.orm import Session

from core.Block import Block

from core.FileManager.AbstractHandler import AbstractHandler
from core.FileManager.FileHandlerMeta import FileHandlerMeta
from core.FileManager.BlockMeta import BlockMeta


class BlockHandler(AbstractHandler):
    """Provide a series of helper functions to help create Blocks"""
    def __init__(self, handler: FileHandlerMeta):
        self.handler = handler
        self._blocks = []
        self._block_hash = {}

    def generate(self, session: Session, **kwargs) -> None:
        """Generates a series of blocks"""
        for block in self._blocks:
            session.add(block)

    def register(self, block_meta: BlockMeta) -> Block:
        """Determines how to create the block"""
        attr = astuple(block_meta)
        if attr not in self._block_hash:
            block = Block(
                top_left=attr.top_left,
                top_right=attr.top_right,
                bottom_left=attr.bottom_left,
                bottom_right=attr.bottom_right
            )
            self._blocks.append(block)
            self._block_hash.update({attr: block})
        return self._block_hash[attr]

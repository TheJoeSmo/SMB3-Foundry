from pathlib import Path

from foundry.game.File import ROM as File
from foundry.game.gfx.GraphicsSet import GraphicsSet

from smb3parse.constants import BASE_OFFSET, PAGE_A000_ByTileset, WORLD_MAP_TSA_INDEX

from core.Cursor.Cursor import Connection


root_dir = Path(__file__).parent.parent / "recources"

create_tsa_database = root_dir / "create_database.sql"


def load_or_create_database():
    with Connection() as connection:
        with open(create_tsa_database, "r") as f:
            connection.executescript(f.read())


def get_tsa_offset(index, start_byte=PAGE_A000_ByTileset):
    if index == 0:
        return BASE_OFFSET + WORLD_MAP_TSA_INDEX * 0x2000
    else:
        return BASE_OFFSET + File().get_byte(start_byte + index) * 0x2000


def get_tsa_pattern_tables(index):
    return GraphicsSet(index).segments[0:2]


def determine_count_of_tilesets(index=0, start_byte=PAGE_A000_ByTileset, end_byte=0x60):
    while True:
        if end_byte == File().get_byte(start_byte + index):
            return index
        else:
            index += 1

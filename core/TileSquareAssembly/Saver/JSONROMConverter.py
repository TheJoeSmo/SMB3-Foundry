from typing import Dict

from foundry.core.TileSquareAssembly.ROM import ROM
from foundry.core.TileSquareAssembly.TileSquareAssembly import TileSquareAssembly
from foundry.core.TileSquareAssembly.Block import Block
from foundry.core.TileSquareAssembly.PatternTable import PatternTable


def dict_to_rom(d: Dict) -> ROM:
    tsas, blocks, ptn_tbls = d["tile_square_assemblies"], d["blocks"], d["pattern_tables"]
    created_blocks, created_ptn_tbls, created_tsas = {}, {}, []

    for block_id, block in blocks.items():
        created_blocks.update(
            {
                int(block_id): Block.from_data(
                    block["name"], block["top_left"], block["top_right"], block["bottom_left"], block["bottom_right"]
                )
            }
        )

    for ptn_tbl_id, ptn_tbl in ptn_tbls.items():
        created_ptn_tbls.update({int(ptn_tbl_id): PatternTable.from_data(ptn_tbl["offset"])})

    for tsa in tsas.values():
        created_tsas.append(
            TileSquareAssembly.from_data(
                tsa["name"],
                tsa["tsa_offset"],
                created_ptn_tbls[tsa["top_pattern_table"]],
                created_ptn_tbls[tsa["bottom_pattern_table"]],
                [created_blocks[block] for block in tsa["blocks"]],
            )
        )

    return ROM.from_data(None, created_tsas)


def rom_to_dict(rom: ROM):
    # Remove any duplicates.
    tsas, blocks, pattern_tables = set(), {}, {}

    # Always reset the ids, for user convience.
    block_id = 1
    ptn_tbl_id = 1

    for tsa in rom.tile_square_assemblies:
        tsas.add(tsa)

        for pattern_table in tsa.pattern_tables:
            if (pattern_table.offset,) not in pattern_tables:
                pattern_tables.update({(pattern_table.offset,): ptn_tbl_id})
                ptn_tbl_id += 1

        ptn_tbls = tsa.pattern_tables
        for block in tsa.blocks:
            block_meta = (block.name, ptn_tbls[0].offset, ptn_tbls[1].offset, *block.patterns)
            if block_meta not in blocks:
                blocks.update({block_meta: block_id})
                block_id += 1

    return {
        "tile_square_assemblies": {
            tsa_id: {
                "name": tsa.name,
                "tsa_offset": tsa.tsa_offset,
                "top_pattern_table": pattern_tables[(tsa.pattern_tables[0].offset,)],
                "bottom_pattern_table": pattern_tables[(tsa.pattern_tables[1].offset,)],
                "blocks": [
                    blocks[(block.name, tsa.pattern_tables[0].offset, tsa.pattern_tables[1].offset, *block.patterns)]
                    for block in tsa.blocks
                ],
            }
            for tsa_id, tsa in enumerate(list(tsas))
        },
        "blocks": {
            block_id: {
                "name": name,
                "top_left": patterns[0],
                "top_right": patterns[1],
                "bottom_left": patterns[2],
                "bottom_right": patterns[3],
            }
            for (name, _, _, *patterns), block_id in blocks.items()
        },
        "pattern_tables": {ptn_tbl_id: {"offset": offset} for (offset,), ptn_tbl_id in pattern_tables.items()},
    }

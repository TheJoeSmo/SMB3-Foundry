"""
Constants for the PatternTables
"""

CHR_PAGE = CHR_ROM_SEGMENT_SIZE = 0x400

WORLD_MAP = 0
SPADE_ROULETTE = 16
N_SPADE = 17
VS_2P = 18

graphic_set2chr_index = {
    0: 0x14,  # World
    1: 0x08,  # Plains
    2: 0x10,  # Fortress
    3: 0x1C,  # Hills / Underground
    4: 0x0C,  # Sky
    5: 0x58,  # Piranha Plant
    6: 0x58,  # Water
    7: 0x5C,  # Mushroom
    8: 0x58,  # Pipe
    9: 0x30,  # Desert
    10: 0x34,  # Ship
    11: 0x6E,  # Giant
    12: 0x18,  # Ice
    13: 0x38,  # Cloudy
    14: 0x1C,  # Not Used (same as 3)
    15: 0x24,  # Bonus Room
    16: 0x2C,  # Spade (Roulette)
    17: 0x5C,  # N-Spade (Card)
    18: 0x58,  # 2P vs.
    19: 0x6C,  # Hills / Underground alternative
    20: 0x68,  # 3-7 only
    21: 0x34,  # World 8 War Vehicle
    22: 0x28,  # Throne Room
}

common_set2chr_index = {
    0: 0x16,  # World
    1: 0x60,  # Plains
    2: 0x60,  # Fortress
    3: 0x60,  # Hills / Underground
    4: 0x60,  # Sky
    5: 0x3E,  # Piranha Plant
    6: 0x60,  # Water
    7: 0x5E,  # Mushroom
    8: 0x60,  # Pipe
    9: 0x60,  # Desert
    10: 0x6A,  # Ship
    11: 0x60,  # Giant
    12: 0x60,  # Ice
    13: 0x60,  # Cloudy
    14: 0x60,  # Not Used (same as 3)
    15: 0x5E,  # Bonus Room
    16: 0x2E,  # Spade (Roulette)
    17: 0x5E,  # N-Spade (Card)
    18: 0x60,  # 2P vs.
    19: 0x60,  # Hills / Underground alternative
    20: 0x60,  # 3-7 only
    21: 0x70,  # World 8 War Vehicle
    22: 0x60,  # Throne Room
}


GRAPHIC_SET_NAMES = [
    "Mario graphics (1)",
    "Plain",
    "Dungeon",
    "Underground (1)",
    "Sky",
    "Pipe/Water (1, Piranha Plant)",
    "Pipe/Water (2, Water)",
    "Mushroom house (1)",
    "Pipe/Water (3, Pipe)",
    "Desert",
    "Ship",
    "Giant",
    "Ice",
    "Clouds",
    "Underground (2)",
    "Spade bonus room",
    "Spade bonus",
    "Mushroom house (2)",
    "Pipe/Water (4)",
    "Hills",
    "Plain 2",
    "Tank",
    "Castle",
    "Mario graphics (2)",
    "Animated graphics (1)",
    "Animated graphics (2)",
    "Animated graphics (3)",
    "Animated graphics (4)",
    "Animated graphics (P-Switch)",
    "Game font/Course Clear graphics",
    "Animated graphics (5)",
    "Animated graphics (6)",
]

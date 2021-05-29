PRAGMA JOURNAL_MODE = WAL;

CREATE TABLE IF NOT EXISTS ROMs (
    ROMID INTEGER PRIMARY KEY AUTOINCREMENT,
    NAME TEXT
);

CREATE TABLE IF NOT EXISTS PatternTables (
    PTID INTEGER PRIMARY KEY AUTOINCREMENT,
    PTOffset INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Blocks (
    BlockID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    TopLeft INTEGER NOT NULL,
    TopRight INTEGER NOT NULL,
    BottomLeft INTEGER NOT NULL,
    BottomRight INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS TileSquareAssemblies (
    TSAID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT,
    TSAOffset INTEGER NOT NULL,
    TopPTID INTEGER NOT NULL REFERENCES PatternTables(PTID),
    BottomPTID INTEGER NOT NULL REFERENCES PatternTables(PTID)
);

-- ROMs that need to be deleted on tear down and start up
CREATE TABLE IF NOT EXISTS ROMTemp (
    ROMDI INTEGER NOT NULL REFERENCES ROMs(ROMID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS ROMTileSquareAssemblies (
    ROMTSAID INTEGER PRIMARY KEY AUTOINCREMENT,
    ROMID INTEGER NOT NULL REFERENCES ROMs(ROMID) ON DELETE CASCADE,
    TSAID INTEGER NOT NULL REFERENCES TileSquareAssemblies(TSAID) ON DELETE CASCADE    
);

CREATE TABLE IF NOT EXISTS TSABlocks (
    BlockIndex INTEGER NOT NULL,
    TSAID INTEGER NOT NULL REFERENCES TileSquareAssemblies(TSAID) ON DELETE CASCADE,
    BlockID INTEGER NOT NULL REFERENCES Blocks(BlockID) ON DELETE CASCADE,
    PRIMARY KEY (BlockIndex, TSAID)
);
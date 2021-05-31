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

CREATE TABLE IF NOT EXISTS Containers (
    ContainerID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name Text,
    ROMOffset INTEGER NOT NULL,
    PCOffset INTEGER NOT NULL,
    Size INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS Addresses (
    AddressID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name Text,
    ContainerOffset INTEGER NOT NULL,
    ContainerID INTEGER NOT NULL REFERENCES Containers(ContainerID) ON DELETE CASCADE,
);

CREATE TABLE IF NOT EXISTS Fillers (
    FillerID INTEGER PRIMARY KEY AUTOINCREMENT,
    AddressID INTEGER NOT NULL REFERENCES Addresses(AddressID) ON DELETE CASCADE,
    Size INTEGER
);

CREATE TABLE IF NOT EXISTS DrawUpdates (
    DrawUpdateID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name Text,
    FillerID INTEGER NOT NULL REFERENCES Fillers(FillerID)
);


CREATE TABLE IF NOT EXISTS DrawEvents (
    DrawEventID INTEGER PRIMARY KEY AUTOINCREMENT,
    PPUAddress INTEGER NOT NULL,
    Type INTEGER NOT NULL,
    Repeat INTEGER NOT NULL,
    TileCount INTEGER NOT NULL
);

CREATE TABLE IF NOT EXISTS DrawTiles (
    EventIndex INTEGER NOT NULL,
    DrawEventID INTEGER NOT NULL REFERENCES DrawEvents(DrawEventID) ON DELETE CASCADE,
    Tile INTEGER,
    PRIMARY KEY (EventIndex, DrawEventID)
);

CREATE TABLE IF NOT EXISTS ROMDrawUpdates (
    ROMDUID INTEGER PRIMARY KEY AUTOINCREMENT 
    ROMID INTEGER NOT NULL REFERENCES ROMs(ROMID) ON DELETE CASCADE,
    DrawUpdateID INTEGER NOT NULL REFERENCES DrawUpdates(DrawUpdateID) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS DrawUpdateEvents (
    DrawUpdateID INTEGER NOT NULL REFERENCES DrawUpdates(DrawUpdateID) ON DELETE CASCADE,
    UpdateIndex INTEGER NOT NULL,
    DrawEventID INTEGER NOT NULL REFERENCES DrawEvents(DrawEventID) ON DELETE CASCADE,
    PRIMARY KEY (DrawUpdateID, UpdateIndex)
);
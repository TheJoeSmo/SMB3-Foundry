from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))
Base = declarative_base()


def create_database():
    # Load all the elements of the database and assert them so Black doesn't complain
    from foundry.core.Address.Address import Address

    assert issubclass(Address, Base)
    from foundry.core.Block.Block import Block

    assert issubclass(Block, Base)
    from foundry.core.BlockGroup.BlockGroup import BlockGroup

    assert issubclass(BlockGroup, Base)
    from foundry.core.Container.Container import Container

    assert issubclass(Container, Base)
    from foundry.core.DrawEvent.DrawEvent import DrawEvent

    assert issubclass(DrawEvent, Base)
    from foundry.core.DrawTile.DrawTile import DrawTile

    assert issubclass(DrawTile, Base)
    from foundry.core.File.File import File

    assert issubclass(File, Base)
    from foundry.core.Filler.Filler import Filler

    assert issubclass(Filler, Base)
    from foundry.core.PatternTable.PatternTable import PatternTable

    assert issubclass(PatternTable, Base)

    Base.metadate.createall(engine)

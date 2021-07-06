from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy_continuum import make_versioned

engine = create_engine("sqlite:///:memory:")
session = scoped_session(sessionmaker(bind=engine))
make_versioned(user_cls=None)
Base = declarative_base()


def create_database():
    """
    Load all the elements of the database and assert that they exist to appease Black
    Note: The order of imports is very particular.
            The imports will are a pyramid; they point to the base object.
    """

    from core.Block import Block
    from core.PatternTable import PatternTable
    from core.BlockGroup import BlockGroup
    from core.File import File
    from core.DrawTile import DrawTile
    from core.DrawEvent import DrawEvent
    from core.DrawUpdate import DrawUpdate
    from core.Filler import Filler
    from core.Address import Address
    from core.Container import Container

    assert issubclass(Container, Base)
    assert issubclass(Address, Base)
    assert issubclass(Block, Base)
    assert issubclass(BlockGroup, Base)
    assert issubclass(DrawEvent, Base)
    assert issubclass(DrawUpdate, Base)
    assert issubclass(DrawTile, Base)
    assert issubclass(File, Base)
    assert issubclass(Filler, Base)
    assert issubclass(PatternTable, Base)

    Base.metadata.create_all(engine)

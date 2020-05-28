from dataclasses import dataclass
from PySide2.QtCore import QSize
from foundry.game.Position import Position


@dataclass
class Size:
    """Defines a 2d shape"""
    _width: float = 0
    _height: float = 0

    @property
    def width(self):
        return int(self._width)

    @width.setter
    def width(self, width):
        self._width = width

    @property
    def height(self):
        return int(self._height)

    @height.setter
    def height(self, height):
        self._height = height

    def to_qt(self) -> QSize:
        return QSize(self.width, self.height)

    def get_relational_position(self, pos: Position) -> int:
        """
        Returns a number to indicate the position in relation to the size
        :param Position pos: the relative position
        :return: The index (0 - 8) going from left to right, top to bottom.
        :rtype: int
        """
        return self.get_scaler_relational_position(pos.x) + \
            (self.get_scaler_relational_position(pos.y, width=False) * 3)

    def get_scaler_relational_position(self, pos, width=True) -> int:
        """
        Returns a number to indicate the position in relation to the width
        :param pos: The positional parameter
        :param width: If we are using the width or height
        :return: The index (0 - 2) going from left to right or top to bottom
        :rtype: int
        """
        scaler = self.width if width else self.height
        if pos == 0:
            return 0
        elif pos == scaler - 1:
            return 2
        else:
            return 1

    def invert(self):
        """
        Invert the width and height
        :return: The inverted size
        :rtype: Size
        """
        return Size(self._height, self._width)

    def flip_rows(self, l: list, width: bool = True):
        """
        Flip the list in terms of the width or height
        :param l: The list to be flipped
        :param width: Flip along the vertical or horizontal axis
        :return: A flipped list
        :rtype: list
        """
        rows = []
        for pos in self.height_positions() if width else self.width_positions():
            row = []
            for other_pos in self.reversed_width_positions() if width else self.reversed_height_positions():
                row.append(l[self.index_position(pos + other_pos)])
            rows.extend(row)
        return rows

    def reversed_width_positions(self):
        """
        Provides a reversed generator for every relative position inside the width
        :return: A generator of relative positions
        :rtype: Generator of Positions
        """
        for pos in reversed(range(self.width)):
            yield Position(pos, 0)

    def width_positions(self):
        """
        Provides a generator for every relative position inside the width
        :return: A generator of relative positions
        :rtype: Generator of Positions
        """
        for pos in range(self.width):
            yield Position(pos, 0)

    def reversed_height_positions(self):
        """
        Provides a reversed generator for every relative position inside the height
        :return: A generator of relative positions
        :rtype: Generator of Positions
        """
        for pos in reversed(range(self.height)):
            yield Position(0, pos)

    def height_positions(self):
        """
        Provides a generator for every relative position inside the height
        :return: A generator of relative positions
        :rtype: Generator of Positions
        """
        for pos in range(self.height):
            yield Position(0, pos)

    def positions(self, width=True):
        """
        Provides every single idx from the matrix of positions
        :param bool width: Determines if we are finding the width or height
        :return: A generator of relative positions
        :rtype: Generator of Positions
        """
        positions = self._index_positions(not width)
        for pos in positions:
            for other_pos in self._index_positions(width):
                yield pos + other_pos

    def index_position(self, pos: Position, width=True) -> int:
        """
        Converts position to an index for a matrix
        :param Position pos: A relative position for a matrix
        :param bool width: Determines if the width or height is the low or high value
        :return: An index for a matrix
        :rtype: int
        """
        return pos.to_index(self.width if width else self.height, width)

    def _index_positions(self, width=True):
        """
        Provides a generator for every relative position inside the width/height
        :param bool width: Determines if we are finding the width or height
        :return: A generator of relative positions
        :rtype: Generator of Positions
        """
        scaler = self.width if width else self.height
        for idx in range(scaler):
            yield Position(idx, 0) if width else Position(0, idx)

    @classmethod
    def from_size(cls, size):
        """
        Makes a size from a size
        :param Size size: The size to be copied
        :return: The copied size
        :rtype: Size
        """
        return Size(size._width, size._height)


    @classmethod
    def from_qt(cls, qsize: QSize):
        """Returns the Qsize version of the object"""
        return cls(*qsize.toTuple())

    @classmethod
    def from_dict(cls, dic: dict, default_width: int = 1, default_height: int = 1):
        """Makes a 2d size from a dictionary of values"""
        width = dic["width"] if "width" in dic else default_width
        height = dic["height"] if "height" in dic else default_height
        return cls(width, height)

    def __add__(self, other):
        if isinstance(other, Size):
            return Size(self.width + other.width, self.height + other.height)
        elif isinstance(other, (int, float)):
            return Size(self.width + other, self.height + other)
        else:
            return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Size):
            return Size(self.width - other.width, self.height - other.height)
        elif isinstance(other, (int, float)):
            return Size(self.width - other, self.height - other)
        else:
            return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, Size):
            return Size(other.width - self.width, other.height - self.height)
        elif isinstance(other, (int, float)):
            return Size(other - self.width, other - self.height)

    def __mul__(self, other):
        if isinstance(other, Size):
            return Size(self.width * other.width, self.height * other.height)
        elif isinstance(other, (int, float)):
            return Size(self.width * other, self.height * other)
        else:
            return NotImplemented

    def __rmul__(self, other):
        return self.__mul__(other)

    def __truediv__(self, other):
        if isinstance(other, Size):
            return Size(self.width / other.width, self.height / other.height)
        elif isinstance(other, (int, float)):
            return Size(self.width / other, self.height / other)
        else:
            return NotImplemented

    def __rtruediv__(self, other):
        if isinstance(other, Size):
            return Size(other.width / self.width, other.height / self.height)
        elif isinstance(other, (int, float)):
            return Size(other / self.width, other / self.height)
        else:
            return NotImplemented

    def __floordiv__(self, other):
        if isinstance(other, Size):
            return Size(self.width // other.width, self.height // other.height)
        elif isinstance(other, (int, float)):
            return Size(self.width // other, self.height // other)
        else:
            return NotImplemented

    def __rfloordiv__(self, other):
        if isinstance(other, Size):
            return Size(other.width // self.width, other.height // self.height)
        elif isinstance(other, (int, float)):
            return Size(other // self.width, other // self.height)
        else:
            return NotImplemented

    def __mod__(self, other):
        if isinstance(other, Size):
            return Size(self.width % other.width, self.height % other.height)
        elif isinstance(other, (int, float)):
            return Size(self.width % other, self.height % other)
        else:
            return NotImplemented

    def __rmod__(self, other):
        if isinstance(other, Size):
            return Size(other.width % self.width, other.height % self.height)
        elif isinstance(other, (int, float)):
            return Size(other % self.width, other % self.height)
        else:
            return NotImplemented

    def __iadd__(self, other):
        """Implicity add"""
        if isinstance(other, Size):
            self.width += other.width
            self.height += other.height
        elif isinstance(other, (int, float)):
            self.width += other
            self.height += other
        else:
            return NotImplemented
        return self

    def __isub__(self, other):
        """Implicity subtract"""
        if isinstance(other, Size):
            self.width -= other.width
            self.height -= other.height
        elif isinstance(other, (int, float)):
            self.width -= other
            self.height -= other
        else:
            return NotImplemented
        return self

    def __imul__(self, other):
        """Implicity multiply"""
        if isinstance(other, Size):
            self.width *= other.width
            self.height *= other.height
        elif isinstance(other, (int, float)):
            self.width *= other
            self.height *= other
        else:
            return NotImplemented
        return self

    def __itruediv__(self, other):
        """Implicity division"""
        if isinstance(other, Size):
            self.width /= other.width
            self.height /= other.height
        elif isinstance(other, (int, float)):
            self.width /= other
            self.height /= other
        else:
            return NotImplemented
        return self

    def __ifloordiv__(self, other):
        """Implicity divide"""
        if isinstance(other, Size):
            self.width //= other.width
            self.height //= other.height
        elif isinstance(other, (int, float)):
            self.width //= other
            self.height //= other
        else:
            return NotImplemented
        return self

    def __imod__(self, other):
        """Implicity mod"""
        if isinstance(other, Size):
            self.width %= other.width
            self.height %= other.height
        elif isinstance(other, (int, float)):
            self.width %= other
            self.height %= other
        else:
            return NotImplemented
        return self

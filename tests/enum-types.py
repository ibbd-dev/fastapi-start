from enum import Enum, IntEnum
from enum import Flag, auto

class Color(IntEnum):
    # RED = 1
    # GREEN = 2
    # BLUE = 3
    RED = auto()
    BLUE = auto()
    GREEN = auto()


class Status(Enum):
    SUCC = 'succ'
    FAIL = 'fail'


class ColorFlag(Flag):
    RED = auto()
    BLUE = auto()
    GREEN = auto()


print(Color.RED.value)
print(Color.RED.name)
print(Status.SUCC.value)
print(Status.SUCC.name)
print(ColorFlag.RED.value)
print(ColorFlag.BLUE.value)
print(ColorFlag.BLUE | ColorFlag.RED)
print((ColorFlag.BLUE & ColorFlag.RED).value)

print(Color.BLUE | Color.RED)
print((Color.BLUE & Color.RED).value)

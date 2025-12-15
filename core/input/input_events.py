from enum import Enum, auto

class GazeDirection(Enum):
    LEFT = auto()
    RIGHT = auto()
    UP = auto()
    DOWN = auto()
    CENTER = auto()

class BlinkType(Enum):
    NONE = auto()
    SINGLE = auto()
    DOUBLE = auto()
    LONG = auto()

class Action(Enum):
    MOVE_LEFT = auto()
    MOVE_RIGHT = auto()
    MOVE_UP = auto()
    MOVE_DOWN = auto()
    SELECT = auto()
    OPEN_KEYBOARD = auto()
    SWITCH_TAB = auto()
    HELP_ALERT = auto()
    NONE = auto()

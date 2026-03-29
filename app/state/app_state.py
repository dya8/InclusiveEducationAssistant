from enum import Enum, auto

class AppState(Enum):
    LOGIN = auto()
    START_CALIBRATION = auto()
    CALIBRATION = auto()
    
    HOME = auto()
    NOTES = auto()
    CODING = auto()
    VIEW_NOTES = auto()
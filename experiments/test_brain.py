import time
from core.input.input_manager import InputManager
from core.input.input_events import GazeDirection, BlinkType

im = InputManager()

print(im.update(GazeDirection.RIGHT, BlinkType.NONE))
time.sleep(0.5)

print(im.update(GazeDirection.CENTER, BlinkType.SINGLE))
time.sleep(0.5)

print(im.update(GazeDirection.CENTER, BlinkType.DOUBLE))
time.sleep(0.5)

print(im.update(GazeDirection.CENTER, BlinkType.LONG))

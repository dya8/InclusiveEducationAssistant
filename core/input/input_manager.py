import time
from core.input.input_events import GazeDirection, BlinkType, Action


class InputManager:
    def __init__(self):
        self.last_action_time = 0
        self.action_cooldown = 0.4  # seconds

    def _cooldown_ok(self):
        return (time.time() - self.last_action_time) > self.action_cooldown

    def update(
        self,
        gaze: GazeDirection,
        blink: BlinkType,
        dwell_time: float = 0.0,
        head_stable: bool = True,
        eog_signal=None
    ) -> Action:
        """
        Called every frame.
        Returns ONE Action.
        """

        # -------- BLINK ACTIONS (highest priority) --------
        if blink == BlinkType.LONG and self._cooldown_ok():
            self.last_action_time = time.time()
            return Action.OPEN_KEYBOARD

        if blink == BlinkType.DOUBLE and self._cooldown_ok():
            self.last_action_time = time.time()
            return Action.SWITCH_TAB

        if blink == BlinkType.SINGLE and self._cooldown_ok():
            self.last_action_time = time.time()
            return Action.SELECT

        # -------- GAZE ACTIONS --------
        if head_stable and self._cooldown_ok():
            gaze_to_action = {
                GazeDirection.LEFT: Action.MOVE_LEFT,
                GazeDirection.RIGHT: Action.MOVE_RIGHT,
                GazeDirection.UP: Action.MOVE_UP,
                GazeDirection.DOWN: Action.MOVE_DOWN,
            }

            if gaze in gaze_to_action:
                self.last_action_time = time.time()
                return gaze_to_action[gaze]

        return Action.NONE

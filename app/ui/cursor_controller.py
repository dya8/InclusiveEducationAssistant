from core.input.input_events import Action
class CursorController:
    def __init__(self, eye_cursor):
        self.cursor = eye_cursor

    def move_to(self, x_norm, y_norm):
        """
        x_norm, y_norm ∈ [0, 1]
        """
        screen_x = int(x_norm * self.cursor.parent().width())
        screen_y = int(y_norm * self.cursor.parent().height())
        self.cursor.set_position(screen_x, screen_y)

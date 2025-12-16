from core.input.input_events import Action

class CursorController:
    def __init__(self, eye_cursor):
        self.cursor = eye_cursor
        self.speed = 12

    def handle_action(self, action):
        if action == Action.MOVE_LEFT:
            self.cursor.move_cursor(-self.speed, 0)
        elif action == Action.MOVE_RIGHT:
            self.cursor.move_cursor(self.speed, 0)
        elif action == Action.MOVE_UP:
            self.cursor.move_cursor(0, -self.speed)
        elif action == Action.MOVE_DOWN:
            self.cursor.move_cursor(0, self.speed)

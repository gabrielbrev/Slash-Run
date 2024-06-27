from .entity import Entity

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA

class FixedEntity(Entity):
    def __init__(self, x, y, width, height):
        super().__init__(x, y, width, height)
        self.window = GD.get_window()

        self.move_animation = MA(self, x, y)

    def move_to(self, x, y, duration_s, animation, overshoot=1.7015, buffer=False):
        self.move_animation.move_to(x, y, duration_s, animation, overshoot, buffer)

    def update_position(self):
        self.move_animation.update()
        super().update_position()

    def is_moving(self):
        return self.move_animation.is_playing()

    def update(self):
        super().update()

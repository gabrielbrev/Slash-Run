from PPlay.mouse import Mouse
from PPlay.window import Window
from PPlay.sprite import Sprite

from scenes.scene_objects.transition import Transition

from .button import Button

class LockedButton(Button):
    def __init__(self, mouse: Mouse, button_image, lock_image, locked=True, command: callable = None, args: tuple = (), transition: Transition = None):
        super().__init__(mouse, button_image, command, args, transition)
        self.lock_sprite = Sprite(lock_image, 1)
        self.locked = locked
        if locked:
            self.set_curr_frame(1)
    
    def lock(self):
        self.set_curr_frame(1)
        self.locked = True
    
    def unlock(self):
        self.set_curr_frame(0)
        self.locked = False

    def set_position(self, x, y):
        super().set_position(x, y)
        self.lock_sprite.set_position(
            x=self.x + self.width/2 - self.lock_sprite.width/2,
            y=self.y + self.height/2 - self.lock_sprite.height/2
        )

    def update(self):
        if not self.locked:
            super().update()

    def draw(self):
        super().draw()
        if self.locked:
            self.lock_sprite.draw()
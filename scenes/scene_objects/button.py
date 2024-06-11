from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
from PPlay.window import Window

from .transition import Transition

class Button(Sprite):
    def __init__(self, window: Window, mouse: Mouse, image_file, frames = 2, command: callable = None, args: tuple = (), transition: Transition = None):
        super().__init__(image_file, frames)
        self.window = window
        self.mouse = mouse
        self.command = command
        self.args = args
        self.pressed = False
        self.transition = transition

    def was_pressed(self):
        return self.pressed
    
    def update(self):
        if self.mouse.is_over_object(self):
            self.set_curr_frame(1)
            if self.mouse.is_button_pressed(1):
                self.pressed = True
                if self.command:
                    if self.transition:
                        self.transition.play_out(self.window)
                    self.command(*self.args)
            else:
                self.pressed = False
        else:
            self.pressed = False
            self.set_curr_frame(0)
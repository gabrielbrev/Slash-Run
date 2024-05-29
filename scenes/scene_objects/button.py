from PPlay.sprite import Sprite
from PPlay.mouse import Mouse

class Button(Sprite):
    def __init__(self, mouse: Mouse, image_file, frames = 2, command: callable = None, args: tuple = ()):
        super().__init__(image_file, frames)
        self.mouse = mouse
        self.command = command
        self.args = args
    
    def update(self):
        if self.mouse.is_over_object(self):
            self.set_curr_frame(1)
            if self.mouse.is_button_pressed(1):
                if self.command:
                    self.command(*self.args)
        else:
            self.set_curr_frame(0)
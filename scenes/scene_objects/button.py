from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
from PPlay.window import Window

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation

from .transition import Transition

class Button(Sprite):
    def __init__(self, mouse: Mouse, image_file, command: callable = None, args: tuple = (), transition: Transition = None):
        super().__init__(image_file, 2)
        self.window = GD.get_window()
        self.mouse = mouse
        self.command = command
        self.args = args
        self.clicked = False
        self.transition = transition

        self.move_animation = MoveAnimation(self, self.x, self.y)

    def move_to(self, x, y, duration_s, animation):
        self.move_animation.move_to(x, y, duration_s, animation)

    def is_clicked(self):
        return self.clicked
    
    def update(self):
        if self.mouse.is_over_object(self):
            self.set_curr_frame(1)
            if self.mouse.is_button_pressed(1):
                self.clicked = True
                if self.command:
                    if self.transition:
                        self.transition.play_out(self.window)
                    self.command(*self.args)
            else:
                self.clicked = False
        else:
            self.clicked = False
            self.set_curr_frame(0)

        self.move_animation.update()
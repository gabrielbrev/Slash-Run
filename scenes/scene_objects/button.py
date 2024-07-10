from PPlay.sprite import Sprite
from PPlay.mouse import Mouse
from PPlay.window import Window

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation
from core.sound_extra import SoundExtra

from .transition import Transition

class Button(Sprite):
    def __init__(self, mouse: Mouse, image_file, command: callable = None, args: tuple = (), transition: Transition = None, hover_sound: SoundExtra = None, click_sound: SoundExtra = None, fade_sounds = False):
        super().__init__(image_file, 2)
        self.window = GD.get_window()
        self.mouse = mouse
        self.command = command
        self.args = args
        self.clicked = False
        self.hovered = False
        self.transition = transition
        self.x = 0
        self.y = 0

        self.move_animation = MoveAnimation(self, self.x, self.y)

        self.hover_sound = hover_sound
        self.click_sound = click_sound

        self.fade_sounds = fade_sounds

    def move_to(self, x, y, duration_s, animation):
        self.move_animation.move_to(x, y, duration_s, animation)

    def is_clicked(self):
        return self.clicked
    
    def is_hovered(self):
        return self.hovered

    def update(self):
        if self.hover_sound:
            self.hover_sound.update_volume()
        if self.click_sound:
            self.click_sound.update_volume()
        if self.mouse.is_over_object(self):
            if not self.hovered:
                if self.hover_sound:
                    self.hover_sound.play()
            self.set_curr_frame(1)
            self.hovered = True
            if self.mouse.is_button_pressed(1):
                if not self.clicked:
                    if self.fade_sounds:
                        SoundExtra.fade_all(500)
                    if self.click_sound:
                        self.click_sound.play()
                self.clicked = True
                if self.command:
                    if self.transition:
                        self.transition.play_out(self.window)
                    self.command(*self.args)
            else:
                self.clicked = False
        else:
            self.hovered = False
            self.clicked = False
            self.set_curr_frame(0)

        self.move_animation.update()
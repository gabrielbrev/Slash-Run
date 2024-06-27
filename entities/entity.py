from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from utils import Vector
from utils import TimedVariable

from core.global_data import GlobalData as GD

from time import time

class Entity(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.og_pos = Vector(x, y)
        self.x = x
        self.y = y
        self.width = width
        self.height = height

        self.on_air = True
        self.attacking = False

        self.sprite = Sprite("assets/temp.png")
        self.SPRITES = {}
        self.curr_action = ""
        self.sprite_anchor = Vector()

        self.blinking = TimedVariable(False, 0.075)
        self.last_blink_time = time()
        self.total_blinks = 0

        self.alive = True

    def reset(self):
        self.x = self.og_pos.x
        self.y = self.og_pos.y
        self.attacking = False
        self.on_air = True
        self.alive = True

    def is_alive(self):
        return self.alive

    def blink(self, duration_s):
        self.total_blinks = duration_s // self.blinking.get_duration() // 2

    def is_blinking(self):
        return self.blinking.get_value()

    def add_sprite(self, key, image_file, frames, duration = 100, loop = True):
        s = Sprite(image_file, frames)
        s.set_position(self.x, self.y)
        s.set_total_duration(duration)
        s.set_loop(loop)
        self.SPRITES[key] = s

    def get_sprite(self, key) -> Sprite:
        return self.SPRITES[key]

    def set_sprite_anchor(self, x, y):
        # Deslocamento do sprite em relação ao objeto
        self.sprite_anchor = Vector(x, y)

    def set_action(self, key, reset = False, play = True):
        self.sprite = self.SPRITES[key]
        self.sprite.playing = play
        if reset:
            self.sprite.set_curr_frame(self.sprite.initial_frame)
        self.curr_action = key.split("_")[0]

    def get_action(self):
        return self.curr_action   
    
    def set_anchor(self, x, y):
        self.og_pos = Vector(x, y)

    def update_blinking(self):
        if self.total_blinks:
            curr_time = time()
            if curr_time - self.last_blink_time >= self.blinking.get_duration():
                self.blinking.set_value(True)
                self.last_blink_time = curr_time + self.blinking.get_duration()
                self.total_blinks -= 1

    def update_position(self):
        self.sprite.set_position(self.x + self.sprite_anchor.x, self.y + self.sprite_anchor.y)

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_position()

    def update(self):
        self.update_blinking()
        self.update_position()
        if self.alive:
            self.sprite.update()

    def draw(self):
        if not self.blinking.get_value():
            self.sprite.draw()

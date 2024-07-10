from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from utils import Vector
from utils import TimedVariable

from core.global_data import GlobalData as GD
from core.sound_extra import SoundExtra

from time import time
import random

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

        self.sprite = Sprite("assets/sprites/temp/garagofest.jpg")
        self.SPRITES = {}
        self.curr_action = ""
        self.sprite_anchor = Vector()

        self.SOUNDS = {}
        self.muted = False
        self.paused_sounds = []

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
        try:
            s = Sprite(image_file, frames)
        except:
            print(f"Could not load sprite from path: {image_file}")
            s = Sprite("assets/sprites/temp/garagofest.jpg", 1)
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

    def add_sound(self, key, sound_file, volume = 100, loop = False, replace = False):
        # Adicionar mais de um som com a mesma key fará com que eles sejam tocados aleatoriamente (se replace for falso)
        s = SoundExtra(sound_file, "sfx", volume, loop)
        if key not in self.SOUNDS.keys():
            self.SOUNDS[key] = []
        elif replace:
            self.SOUNDS[key].clear()
        self.SOUNDS[key].append(s)

    def get_sound(self, key):
        return self.SOUNDS[key]
    
    def is_sound_playing(self, key):
        for s in self.SOUNDS[key]:
            if s.is_playing():
                return True
        return False

    def play_sound(self, key):
        if not self.muted:
            random.choice(self.SOUNDS[key]).play()

    def pause_sound(self, key):
        for s in self.SOUNDS[key]:
            if s.is_playing():
                s.pause()
                self.paused_sounds.append({
                    "key": key,
                    "sound": s
                })

    def unpause_sound(self, key):
        s = None
        for i in range(len(self.paused_sounds)):
            if self.paused_sounds[i]["key"] == key:
                self.paused_sounds[i]["sound"].unpause()
                s = self.paused_sounds[i]
        if s:
            self.paused_sounds.remove(s)

    def fade_sounds(self, time_ms):
        for s_list in self.SOUNDS.values():
            for s in s_list:
                if s.is_playing():
                    s.fadeout(time_ms)

    def mute(self):
        self.muted = True
        for key, s_list in self.SOUNDS.items():
            for s in s_list:
                if s.is_playing():
                    self.pause_sound(key)

    def unmute(self):
        self.muted = False
        for s in self.paused_sounds:
            self.unpause_sound(s["key"])

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

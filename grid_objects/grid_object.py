from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from core.global_data import GlobalData as GD
from core.sound_extra import SoundExtra

from utils import Vector

import random

class GridObject(GameObject):
    def __init__(self, x, y, cell_size, grid_id, fragile = False):
        super().__init__()
        self.x = x
        self.y = y
        self.og_pos = Vector(x, y)
        self.cell_size = cell_size
        self.grid_id = grid_id
        self.fragile = fragile
        self.destroyed = False
        self.sprite = Sprite("assets/sprites/temp/garagofest.jpg")
        self.sprite.set_total_duration(100)
        self.SPRITES = {}
        self.curr_action = ""
        self.sprite_anchor = Vector()
        self.SOUNDS = {}
        self.muted = False
        self.paused_sounds = []

    def reset(self):
        self.x = self.og_pos.x
        self.y = self.og_pos.y
        self.destroyed = False
        self.sprite.set_curr_frame(0)

    def is_destroyed(self):
        return self.destroyed

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
        if not (self.width or self.height):
            self.width = s.width
            self.height = s.height

    def get_sprite(self, key) -> Sprite:
        return self.SPRITES[key]

    def set_action(self, key, reset = False, play = True):
        self.sprite = self.SPRITES[key]
        self.sprite.playing = play
        if reset:
            self.sprite.set_curr_frame(self.sprite.initial_frame)
        self.curr_action = key.split("_")[0]
    
    def get_action(self):
        return self.curr_action  
    
    def set_sprite_anchor(self, x, y):
        # Deslocamento do sprite em relação ao objeto
        self.sprite_anchor = Vector(x, y)
    
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

    def destroy(self):
        self.destroyed = True

    def update_position(self):
        self.sprite.set_position(self.x + self.sprite_anchor.x, self.y + self.sprite_anchor.y)

    def update(self):
        self.update_position()
        self.sprite.update()

    def draw(self):
        if not self.destroyed:
            self.sprite.draw()
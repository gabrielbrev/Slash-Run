from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from core.global_data import GlobalData as GD

from utils import Vector

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
        self.sprite = Sprite("assets/temp.png")
        self.sprite.set_total_duration(10000)
        self.SPRITES = {}
        self.curr_action = ""

    def reset(self):
        self.x = self.og_pos.x
        self.y = self.og_pos.y
        self.destroyed = False
        self.sprite.set_curr_frame(0)

    def add_sprite(self, key, image_file, frames, duration = 100, loop = True):
        s = Sprite(image_file, frames)
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

    def destroy(self):
        self.destroyed = True

    def update_position(self):
        self.sprite.set_position(self.x, self.y)

    def update(self):
        self.update_position()
        self.sprite.update()

    def draw(self):
        if not self.destroyed:
            self.sprite.draw()
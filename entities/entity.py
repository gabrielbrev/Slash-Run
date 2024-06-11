from PPlay.gameobject import GameObject
from PPlay.sprite import Sprite

class Entity(GameObject):
    def __init__(self, x, y, width, height):
        super().__init__()
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.on_air = True
        self.attacking = False
        self.sprite = Sprite("assets/temp.png")
        self.SPRITES = {}
        self.curr_action = ""

    def add_sprite(self, key, image_file, frames, duration = 100):
        s = Sprite(image_file, frames)
        s.set_total_duration(duration)
        self.SPRITES[key] = s

    def get_sprite(self, key):
        return self.SPRITES[key]

    def set_action(self, key):
        self.sprite = self.SPRITES[key]
        self.curr_action = key.split("_")[0]

    def get_action(self):
        return self.curr_action        

    def move_left(self):
        self.sprite.set_position(self.x, self.y)

    def move_right(self):
        self.sprite.set_position(self.x, self.y)

    def update(self):
        self.sprite.set_position(self.x, self.y)
        self.sprite.update()

    def draw(self):
        self.sprite.draw()
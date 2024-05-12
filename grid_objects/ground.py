from PPlay.sprite import Sprite
from PPlay.window import Window

class Ground(Sprite):
    def __init__(self, window: Window, image_file, frames=1):
        super().__init__(image_file, frames)
        self.window = window
        self.highlight = False
        self.highlight_sprite = Sprite("assets/highlight.png")
        self.highlight_sprite.x = self.x
        self.highlight_sprite.y = self.y

    def update(self):
        self.highlight_sprite.x = self.x
        self.highlight_sprite.y = self.y

    def draw(self):
        if self.highlight:
            self.highlight_sprite.draw()
            self.highlight = False
        else:
            super().draw()
    
        
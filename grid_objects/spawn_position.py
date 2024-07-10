from PPlay.gameobject import GameObject
from PPlay.sprite import Sprite

from .grid_object import GridObject

from core.global_data import GlobalData as GD

class SpawnPos(GridObject):        
    def __init__(self, x, y, cell_size, grid_id, on_editor = False):
        super().__init__(x, y, cell_size, grid_id, False)
        self.width = cell_size
        self.height = cell_size
        self.on_editor = on_editor
        self.sprite = Sprite(f"assets/sprites/grid_objects/highlights/cell{cell_size}.png", 1)
        self.sprite.set_position(x, y)
        self.sprite.set_total_duration(100)

    def update(self):
        if self.on_editor:
            super().update()
    
    def draw(self):
        if self.on_editor:
            size = 20
            name = "spawn pos"
            GD.get_window().draw_text(name, self.x + self.width/2 - size/2 * len(name)/2, self.y + self.height/2 - size/2, size=size, color=(255, 255, 255))
            self.sprite.draw()
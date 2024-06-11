from .grid_entity import GridEntity

class Enemy(GridEntity):
    def __init__(self, x, y, width, height, cell_size, grid_id):
        super().__init__(x, y, width, height, cell_size, grid_id)
        
        self.alive = True
        self.attacked = False # Monsters can only attack once

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def update(self):
        GridEntity.update(self)

    def draw(self):
        if self.alive:
            self.sprite.draw()
from .entity import Entity

class Enemy(Entity):
    def __init__(self, x, y, width, height, cell_size, grid_id):
        super().__init__(x, y, width, height)
        
        self.alive = True
        self.attacked = False # Monsters can only attack once

        # Attibutos da classe GridObject
        self.cell_size = cell_size
        self.grid_id = grid_id

    def is_alive(self):
        return self.alive

    def kill(self):
        self.alive = False

    def update(self):
        Entity.update(self)

    def draw(self):
        if self.alive:
            self.sprite.draw()
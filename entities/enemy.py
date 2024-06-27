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
        self.blink(0.5)

    def attack(self):
        self.attacked = True

    def update(self):
        GridEntity.update(self)

    def draw(self):
        if not self.blinking.get_value():
            if self.alive or self.total_blinks > 0:
                self.sprite.draw()
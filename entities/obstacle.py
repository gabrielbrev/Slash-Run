from .grid_entity import GridEntity

class Obstacle(GridEntity):
    def __init__(self, x, y, width, height, cell_size, grid_id):
        super().__init__(x, y, width, height, cell_size, grid_id)
        self.damaged_player = False
        self.destroyed = False

    def reset(self):
        self.damaged_player = False
        self.destroyed = False
        super().reset()

    def is_destroyed(self):
        return self.destroyed
    
    def destroy(self):
        self.fade_sounds(200)
        self.destroyed = True

    def deal_damage(self):
        self.damaged_player = True

    def draw(self):
        if not self.destroyed:
            super().draw()
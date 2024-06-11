from .entity import Entity

class GridEntity(Entity):
    def __init__(self, x, y, width, height, cell_size, grid_id):
        super().__init__(x, y, width, height)
        self.cell_size = cell_size
        self.grid_id = grid_id

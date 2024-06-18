from .ground import Ground
from .grid_object import GridObject

from core.global_data import GlobalData as GD

class InfiniteGround(GridObject):
    def __init__(self, x, y, cell_size, grid_id, tile_height):
        self.SPECIAL_DATA = ["tile_height"]
        super().__init__(x, y, cell_size, grid_id, False)
        self.tile_height = tile_height

        self.origin_x = x

        self.g1 = Ground(x, y, 4, tile_height, cell_size, grid_id)
        self.g2 = Ground(x + self.g1.width, y, 4, tile_height, cell_size, grid_id)

        self.width = self.g1.width + self.g2.width
        self.height = self.g1.height

        self.grid = GD.get_grid(grid_id)

    def try_move_fowards(self, back: Ground, front: Ground):
        if back.x + back.width < 0:
            back.set_position(
                x=front.x + front.width,
                y=self.y
            )
            self.x = front.x

    def try_move_backwards(self, back: Ground, front: Ground):
        if front.x > GD.get_window().width:
            if back.x - back.width >= self.origin_x + self.grid.x:
                front.set_position(
                    x=back.x - back.width,
                    y=self.y
                )
                self.x = front.x

    def update_position(self):
        if self.g1.x < self.g2.x:
            back = self.g1
            front = self.g2
            
            old_g1_x = self.g1.x
            self.g1.x = self.x
            self.g2.x = self.x + self.g2.width
            delta_x = self.g1.x - old_g1_x
        else:
            back = self.g2
            front = self.g1

            old_g2_x = self.g2.x
            self.g1.x = self.x + self.g1.width
            self.g2.x = self.x
            delta_x = self.g2.x - old_g2_x

        self.g1.update_position()
        self.g2.update_position()

        if delta_x < 0: # Moveu para a esquerda
            self.try_move_fowards(back, front)
        elif delta_x > 0: # Moveu para a direita
            self.try_move_backwards(back, front)                    
    
    def update(self):
        self.update_position()

    def draw(self):
        self.g1.draw()
        self.g2.draw()
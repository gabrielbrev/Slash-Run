from PPlay.sprite import Sprite

from .grid_object import GridObject

from core.global_data import GlobalData as GD

class Ground(GridObject):
    # A ground object is 8 times the cell size
    def __init__(self, x, y, tile_width, tile_height, cell_size, grid_id):
        self.SPECIAL_DATA = ["tile_width", "tile_height"]
        super().__init__(x, y, cell_size, grid_id)
        self.tile_size = cell_size * 8
        self.tile_width = tile_width
        self.tile_height = tile_height
        self.width = tile_width * self.tile_size
        self.height = tile_height * self.tile_size
        self.tile_size = self.tile_size
        self.tiles = []
        for i in range(tile_width):
            tile_list = []
            for j in range(tile_height):
                tile = Sprite(f"assets/terrain/ground{self.tile_size}.jpeg")
                tile.x = x + i * self.tile_size
                tile.y = y + j * self.tile_size
                tile_list.append(tile)
            self.tiles.append(tile_list)
        # self.collapse = False

    def update(self):
        for i, tile_list in enumerate(self.tiles):
            for j, tile in enumerate(tile_list):
                tile.x = self.x + i * self.tile_size
                tile.y = self.y + j * self.tile_size

    def move_left(self):
        self.update()

    def move_right(self):
        self.update()

    def draw(self):
        for tile_list in self.tiles:
            for tile in tile_list:
                if GD.on_screen(tile):
                    tile.draw()
    
        
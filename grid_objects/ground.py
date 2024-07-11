from PPlay.sprite import Sprite
from PPlay.gameimage import GameImage
from PPlay.gameobject import GameObject

from .grid_object import GridObject

from core.global_data import GlobalData as GD

from utils import Vector

from time import time

class GroundSide(GameObject):
    def __init__(self, x, y, type, size) -> None:
        super().__init__()
        self.images = []
        match type:
            case "top_left":
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/left/top_left_border{size}.png")) # borda
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/left/top_left{size}.jpeg")) # resto
            case "center_left":
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/left/center_left_border{size}.png")) # borda
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/left/center_left{size}.jpeg")) # resto
            case "top_right":
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/right/top_right{size}.jpeg")) # resto
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/right/top_right_border{size}.png")) # borda
            case "center_right":
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/right/center_right{size}.jpeg")) # resto
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/right/center_right_border{size}.png")) # borda
            case "top_single":
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/single/top_single_l_border{size}.png")) # borda esq
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/single/top_single{size}.jpeg")) # meio
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/single/top_single_r_border{size}.png")) # borda dir
            case "center_single":
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/single/center_single_l_border{size}.png")) # borda esq
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/single/center_single{size}.jpeg")) # meio
                self.images.append(GameImage(f"assets/sprites/grid_objects/ground/sides/single/center_single_r_border{size}.png")) # borda dir
            case _:
                raise ValueError("type is not valid")

        self.width = size
        self.height = size
        self.update_position(x, y)

    def update_position(self, x, y):
        self.x = x
        self.y = y
        for i in range(len(self.images)):
            image = self.images[i]
            image.y = y
            if i == 0:
                self.x = x
                image.x = x
            else:
                image_before = self.images[i - 1]
                image.x = image_before.x + image_before.width

    def draw(self):
        for i in self.images:
            i.draw()

class Ground(GridObject):
    GRAVITY = 500

    # A ground object is 8 times the cell size
    def __init__(self, x, y, tile_width, tile_height, cell_size, grid_id, infinite=False):
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
                file_format = "png"
                if infinite:
                    if j == 0:
                        name = "top_mid"
                        file_format = "jpeg"
                    else:
                        name = "center_mid"
                        file_format = "jpeg"
                else:
                    if i == tile_width - 1 == 0:
                        if j == 0:
                            name = "top_single"
                        else:
                            name = "center_single"
                    elif i == 0:
                        if j == 0:
                            name = "top_left"
                        else:
                            name = "center_left"
                    elif i == tile_width - 1:
                        if j == 0:
                            name = "top_right"
                        else:
                            name = "center_right"
                    else:
                        if j == 0:
                            name = "top_mid"
                            file_format = "jpeg"

                        else:
                            name = "center_mid"
                            file_format = "jpeg"

                if "mid" in name:
                    tile = GameImage(f"assets/sprites/grid_objects/ground/{name}{self.tile_size}.{file_format}")
                    tile.x = x + i * self.tile_size
                    tile.y = y + j * self.tile_size
                else:
                    tile = GroundSide(x + i * self.tile_size, y + j * self.tile_size, name, self.tile_size)
                tile_list.append(tile)
            self.tiles.append(tile_list)

        self.collapsing = False
        self.speed = Vector(0, 0)

    def collapse(self):
        self.collapsing = True
        self.speed.y += 15

    def update_position(self):
        for i, tile_list in enumerate(self.tiles):
            for j, tile in enumerate(tile_list):
                new_x = self.x + i * self.tile_size
                new_y = self.y + j * self.tile_size
                if isinstance(tile, GroundSide):
                    tile.update_position(new_x, new_y)
                else:
                    tile.x = new_x
                    tile.y = new_y

    def set_position(self, x, y):
        self.x = x
        self.y = y
        self.update_position()

    def increase_width(self):
        self.tile_width += 1
        self.width += self.tile_size
        tile_list = []
        for i in range(self.tile_height):
            if i == 0:
                name = "top_mid"
            else:
                name = "center_mid"
            tile = GameImage(f"assets/sprites/grid_objects/ground/{name}{self.tile_size}.jpeg")
            tile_list.append(tile)
        self.tiles.insert(-1, tile_list)

    def update(self):
        self.y += self.speed.y * GD.get_window().delta_time()
        if self.collapsing:
            self.speed.y += Ground.GRAVITY * GD.get_window().delta_time()

        self.update_position()

    def draw(self):
        for tile_list in self.tiles:
            for tile in tile_list:
                match GD.off_screen(tile):
                    case 0:
                        tile.draw()
                    case 1:
                        break
    
        
from PPlay.window import Window
from PPlay.gameobject import GameObject

from grid_objects.air import Air
from grid_objects.ground import Ground
from grid_objects.extense_object import ExtenseObject
from utils import ScreenUtils
from entities.player import Player

import json

class Grid(GameObject):
    def __init__(self, window: Window, width, height, speed, cell_size, active = True, draw_grid = False) -> None:
        super().__init__()
        self.window = window
        self.matrix = [[None for _ in range(height)] for _ in range(width)]
        self.cell_size = cell_size
        self.x = 0
        self.y = window.height - (height * cell_size) # Ultima linha fica alinhada ao chão da janela
        self.width = width
        self.height = height
        self.speed = speed
        self.draw_grid = draw_grid
        self.active = active
        self.screen = ScreenUtils(window)

    def load_terrain(self, obj_list, obj_class, sprite_path):
        for obj in obj_list:
            x = obj["x"]
            y = obj["y"]
            width = obj["width"]
            height = obj["height"]

            obj = ExtenseObject(
                window=self.window, 
                x=self.x + x * self.cell_size, 
                y=self.y + (self.height - 1 - y) * self.cell_size,
                width=width, 
                height=height,
                cell_size=self.cell_size,
                type=obj_class,
                args=(self.window, sprite_path)
            )
            self.matrix[x][y] = obj

    def load_level(self, file_path):
        with open(file_path, "r") as json_file:
            level: dict = json.load(json_file)
        for key in level.keys():
            if key == "Air" and self.draw_grid:
                self.load_terrain(level[key], Air, "assets/terrain/air.png")
            elif key == "Ground":
                self.load_terrain(level[key], Ground, "assets/terrain/ground.png")

    def update(self, player: Player):
        self.x -= self.speed * self.window.delta_time()
        for obj_list in self.matrix:
            for j, obj in enumerate(obj_list):
                if obj:
                    obj.x -= self.speed * self.window.delta_time()
                    if self.screen.on_screen(obj):
                        obj.update(player)

    def draw(self):
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    if self.screen.on_screen(obj):
                        obj.draw()
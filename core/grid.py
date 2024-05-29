from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.gameobject import GameObject

from grid_objects.air import Air
from grid_objects.ground import Ground
from grid_objects.energy_orb import EnergyOrb
from entities.attacker import Attacker
from common import GlobalData as GD

import json

class Grid(GameObject):
    def __init__(self, width, height, speed, cell_size, active = True, draw_grid = False) -> None:
        super().__init__()
        self.matrix = [[None for _ in range(height)] for _ in range(width)]
        self.cell_size = cell_size
        self.x = 0
        self.y = GD.get_window().height - (height * cell_size) # Ultima linha fica alinhada ao chão da janela
        self.width = width
        self.height = height
        self.speed = speed
        self.draw_grid = draw_grid
        self.active = active # Determina se o player está em seu plano ou não

    def load_ground(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            width = item["width"]
            height = item["height"]
            self.matrix[x][y] = Ground(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                width=width, 
                height=height,
                tile_size=self.cell_size * 8,
                cell_size=self.cell_size,
                active=self.active
            )

    def load_air(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            width = item["width"]
            height = item["height"]
            self.matrix[x][y] = Air(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                width=width, 
                height=height,
                tile_size=self.cell_size,
                active=self.active
            )

    def load_energy_orbs(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            self.matrix[x][y] = EnergyOrb(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                cell_size=self.cell_size,
                active=self.active
            )

    def load_entities(self, obj_list, entity_type: callable):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            self.matrix[x][y] = entity_type(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                cell_size=self.cell_size,
                active=self.active
            )

    def load_level(self, file_path):
        with open(file_path, "r") as json_file:
            level: dict = json.load(json_file)
        if self.draw_grid:
            self.load_air([{"x": 0, "y": self.height - 1, "width": self.width, "height": self.height}])
        for key in level.keys():
            if key == "Ground":
                self.load_ground(level[key])
            elif key == "EnergyOrb":
                self.load_energy_orbs(level[key])
            elif key == "Attacker":
                self.load_entities(level[key], Attacker)

    def activate(self):
        self.active = True
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.active = True

    def deactivate(self):
        self.active = False
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.active = False

    def update(self):
        self.x -= self.speed * GD.get_window().delta_time()
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x -= self.speed * GD.get_window().delta_time()
                    if GD.on_screen(obj):
                        obj.update()
            
    def draw(self):
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    if GD.on_screen(obj, append_to_list=True):
                        obj.draw()
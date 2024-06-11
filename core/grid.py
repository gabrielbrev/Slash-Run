from PPlay.gameobject import GameObject

from .global_data import GlobalData as GD

from grid_objects.ground import Ground
from grid_objects.energy_orb import EnergyOrb

from entities.attacker import Attacker
from entities.boulder import Boulder

from common import Multipliable

import json

class Grid(GameObject):
    next_id = 1
    def get_id():
        id = Grid.next_id
        Grid.next_id += 1
        return id

    def __init__(self, width, height, speed, cell_size, speed_multipliers: list = [1]) -> None:
        super().__init__()
        self.matrix = [[None for _ in range(height)] for _ in range(width)]
        self.cell_size = cell_size
        self.x = 0
        self.delta_x = 0 # Serve para terceiros verificarem se houve movimento no editor
        self.y = GD.get_window().height - (height * cell_size) # Ultima linha fica alinhada ao chão da janela
        self.width = width
        self.height = height
        self.speed = Multipliable(speed, speed_multipliers)
        self.id = Grid.get_id() # Determina se o player está em seu plano ou não

    def translate_coordinates(self, x, y):
        new_x = self.x + x * self.cell_size
        new_y = self.y + (self.height - 1 - y) * self.cell_size
        return new_x, new_y
    
    def raise_speed(self):
        self.speed.raise_multiplier()
    
    def lower_speed(self):
        self.speed.lower_multiplier()

    def load_ground(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            tile_width = item["tile_width"]
            tile_height = item["tile_height"]
            self.matrix[x][y] = Ground(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                tile_width=tile_width, 
                tile_height=tile_height,
                cell_size=self.cell_size,
                grid_id=self.id
            )

    def load_energy_orbs(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            self.matrix[x][y] = EnergyOrb(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                cell_size=self.cell_size,
                grid_id=self.id
            )

    def load_attackers(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            self.matrix[x][y] = Attacker(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                cell_size=self.cell_size,
                grid_id=self.id
            )

    def load_boulders(self, obj_list):
        for item in obj_list:
            x = item["x"]
            y = item["y"]
            self.matrix[x][y] = Boulder(
                x=self.x + x * self.cell_size,
                y=self.y + (self.height - 1 - y) * self.cell_size,
                cell_size=self.cell_size,
                grid_id=self.id,
                fragile=item["fragile"]
            )

    def load_level(self, file_path):
        with open(file_path, "r") as json_file:
            level: dict = json.load(json_file)
        for key in level.keys():
            if key == "Ground":
                self.load_ground(level[key])
            elif key == "EnergyOrb":
                self.load_energy_orbs(level[key])
            elif key == "Attacker":
                self.load_attackers(level[key])
            elif key == "Boulder":
                self.load_boulders(level[key])

    def move_right(self):
        old_x = self.x
        self.x += self.speed.get_value() * GD.get_window().delta_time()
        if self.x > 0:
            self.x = 0
        self.delta_x = self.x - old_x
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x += self.delta_x
                    obj.move_right()
        if self.delta_x:
            return 1
        return 0

    def move_left(self):
        old_x = self.x
        self.x -= self.speed.get_value() * GD.get_window().delta_time()
        # Movimento para esquerda não é limitado no fim do grid pois o desalinha com do outro
        self.delta_x = self.x - old_x
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x += self.delta_x
                    obj.move_left()

    def update(self):
        self.x -= self.speed.get_value() * GD.get_window().delta_time()
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x -= self.speed.get_value() * GD.get_window().delta_time()
                    if GD.on_screen(obj):
                        obj.update()
            
    def draw(self):
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    if GD.on_screen(obj, append_to_list=True):
                        obj.draw()
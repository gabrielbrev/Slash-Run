from PPlay.gameobject import GameObject

from .global_data import GlobalData as GD

from grid_objects.ground import Ground
from grid_objects.energy_orb import EnergyOrb
from grid_objects.geyser import Geyser
from grid_objects.spawn_position import SpawnPos
from grid_objects.infinite_ground import InfiniteGround
from grid_objects.end_trigger import EndTrigger

from entities.attacker import Attacker
from entities.boulder import Boulder
from entities.destroyer import Destroyer
from entities.flyer import Flyer
from entities.entity import Entity

from utils import Multipliable

import json

class Grid(GameObject):
    next_id = 1
    def get_id():
        id = Grid.next_id
        Grid.next_id += 1
        return id

    def __init__(self, width, height, cell_size, speed: Multipliable, on_editor = False) -> None:
        super().__init__()
        self.matrix = [[None for _ in range(height)] for _ in range(width)]
        self.cell_size = cell_size
        self.x = 0
        self.delta_x = 0 # Serve para terceiros verificarem se houve movimento no editor
        self.y = GD.get_window().height - (height * cell_size) # Ultima linha fica alinhada ao chão da janela
        self.width = width
        self.height = height
        self.speed = speed
        self.id = Grid.get_id() # Determina se o player está em seu plano ou não
        self.on_editor = on_editor
        self.spawn_position = None
        GD.add_grid(self)

    def __close__(self):
        GD.remove_grid(self.id)

    def translate_coordinates(self, x, y):
        new_x = self.x + x * self.cell_size
        new_y = self.y + (self.height - 1 - y) * self.cell_size
        return new_x, new_y
    
    def raise_speed(self):
        self.speed.raise_multiplier()
    
    def lower_speed(self):
        self.speed.lower_multiplier()

    def load_ground(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            tile_width = item["tile_width"]
            tile_height = item["tile_height"]
            self.matrix[i][j] = Ground(
                x=x,
                y=y,
                tile_width=tile_width, 
                tile_height=tile_height,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded ground {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_infinite_ground(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            tile_height = item["tile_height"]
            self.matrix[i][j] = InfiniteGround(
                x=x,
                y=y,
                tile_height=tile_height,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded infinite ground {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_geysers(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = Geyser(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded geyser {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_energy_orbs(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = EnergyOrb(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded energy orb {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_attackers(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = Attacker(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded attacker {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_destroyers(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = Destroyer(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded destroyer {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")
    
    def load_flyers(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = Flyer(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id
            )
            print(f"Loaded flyer {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_boulders(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = Boulder(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id,
                fragile=item["fragile"]
            )
            print(f"Loaded boulder {index}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_spawn_positions(self, obj_list):
        for index, item in enumerate(obj_list):
            i = item["x"]
            j = item["y"]
            x, y = self.translate_coordinates(i, j)
            self.matrix[i][j] = self.spawn_position = SpawnPos(
                x=x,
                y=y,
                cell_size=self.cell_size,
                grid_id=self.id,
                on_editor=self.on_editor
            )
            print(f"Loaded spawn position {index + 1}/{len(obj_list)} at ({i}, {j}) in grid {self.id}")

    def load_end_trigger(self, obj_list):
        item = obj_list[0]
        i = item["x"]
        j = item["y"]
        x, y = self.translate_coordinates(i, j)
        self.matrix[i][j] = EndTrigger(
            x=x,
            cell_size=self.cell_size,
            grid_id=self.id,
            on_editor=self.on_editor
        )
        print(f"Loaded end trigger at ({i}, {j}) in grid {self.id}")
        
    def load_level(self, file_path):
        with open(file_path, "r") as json_file:
            level: dict = json.load(json_file)
        for key in level.keys():
            match key:
                case "Ground":
                    self.load_ground(level[key])
                case "InfiniteGround":
                    self.load_infinite_ground(level[key])
                case "Geyser":
                    self.load_geysers(level[key])
                case "EnergyOrb":
                    self.load_energy_orbs(level[key])
                case "Attacker":
                    self.load_attackers(level[key])
                case "Boulder":
                    self.load_boulders(level[key])
                case "Destroyer":
                    self.load_destroyers(level[key])
                case "Flyer":
                    self.load_flyers(level[key])
                case "SpawnPos":
                    self.load_spawn_positions(level[key])
                case "EndTrigger":
                    self.load_end_trigger(level[key])

    def get_spawn_position(self):
        if self.spawn_position:
            return self.spawn_position.x, self.spawn_position.y
        return None
    
    def get_inf_ground_y(self):
        inf_ground = None
        for obj_list in self.matrix:
            if inf_ground:
                break
            for obj in obj_list:
                if isinstance(obj, InfiniteGround):
                    inf_ground = obj
                    break
        if inf_ground:
            return inf_ground.y
        return None

    def move(self, amount):
        self.x += amount
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x += amount
                    obj.update_position()

    def move_left(self):
        amount = self.speed.get_value() * GD.get_window().delta_time()
        self.move(-amount)

    def move_right(self):
        amount = self.speed.get_value() * GD.get_window().delta_time()
        if self.x + amount > 0:
            amount = -self.x
        if amount:
            self.move(amount)

    def update_x_position(self, delta_x):
        self.x += delta_x
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x += delta_x

    def update(self):
        if GD.is_game_over():
            self.speed.set_value(0)
        self.x -= self.speed.get_value() * GD.get_window().delta_time()
        for obj_list in self.matrix:
            for obj in obj_list:
                if obj:
                    obj.x -= self.speed.get_value() * GD.get_window().delta_time()
                    if isinstance(obj, Entity):
                        if GD.on_update_range(obj):
                            obj.update()
                    else:
                        if GD.on_screen(obj, append_to_list=True):
                            obj.update()
            
    def draw(self):
        for obj_list in self.matrix:
            for i, obj in enumerate(obj_list):
                if obj:
                    match GD.off_screen(obj, append_to_list=True):
                        case -1:
                            if not self.on_editor:
                                obj_list[i] = None
                        case 0:
                            obj.draw()
                        case 1:
                            break
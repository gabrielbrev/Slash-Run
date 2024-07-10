from PPlay.gameobject import GameObject

from .global_data import GlobalData as GD

from grid_objects.ground import Ground
from grid_objects.energy_orb import EnergyOrb
from grid_objects.geyser import Geyser
from grid_objects.spawn_position import SpawnPos
from grid_objects.infinite_ground import InfiniteGround
from grid_objects.end_trigger import EndTrigger
from grid_objects.spike import Spike

from entities.attacker import Attacker
from entities.boulder import Boulder
from entities.destroyer import Destroyer
from entities.flyer import Flyer
from entities.entity import Entity

from utils import Multipliable

import json
from time import time

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
        for item in obj_list:
            try:
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
            except Exception as e:
                print(f"Could not load ground {item}. Reason: {e}")

    def load_infinite_ground(self, obj_list):
        for item in obj_list:
            try:
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
            except Exception as e:
                print(f"Could not load infinite ground {item}. Reason: {e}")

    def load_geysers(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = Geyser(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id
                )
            except Exception as e:
                print(f"Could not load geyser {item}. Reason: {e}")
    
    def load_spikes(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = Spike(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id
                )
            except Exception as e:
                print(f"Could not load spike {item}. Reason: {e}")

    def load_energy_orbs(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = EnergyOrb(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id
                )
            except Exception as e:
                print(f"Could not load energy orb {item}. Reason: {e}")

    def load_attackers(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = Attacker(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id
                )
            except Exception as e:
                print(f"Could not load attacker {item}. Reason: {e}")

    def load_destroyers(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = Destroyer(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id
                )
            except Exception as e:
                print(f"Could not load destroyer {item}. Reason: {e}")
    
    def load_flyers(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = Flyer(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id
                )
            except Exception as e:
                print(f"Could not load flyer {item}. Reason: {e}")

    def load_boulders(self, obj_list):
        for item in obj_list:
            try:
                i = item["x"]
                j = item["y"]
                x, y = self.translate_coordinates(i, j)
                self.matrix[i][j] = Boulder(
                    x=x,
                    y=y,
                    cell_size=self.cell_size,
                    grid_id=self.id,
                )
            except Exception as e:
                print(f"Could not load boulder {item}. Reason: {e}")

    def load_spawn_positions(self, obj_list):
        for item in obj_list:
            try:
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
            except Exception as e:
                print(f"Could not load spawn position {item}. Reason: {e}")

    def load_end_trigger(self, obj_list):
        try:
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
        except Exception as e:
            print(f"Could not load end trigger {item}. Reason: {e}")
        
    def load_level(self, file_path):
        print(f"LOADING GRID {self.id}")
        try:
            with open(file_path, "r") as json_file:
                level: dict = json.load(json_file)
        except FileNotFoundError:
            with open(file_path, "w") as json_file:
                level: dict = {}
                json.dumps(level, json_file)
        for key in level.keys():
            start_time = time()
            match key:
                case "Ground":
                    self.load_ground(level[key])
                case "InfiniteGround":
                    self.load_infinite_ground(level[key])
                case "Geyser":
                    self.load_geysers(level[key])
                case "Spike":
                    self.load_spikes(level[key])
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
    
            print(f"Loaded {key}(s) in {(time() - start_time):.2f}")
        print()

    def mute(self):
        for obj_list in self.matrix:
            broke_loop = False
            for obj in obj_list:
                if obj:
                    if GD.off_screen(obj) > 0:
                        broke_loop = True
                        break
                    obj.mute()
            if broke_loop:
                break
    
    def unmute(self):
        for obj_list in self.matrix:
            broke_loop = False
            for obj in obj_list:
                if obj:
                    if GD.off_screen(obj) > 0:
                        broke_loop = True
                        break
                    obj.unmute()
            if broke_loop:
                break

    def fade_sounds(self, time_ms):
        for obj_list in self.matrix:
            broke_loop = False
            for obj in obj_list:
                if obj:
                    if GD.off_screen(obj) > 0:
                        broke_loop = True
                        break
                    obj.fade_sounds(time_ms)
            if broke_loop:
                break

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
                    match GD.off_screen(obj, append_to_list=True, test_sprite=True):
                        case -1:
                            if not self.on_editor:
                                obj.fade_sounds(200)
                                obj_list[i] = None
                        case 0:
                            obj.draw()
                        case 1:
                            break
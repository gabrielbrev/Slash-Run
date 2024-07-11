from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from .grid import Grid
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

from utils import TimedVariable, convert_seconds

import json
from time import time

class GridEditor:
    OBJ_CLASSES = [Ground, InfiniteGround, Geyser, Spike, EnergyOrb, Attacker, Destroyer, Flyer, Boulder, SpawnPos, EndTrigger]

    def __init__(self, mouse: Mouse, front_grid: Grid, back_grid: Grid) -> None:
        self.mouse = mouse
        self.fg = front_grid
        self.bg = back_grid
        self.grid = front_grid
        self.highlight = Sprite(f"assets/sprites/grid_objects/highlights/cell{self.grid.cell_size}.png")
        self.hovering = None
        self.matrix_x = 0
        self.matrix_y = 0
        self.undo_list = []
        self.redo_list = []
        self.new_obj_index = len(GridEditor.OBJ_CLASSES) - 1
        self.cycle_object()
        self.has_changes = False
        self.message = TimedVariable("", 10)
        self.level_duration = 0
        self.update_cooldown = 10
        self.last_update_time = 0

    def switch_grid(self):
        if self.grid == self.fg:
            self.grid = self.bg
        else:
            self.grid = self.fg
        self.highlight = Sprite(f"assets/sprites/grid_objects/highlights/cell{self.grid.cell_size}.png")
    
    def add_undo(self, curr_obj, new_obj, x, y, grid_id, copy_coords = False):
        data = {
            "grid_id": grid_id,
            "curr_obj": curr_obj,
            "new_obj": new_obj,
            "x": x,
            "y": y,
            "copy_coords": copy_coords
        }
        self.undo_list.append(data)
        if len(self.undo_list) > 100:
            self.undo_list.pop(0)

    def add_redo(self, curr_obj, new_obj, x, y, grid_id, copy_coords = False):
        data = {
            "grid_id": grid_id,
            "curr_obj": curr_obj,
            "new_obj": new_obj,
            "x": x,
            "y": y,
            "copy_coords": copy_coords
        }
        self.redo_list.append(data)
        if len(self.redo_list) > 100:
            self.redo_list.pop(0)

    def empty_redo(self):
        self.redo_list.clear()

    def undo(self):
        self.has_changes = True
        if len(self.undo_list) > 0:
            data = self.undo_list[-1]
            grid = self.fg if self.fg.id == data["grid_id"] else self.bg
            curr_obj = data["curr_obj"]
            new_obj = data["new_obj"]
            x = data["x"]
            y = data["y"]
            self.add_redo(new_obj, curr_obj, x, y, data["grid_id"])
            grid.matrix[x][y] = curr_obj
            if data["copy_coords"]:
                curr_obj.x = new_obj.x
                curr_obj.y = new_obj.y
            self.undo_list.pop(-1)
            GD.remove_screen_obj(new_obj)
            if curr_obj:
                curr_obj.update_position()

    def redo(self):
        self.has_changes = True
        if len(self.redo_list) > 0:
            data = self.redo_list[-1]
            grid = self.fg if self.fg.id == data["grid_id"] else self.bg
            curr_obj = data["curr_obj"]
            new_obj = data["new_obj"]
            x = data["x"]
            y = data["y"]
            self.add_undo(new_obj, curr_obj, x, y, data["grid_id"])
            grid.matrix[x][y] = curr_obj
            if data["copy_coords"]:
                curr_obj.x = new_obj.x
                curr_obj.y = new_obj.y
            self.redo_list.pop(-1)
            GD.remove_screen_obj(new_obj)
            if curr_obj:
                curr_obj.update_position()

    def get_hovered_object(self) -> GameObject:
        try:
            hovered_obj = self.grid.matrix[self.matrix_x][self.matrix_y]
        except:
            hovered_obj = None

        # Caso a seleção nao esteja sobre nenhum objeto, checa a colisao com objetos extensos, que ocupam mais de uma célula quando renderizados
        if not hovered_obj:
            for obj in GD.get_screen_objs("All"):
                if (obj.grid_id == self.grid.id or obj.grid_id == -1) and self.highlight.collided(obj):
                    if (isinstance(obj, Ground) 
                        or isinstance(obj, EndTrigger)
                        or isinstance(obj, InfiniteGround)):
                        hovered_obj = obj
                        break

        return hovered_obj
    
    def get_hovered_object_name(self):
        if self.hovering:
            return self.hovering.__class__.__name__
        return "None"
    
    def get_new_object_name(self):
        return GridEditor.OBJ_CLASSES[self.new_obj_index].__name__
    
    def get_message(self):
        return self.message.get_value()
    
    def get_level_duration(self):
        return self.level_duration

    def create_properties_json(self):
        match self.get_new_object_name():
            case "Ground":
                properties = {
                    "tile_width": 1,
                    "tile_height": 1
                }
            case "InfiniteGround":
                properties = {
                    "tile_height": 1
                }
            case _:
                properties = {}

        with open("obj_properties.json", "w") as json_file:
            json.dump(properties, json_file, indent=4)

    def cycle_object(self, backwards = False):
        self.new_obj_index += (-1 if backwards else 1)
        if self.new_obj_index == len(GridEditor.OBJ_CLASSES):
            self.new_obj_index = 0
        elif self.new_obj_index == -1:
            self.new_obj_index = len(GridEditor.OBJ_CLASSES) - 1

        self.create_properties_json()

    def create_object(self, class_name):
        try:
            with open("obj_properties.json", "r") as json_file:
                properties = json.load(json_file)
            x, y = self.grid.translate_coordinates(self.matrix_x, self.matrix_y)
            match class_name:
                case "Ground":
                    self.message.set_value("Place another on top of this to increase it's width")
                    obj = Ground(
                        x=x,
                        y=y,
                        tile_width=properties["tile_width"],
                        tile_height=properties["tile_height"],
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "InfiniteGround":
                    obj = InfiniteGround(
                        x=x,
                        y=y,
                        tile_height=properties["tile_height"],
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "Attacker":
                    obj = Attacker(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "Destroyer":
                    obj = Destroyer(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "Flyer":
                    obj = Flyer(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "Boulder":
                    obj = Boulder(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id,
                    )
                case "EnergyOrb":
                    obj = EnergyOrb(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "Geyser":
                    obj = Geyser(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "Spike":
                    obj = Spike(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
                case "SpawnPos":
                    obj = SpawnPos(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id,
                        on_editor=True
                    )
                case "EndTrigger":
                    obj = EndTrigger(
                        x=x,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id,
                        on_editor=True
                    )
            return obj
        except Exception as e:
            print(e)
            self.message.set_value("Houve um erro ao tentar instanciar o novo objeto")

    def change_ground_width(self, amount = 1):
        curr_obj: Ground = self.hovering
        matrix_x = matrix_y = 0
        found_obj = False
        for i in range(len(self.grid.matrix)):
            for j in range(len(self.grid.matrix[i])):
                if self.grid.matrix[i][j] == curr_obj:
                    found_obj = True
                    matrix_x = i
                    matrix_y = j
                    break
            if found_obj:
                break
        x, y = self.grid.translate_coordinates(matrix_x, matrix_y)
        new_obj = Ground(
            x=x,
            y=y,
            tile_width=curr_obj.tile_width + amount,
            tile_height=curr_obj.tile_height,
            cell_size=curr_obj.cell_size,
            grid_id=curr_obj.grid_id
        )
        self.add_undo(curr_obj, new_obj, matrix_x, matrix_y, self.grid.id, True)
        self.grid.matrix[matrix_x][matrix_y] = new_obj
        GD.remove_screen_obj(curr_obj)
        new_obj.update_position()

    def place_object(self):
        if 0 <= self.matrix_x < self.grid.width and 0 <= self.matrix_y < self.grid.height:
            self.has_changes = True
            if isinstance(self.hovering, Ground) and self.get_new_object_name() == "Ground":
                self.change_ground_width()
            else:
                curr_obj = self.grid.matrix[self.matrix_x][self.matrix_y]
                new_obj = self.create_object(self.get_new_object_name())
                if new_obj:
                    self.add_undo(curr_obj, new_obj, self.matrix_x, self.matrix_y, self.grid.id)
                    self.grid.matrix[self.matrix_x][self.matrix_y] = new_obj
                    if curr_obj:
                        GD.remove_screen_obj(curr_obj)

                    new_obj.update_position()
                print(f"Placed new {new_obj.__class__.__name__} at ({self.matrix_x}, {self.matrix_y})")
            self.empty_redo()

    def delete_hovered_object(self):
        if 0 <= self.matrix_x < self.grid.width and 0 <= self.matrix_y < self.grid.height:
            self.has_changes = True
            if isinstance(self.hovering, Ground) and self.hovering.tile_width > 1:
                self.change_ground_width(-1)
            else:
                self.add_undo(self.hovering, None, self.matrix_x, self.matrix_y, self.grid.id)
                if self.grid.matrix[self.matrix_x][self.matrix_y]:
                    self.grid.matrix[self.matrix_x][self.matrix_y] = None
                else:
                    for obj_list in self.grid.matrix:
                        if self.hovering in obj_list:
                            obj_list[obj_list.index(self.hovering)] = None
                            break
                if self.hovering:
                    GD.remove_screen_obj(self.hovering)
                print(f"Deleted object at ({self.matrix_x}, {self.matrix_y})")
            self.empty_redo()

    def is_saved(self):
        return not self.has_changes

    def convert_matrix_to_dict(self, grid: Grid):
        grid_data = {}
        for i, obj_list in enumerate(grid.matrix):
            for j, obj in enumerate(obj_list):
                if obj:
                    obj_data = {}
                    obj_data["x"] = i
                    obj_data["y"] = j
                    if hasattr(obj, "SPECIAL_DATA"):
                        special_data = obj.SPECIAL_DATA
                        for attr in special_data:
                            obj_data[attr] = getattr(obj, attr)
                    else:
                        pass
                    class_name = obj.__class__.__name__
                    if class_name not in grid_data.keys():
                        grid_data[class_name] = []
                    grid_data[class_name].append(obj_data)
        return grid_data


    def save_changes(self, folder_path):
        fg_data = self.convert_matrix_to_dict(self.fg)
        bg_data = self.convert_matrix_to_dict(self.bg)

        try:
            with open(folder_path + "/front.json", "w") as json_file:
                json.dump(fg_data, json_file, indent=4)
            with open(folder_path + "/back.json", "w") as json_file:
                json.dump(bg_data, json_file, indent=4)
            self.has_changes = False
            return 0
        except:
            return -1

    def update(self):
        if self.mouse.delta_movement():
            mouse_x, mouse_y = self.mouse.get_position()

            self.matrix_x = int((mouse_x - self.grid.x) / self.grid.cell_size)
            self.matrix_y = self.grid.height - 1 - int((mouse_y - self.grid.y) / self.grid.cell_size)

            cell_x = self.matrix_x * self.grid.cell_size + self.grid.x
            cell_y = (self.grid.height - 1 - self.matrix_y) * self.grid.cell_size + self.grid.y

            self.highlight.set_position(cell_x, cell_y)

            self.hovering = self.get_hovered_object()
        
        if time() - self.last_update_time >= self.update_cooldown:
            self.last_update_time = time()
            self.level_duration = convert_seconds(abs(self.fg.x) / self.fg.speed.get_default_value())

    def draw(self):
        if self.highlight.x < self.grid.x + self.grid.width * self.grid.cell_size:
            self.highlight.draw()
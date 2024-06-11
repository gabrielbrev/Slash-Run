from PPlay.mouse import Mouse
from PPlay.sprite import Sprite
from PPlay.gameobject import GameObject

from .grid import Grid
from .global_data import GlobalData as GD

from grid_objects.ground import Ground
from grid_objects.energy_orb import EnergyOrb

from entities.attacker import Attacker
from entities.boulder import Boulder

from common import TimedVariable

import json

class GridEditor:
    OBJ_CLASSES = [Ground, EnergyOrb, Attacker, Boulder]

    def __init__(self, mouse: Mouse, front_grid: Grid, back_grid: Grid) -> None:
        self.mouse = mouse
        self.fg = front_grid
        self.bg = back_grid
        self.grid = front_grid
        self.highlight = Sprite(f"assets/highlight{self.grid.cell_size}.png")
        self.hovering = None
        self.matrix_x = 0
        self.matrix_y = 0
        self.undo_list = []
        self.redo_list = []
        self.new_obj_index = len(GridEditor.OBJ_CLASSES) - 1
        self.cycle_object()
        self.has_changes = True
        self.message = TimedVariable("", 10)

    def switch_grid(self):
        if self.grid == self.fg:
            self.grid = self.bg
        else:
            self.grid = self.fg
        self.highlight = Sprite(f"assets/highlight{self.grid.cell_size}.png")
    
    def add_undo(self, curr_obj, new_obj, x, y, grid_id):
        data = {
            "grid_id": grid_id,
            "curr_obj": curr_obj,
            "new_obj": new_obj,
            "x": x,
            "y": y
        }
        self.undo_list.append(data)
        if len(self.undo_list) > 100:
            self.undo_list.pop(0)

    def add_redo(self, curr_obj, new_obj, x, y, grid_id):
        data = {
            "grid_id": grid_id,
            "curr_obj": curr_obj,
            "new_obj": new_obj,
            "x": x,
            "y": y
        }
        self.redo_list.append(data)
        if len(self.redo_list) > 100:
            self.redo_list.pop(0)

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
            self.undo_list.pop(-1)

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
            self.redo_list.pop(-1)

    def get_hovered_object(self) -> GameObject:
        try:
            hovered_obj = self.grid.matrix[self.matrix_x][self.matrix_y]
        except:
            hovered_obj = None

        # Caso a seleção nao esteja sobre nenhum objeto, checa a colisao com objetos extensos, que sao "chatos de achar" na matriz
        if not hovered_obj:
            for obj in GD.get_screen_objs():
                if obj.grid_id == self.grid.id and isinstance(obj, Ground) and self.highlight.collided(obj):
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

    def create_properties_json(self):
        match self.get_new_object_name():
            case "Ground":
                properties = {
                    "tile_width": 1,
                    "tile_height": 1
                }
            case "Boulder":
                properties = {
                    "fragile": False
                }
            case _:
                properties = {}

        with open("new_item_properties.json", "w") as json_file:
            json.dump(properties, json_file, indent=4)

    def cycle_object(self, backwards = False):
        self.new_obj_index += (-1 if backwards else 1)
        if self.new_obj_index == len(GridEditor.OBJ_CLASSES):
            self.new_obj_index = 0
        elif self.new_obj_index == -1:
            self.new_obj_index = len(GridEditor.OBJ_CLASSES) - 1

        self.create_properties_json()

    def create_object(self, class_name):
        x, y = self.grid.translate_coordinates(self.matrix_x, self.matrix_y)
        try:
            with open("new_item_properties.json", "r") as json_file:
                properties = json.load(json_file)
            match class_name:
                case "Ground":
                    obj = Ground(
                        x=x,
                        y=y,
                        tile_width=properties["tile_width"],
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
                case "Boulder":
                    obj = Boulder(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id,
                        fragile=properties["fragile"]
                    )
                case "EnergyOrb":
                    obj = EnergyOrb(
                        x=x,
                        y=y,
                        cell_size=self.grid.cell_size,
                        grid_id=self.grid.id
                    )
            return obj
        except:
            self.message.set_value("There was an error instantiating the new object.")

    def place_object(self):
        if 0 <= self.matrix_x < self.grid.width and 0 <= self.matrix_y < self.grid.height:
            self.has_changes = True
            curr_obj = self.grid.matrix[self.matrix_x][self.matrix_y]
            new_obj = self.create_object(self.get_new_object_name())
            if new_obj:
                self.add_undo(curr_obj, new_obj, self.matrix_x, self.matrix_y, self.grid.id)
                self.grid.matrix[self.matrix_x][self.matrix_y] = new_obj
                GD.remove_obj_from_list(curr_obj)

                # Atualizar a posicao do objeto inicializado caso esteja em (0, 0)
                new_obj.move_left()
                new_obj.move_right()

    def delete_hovered_object(self):
        if 0 <= self.matrix_x < self.grid.width and 0 <= self.matrix_y < self.grid.height:
            self.has_changes = True
            self.add_undo(self.hovering, None, self.matrix_x, self.matrix_y, self.grid.id)
            if self.grid.matrix[self.matrix_x][self.matrix_y]:
                self.grid.matrix[self.matrix_x][self.matrix_y] = None
            else:
                for obj_list in self.grid.matrix:
                    if self.hovering in obj_list:
                        obj_list[obj_list.index(self.hovering)] = None
                        break
            GD.remove_obj_from_list(self.hovering)
            

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

    def draw(self):
        if self.highlight.x < self.grid.x + self.grid.width * self.grid.cell_size:
            self.highlight.draw()
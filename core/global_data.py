from PPlay.window import Window
from PPlay.gameobject import GameObject

from time import time

def print_dict(d, indent=0):
    for key, value in d.items():
        print(' ' * indent + str(key) + ':', end=' ')
        if isinstance(value, dict):
            print()  # Print a newline before diving into the nested dictionary
            print_dict(value, indent + 4)  # Increase indentation for nested dictionary
        elif isinstance(value, list) or isinstance(value, set):
            print()  # Print a newline before listing the elements
            for item in value:
                if isinstance(item, dict):
                    print_dict(item, indent + 4)  # Nested dictionary in list or set
                else:
                    print(' ' * (indent + 4) + str(item))
        else:
            print(value)

class GlobalData:
    class GlobalDataException(Exception):
        def __init__(self, message="An error occurred."):
            self.message = message
            super().__init__(self.message)

    _screen = None
    _on_screen_dict = {"All": set()}
    _update_range = None
    _window: Window = None
    _grids = []
    _player = None
    _level_being_played = -1
    _level_complete = False
    _level_completion_time = 0
    _game_over = False

    @staticmethod
    def _set_screen(window: Window):
        GlobalData._screen = GameObject()
        GlobalData._screen.width = window.width
        GlobalData._screen.height = window.height

        GlobalData._update_range = GameObject()
        GlobalData._update_range.width = window.width * 1.3
        GlobalData._update_range.height = window.height

    @staticmethod
    def add_screen_obj(obj: GameObject):
        obj_class = obj.__class__.__name__
        grid_id = obj.grid_id

        if obj_class in GlobalData._on_screen_dict:
            if grid_id in GlobalData._on_screen_dict[obj_class]:
                GlobalData._on_screen_dict[obj_class][grid_id].add(obj)
            else:
                GlobalData._on_screen_dict[obj_class][grid_id] = set([obj])
        else:
            GlobalData._on_screen_dict[obj_class] = {grid_id: set([obj])}

        GlobalData._on_screen_dict["All"].add(obj)
        

    @staticmethod
    def remove_screen_obj(obj: GameObject):
        obj_class = obj.__class__.__name__
        grid_id = obj.grid_id

        if obj_class in GlobalData._on_screen_dict:
            if grid_id in GlobalData._on_screen_dict[obj_class]:
                GlobalData._on_screen_dict[obj_class][grid_id].discard(obj)

        GlobalData._on_screen_dict["All"].discard(obj)
        

    @staticmethod
    def on_screen(obj: GameObject, append_to_list = False):
        if GlobalData._screen:
            if obj.collided(GlobalData._screen):
                if append_to_list:
                    GlobalData.add_screen_obj(obj)
                return True
            else:
                if append_to_list:
                    GlobalData.remove_screen_obj(obj)
        else:
            raise GlobalData.ScreenException("Window is not set")
    
    @staticmethod
    def off_screen(obj: GameObject, append_to_list = False):
        if not GlobalData.on_screen(obj, append_to_list):
            if obj.x + obj.width < 0:
                # Objeto está antes da tela
                return -1
            elif obj.x > GlobalData._screen.width:
                # Objeto está depois da tela
                return 1
        # Objeto esta dentro da tela
        return 0
    
    @staticmethod
    def on_update_range(obj: GameObject):
        return GlobalData._update_range.collided(obj)
    
    @staticmethod
    def reset_screen_objs():
        GlobalData._on_screen_dict = {}

    @staticmethod
    def get_screen_objs(class_name, grid_id = -1) -> set[GameObject]:
        if class_name == "All":
            return GlobalData._on_screen_dict["All"]
        
        elif class_name in GlobalData._on_screen_dict:

            if grid_id == -1:
                sets_list = []
                for grid_id in GlobalData._on_screen_dict[class_name]:
                    sets_list.append(GlobalData._on_screen_dict[class_name][grid_id])
                return set().union(*sets_list)
            
            else:
                objs_set = None
                if grid_id in GlobalData._on_screen_dict[class_name]:
                    objs_set = GlobalData._on_screen_dict[class_name][grid_id]
                if -1 in GlobalData._on_screen_dict[class_name]:
                    if objs_set:
                        objs_set = objs_set.union(GlobalData._on_screen_dict[class_name][-1])
                    else:
                        objs_set = GlobalData._on_screen_dict[class_name][-1]
                if objs_set:
                    return objs_set
        
        return set()

    @staticmethod
    def set_window(window: Window):
        GlobalData._window = window
        GlobalData._set_screen(window)

    @staticmethod
    def get_window() -> Window:
        return GlobalData._window

    @staticmethod
    def set_game_over(b: bool):
        GlobalData._game_over = b

    @staticmethod
    def is_game_over():
        return GlobalData._game_over
    
    @staticmethod
    def add_grid(grid):
        GlobalData._grids.append(grid)

    @staticmethod
    def remove_grid(grid_id: int):
        for grid in GlobalData._grids:
            if grid.id == grid_id:
                GlobalData._grids.remove(grid)
                return
        raise GlobalData.GlobalDataException(f"Grid with ID {grid_id} not found.")

    @staticmethod
    def get_grid(grid_id: int) -> GameObject:
        for grid in GlobalData._grids:
            if grid.id == grid_id:
                return grid
        raise GlobalData.GlobalDataException(f"Grid with ID {grid_id} not found.")
    
    @staticmethod
    def set_player(player):
        GlobalData._player = player

    @staticmethod
    def get_player() -> GameObject:
        return GlobalData._player
    
    @staticmethod
    def set_level_being_played(level):
        GlobalData._level_being_played = level

    @staticmethod
    def get_level_being_played():
        return GlobalData._level_being_played
    
    @staticmethod
    def set_level_complete(b: bool):
        if b:
            GlobalData._level_completion_time = time()
        GlobalData._level_complete = b

    @staticmethod
    def is_level_complete():
        return GlobalData._level_complete
    
    @staticmethod
    def get_level_completion_time():
        return GlobalData._level_completion_time

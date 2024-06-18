from PPlay.window import Window
from PPlay.gameobject import GameObject

class GlobalData:
    class GlobalDataException(Exception):
        def __init__(self, message="An error occurred."):
            self.message = message
            super().__init__(self.message)

    _screen = None
    _objs_on_screen = []
    _update_range = None
    _window: Window = None
    _game_over = False
    _grids = []
    _player = None

    @staticmethod
    def _set_screen(window: Window):
        GlobalData._screen = GameObject()
        GlobalData._screen.width = window.width
        GlobalData._screen.height = window.height

        GlobalData._update_range = GameObject()
        GlobalData._update_range.width = window.width * 1.3
        GlobalData._update_range.height = window.height

    @staticmethod
    def on_screen(obj: GameObject, append_to_list = False):
        if GlobalData._screen:
            if obj.collided(GlobalData._screen):
                if append_to_list and obj not in GlobalData._objs_on_screen:
                    GlobalData._objs_on_screen.append(obj)
                return True
            else:
                if obj in GlobalData._objs_on_screen:
                    GlobalData._objs_on_screen.remove(obj)
        else:
            raise GlobalData.ScreenException("Window is not set")
    
    @staticmethod
    def off_screen(obj: GameObject, append_to_list = False):
        if not GlobalData._screen.on_screen(obj, append_to_list):
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
    def remove_obj_from_list(obj: GameObject):
        if obj in GlobalData._objs_on_screen:
            GlobalData._objs_on_screen.remove(obj)
    
    @staticmethod
    def get_screen_objs():
        return GlobalData._objs_on_screen

    @staticmethod
    def set_window(window: Window):
        GlobalData._window = window
        GlobalData._set_screen(window)

    @staticmethod
    def get_window():
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
    def get_player():
        return GlobalData._player
    
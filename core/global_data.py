from PPlay.window import Window
from PPlay.gameobject import GameObject

class GlobalData:
    class GlobalDataException(Exception):
        def __init__(self, message="An error occurred."):
            self.message = message
            super().__init__(self.message)

    _screen = None
    _objs_on_screen = []
    _window: Window = None

    @staticmethod
    def set_screen(window: Window):
        GlobalData._screen = GameObject()
        GlobalData._screen.width = window.width
        GlobalData._screen.height = window.height

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
            raise GlobalData.ScreenException("Screen is not set")
    
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
    def remove_obj_from_list(obj: GameObject):
        if obj in GlobalData._objs_on_screen:
            GlobalData._objs_on_screen.remove(obj)
    
    @staticmethod
    def get_screen_objs():
        return GlobalData._objs_on_screen

    @staticmethod
    def set_window(window: Window):
        GlobalData._window = window

    @staticmethod
    def get_window():
        return GlobalData._window

    game_over: bool = False
    def set_game_over(b: bool):
        GlobalData.game_over = b
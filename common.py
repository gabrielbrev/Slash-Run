from PPlay.window import Window
from PPlay.gameobject import GameObject

from time import time

class Vector():
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y

class GlobalData():
    class GlobalDataException(Exception):
        def __init__(self, message="An error occurred."):
            self.message = message
            super().__init__(self.message)

    _screen = None
    objs_on_screen = []

    @staticmethod
    def set_screen(window: Window):
        GlobalData._screen = GameObject()
        GlobalData._screen.width = window.width
        GlobalData._screen.height = window.height

    @staticmethod
    def on_screen(obj: GameObject, append_to_list = False):
        if GlobalData._screen:
            if obj.collided(GlobalData._screen):
                if append_to_list and obj not in GlobalData.objs_on_screen:
                    GlobalData.objs_on_screen.append(obj)
                return True
            else:
                if obj in GlobalData.objs_on_screen:
                    GlobalData.objs_on_screen.remove(obj)
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
    
    _window: Window = None

    @staticmethod
    def set_window(window: Window):
        GlobalData._window = window

    @staticmethod
    def get_window():
        return GlobalData._window

    game_over: bool = False
    def set_game_over(b: bool):
        GlobalData.game_over = b

class FPSCounter():
    def __init__(self, x: int, y: int, size: int, color = (255, 255, 255)) -> None:
        self.curr_fps = 0
        self.counter = 0
        self.time_aux = time()
        self.x = x
        self.y = y
        self.size = size
        self.color = color
    
    def update(self):
        self.counter += 1
        now = time()
        if now - self.time_aux >= 1:
            self.curr_fps = self.counter
            self.counter = 0
            self.time_aux = now

    def draw(self):
        GlobalData.get_window().draw_text(str(self.curr_fps), self.x, self.y, self.size, self.color)
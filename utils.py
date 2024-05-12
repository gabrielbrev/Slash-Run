from PPlay.window import Window
from PPlay.gameobject import GameObject

class Vector():
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y

class ScreenUtils():
    def __init__(self, window: Window) -> None:
        self.window_obj = GameObject()
        self.window_obj.width = window.width
        self.window_obj.height = window.height

    def on_screen(self, obj: GameObject):
        return obj.collided(self.window_obj)
    
    def off_screen(self, obj: GameObject):
        if not self.on_screen(obj):
            if obj.x + obj.width < 0:
                # Objeto está antes da tela
                return -1
            elif obj.x > self.window_obj.width:
                # Objeto está depois da tela
                return 1
        return 0
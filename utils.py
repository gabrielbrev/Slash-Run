from PPlay.window import Window

from time import time

class Vector:
    def __init__(self, x = 0, y = 0) -> None:
        self.x = x
        self.y = y

class FPSCounter:
    def __init__(self, window: Window, x: int, y: int, size: int, color = (255, 255, 255)) -> None:
        self.window = window
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
        self.window.draw_text(str(self.curr_fps), self.x, self.y, self.size, self.color)
  
class Multipliable:
    def __init__(self, value: int, multipliers: list = [1]) -> None:
        self.default_value = value
        self.curr_value = value
        self.multipliers = multipliers
        self.multipliers.sort()
        self.cursor = 0
    
    def set_value(self, value):
        self.default_value = value
        self.curr_value = value * self.multipliers[self.cursor]

    def get_value(self):
        return self.curr_value
    
    def raise_multiplier(self):
        if self.cursor < len(self.multipliers) - 1:
            self.cursor += 1
            self.curr_value = self.default_value * self.multipliers[self.cursor]

    def lower_multiplier(self):
        if self.cursor > 0:
            self.cursor -= 1
            self.curr_value = self.default_value * self.multipliers[self.cursor]

class TimedVariable:
    def __init__(self, default_value, duration_s) -> None:
        self.default_value = default_value
        self.value = default_value
        self.duration = duration_s
        self.set_time = time()

    def set_value(self, value):
        self.value = value
        self.set_time = time()

    def get_value(self):
        if time() - self.set_time >= self.duration:
            self.value = self.default_value
        return self.value

    def get_duration(self):
        return self.duration
    
# Essa é uma ferramenta de debugging e não deve ser usada em multiplos pontos do código pois não vai funcionar como desejado
class PrintChange:
    _last_print = None
    @staticmethod
    def print(*values):
        if PrintChange._last_print != values:
            print(*values)
            PrintChange._last_print = values
    
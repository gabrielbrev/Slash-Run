from PPlay.window import Window
from PPlay.gameobject import GameObject

from core.global_data import GlobalData as GD

from time import time
from math import sqrt

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
  
# Variavel que possui um valor padrao e pode ser multiplicada por uma serie de numeros desejados
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
    
    def get_default_value(self):
        return self.default_value
    
    def raise_multiplier(self):
        if self.cursor < len(self.multipliers) - 1:
            self.cursor += 1
            self.curr_value = self.default_value * self.multipliers[self.cursor]

    def lower_multiplier(self):
        if self.cursor > 0:
            self.cursor -= 1
            self.curr_value = self.default_value * self.multipliers[self.cursor]

# Variavel que reseta seu valor apos o tempo desejado
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

# Feito para aumentar a dificuldade do boss de acordo com sua vida
def difficulty_multiplier(health, max_health):
    return 1 + (max_health - health) / 6

def convert_seconds(total_seconds):
    days = total_seconds // 86400
    hours = (total_seconds % 86400) // 3600
    minutes = (total_seconds % 3600) // 60
    seconds = int(total_seconds % 60)
    
    result = []
    if days > 0:
        result.append(f"{days} day{'s' if days != 1 else ''}")
    if hours > 0:
        result.append(f"{hours} hour{'s' if hours != 1 else ''}")
    if minutes > 0:
        result.append(f"{minutes} minute{'s' if minutes != 1 else ''}")
    if seconds > 0:
        result.append(f"{seconds} second{'s' if seconds != 1 else ''}")
    
    if len(result) > 1:
        return ', '.join(result[:-1]) + ' and ' + result[-1]
    elif result:
        return result[0]
    else:
        return "0 seconds"
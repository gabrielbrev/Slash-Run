from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse

from time import time
import json

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

class DataManager:
    def __init__(self) -> None:
        try:
            with open("data.json", "r") as json_file:
                self._data: dict = json.load(json_file)
        except:
            print("Could not instantiate object")

    def write(self, key, data):
        if key in self._data.keys():
            self._data[key] = data
            try:
                with open("data.json", "w") as json_file:
                    json.dump(self._data, json_file)
                    return 0
            except:
                print("Could not read file")
        return -1
        
    def read(self, key):
        try:
            with open("data.json", "r") as json_file:
                self._data: dict = json.load(json_file)
        except:
            print("Could not read file")
            return
        if key in self._data.keys():
            return self._data[key]
        
    def get_data_dict(self):
        return self._data

class KeyboardExtra(Keyboard):
    _clicked_keys = []

    def __init__(self) -> None:
        super().__init__()

    def key_clicked(self, key):
        if self.key_pressed(key):
            if key not in KeyboardExtra._clicked_keys:
                KeyboardExtra._clicked_keys.append(key)
                return True
            else:
                return False
        elif key in KeyboardExtra._clicked_keys:
            KeyboardExtra._clicked_keys.remove(key)
        return False
    
class MouseExtra(Mouse):
    _clicked_buttons = []

    def __init__(self):
        super().__init__()

    def is_button_clicked(self, button):
        if self.is_button_pressed(button):
            if button not in MouseExtra._clicked_buttons:
                MouseExtra._clicked_buttons.append(button)
                return True
            else:
                return False
        elif button in MouseExtra._clicked_buttons:
            MouseExtra._clicked_buttons.remove(button)
        return False
  
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
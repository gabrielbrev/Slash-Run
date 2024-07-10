from PPlay.gameobject import GameObject
from PPlay.gameimage import GameImage

from core.mouse_extra import MouseExtra
from core.sound_extra import SoundExtra

from .button import Button

class Slider(GameObject):
    def __init__(self, mouse: MouseExtra, bar_image, indicator_image, initial_value = 0, value_range: tuple = (0, 100), title: GameImage = None):
        super().__init__()
        self.mouse = mouse
        self.indicator = Button(mouse, indicator_image)
        self.bar = GameImage(bar_image)
        if len(value_range) != 2:
            raise ValueError("value_range must be of format (min, max)")
        self.min_value = value_range[0]
        self.max_value = value_range[1]
        self.value_range_size = self.max_value - self.min_value
        self.curr_value = initial_value
        self.width = self.bar.width + self.indicator.width
        self.height = max(self.bar.height, self.indicator.height)
        if title:
            self.title = title
            self.title_spacing = 20
            self.height += self.title.height + self.title_spacing
        self.set_position(0, 0)

        self.sliding = False

    def set_position(self, x, y):
        self.x = x
        self.y = y
        tallest = self.bar if self.bar.height > self.indicator.height else self.indicator
        self.bar.set_position(x + self.indicator.width/2, y + (tallest.height - self.bar.height)/2)
        self.set_indicator_position()
        if self.title:
            self.title.x = self.bar.x + self.bar.width/2 - self.title.width/2
            self.title.y = self.y
            self.y += self.title.height + self.title_spacing
            self.bar.y += self.title.height + self.title_spacing
            self.indicator.y += self.title.height + self.title_spacing
            

    def set_indicator_position(self):
        value_in_bar = self.bar.width * self.get_value_percentage()
        self.indicator.set_position(self.bar.x + value_in_bar - self.indicator.width/2, self.bar.y + self.bar.height/2 - self.indicator.height/2)

    def get_value_percentage(self):
        value_in_range = self.curr_value - self.min_value
        value_percentage = (value_in_range * 100 / self.value_range_size) / 100
        return value_percentage
    
    def _get_value(self):
        indicator_center_x = self.indicator.x + self.indicator.width/2
        value_in_bar = indicator_center_x - self.bar.x
        value_percentage = (value_in_bar * 100 / self.bar.width) / 100
        value = self.min_value + self.value_range_size * value_percentage
        return value
    
    def get_value(self):
        return self.curr_value
    
    def update(self):
        self.indicator.update()

        if self.indicator.is_hovered() or self.sliding:
            mouse_delta_x = self.mouse.delta_movement()[0]
            if self.indicator.is_clicked():
                self.sliding = True
            if self.sliding: 
                self.indicator.x += mouse_delta_x
                if not self.mouse.is_button_pressed(1):
                    self.sliding = False

        self.indicator.x = max(self.indicator.x, self.bar.x - self.indicator.width/2)
        self.indicator.x = min(self.indicator.x, self.bar.x + self.bar.width - self.indicator.width/2)

        self.curr_value = self._get_value()

    def draw(self):
        self.title.draw()
        self.bar.draw()
        self.indicator.draw()
    
    
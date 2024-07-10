from PPlay.gameimage import GameImage
from PPlay.sprite import Sprite

from core.global_data import GlobalData as GD

from utils import Multipliable

class Background():
    def __init__(self, speed: Multipliable) -> None:
        self.speed = speed
        self.window = GD.get_window()

        self.sprite_1 = Sprite("assets/sprites/backgrounds/level_bg.jpeg", 13)
        self.sprite_1.set_loop(False)
        self.sprite_1.playing = False

        self.sprite_2 = Sprite("assets/sprites/backgrounds/level_bg.jpeg", 13)
        self.sprite_2.set_loop(False)
        self.sprite_2.playing = False
        self.sprite_2.x = self.sprite_1.x + self.sprite_1.width

    def raise_speed(self):
        self.speed.raise_multiplier()
    
    def lower_speed(self):
        self.speed.lower_multiplier()
    
    def move_left(self):
        self.sprite_1.x -= self.speed.get_value() * self.window.delta_time()
        self.sprite_2.x -= self.speed.get_value() * self.window.delta_time()
        
        if self.sprite_1.x < self.sprite_2.x:
            if self.sprite_2.x < 0:
                self.sprite_1.x = self.sprite_2.x + self.sprite_2.width
        else:
            if self.sprite_1.x < 0:
                self.sprite_2.x = self.sprite_1.x + self.sprite_1.width
        # Coloca a primeira imagem (está fora da tela) na frente da segunda

    def move_right(self):
        self.sprite_1.x += self.speed.get_value() * self.window.delta_time()
        self.sprite_2.x += self.speed.get_value() * self.window.delta_time()
        
        if self.sprite_1.x < self.sprite_2.x:
            if self.sprite_1.x > 0:
                self.sprite_2.x = self.sprite_1.x - self.sprite_1.width
        else:
            if self.sprite_2.x > 0:
                self.sprite_1.x = self.sprite_2.x - self.sprite_2.width
        # Coloca a segunda imagem (está fora da tela) atras da segunda

    def darken(self, time_ms):
        self.sprite_1.set_total_duration(time_ms)
        self.sprite_1.playing = True
        self.sprite_2.set_total_duration(time_ms)
        self.sprite_2.playing = True

    def update(self):
        if GD.is_game_over():
            self.speed.set_value(0)
        self.move_left()
        self.sprite_1.update()
        self.sprite_2.update()

    def draw(self):
        if GD.on_screen(self.sprite_1):
            self.sprite_1.draw()
        if GD.on_screen(self.sprite_2):
            self.sprite_2.draw()
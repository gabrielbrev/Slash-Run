from PPlay.gameimage import GameImage

from .global_data import GlobalData as GD

from common import Multipliable

class Background():
    def __init__(self, speed, image_file, speed_multipliers: list = [1]) -> None:
        self.speed = Multipliable(speed, speed_multipliers)
        self.window = GD.get_window()
        self.image_1 = GameImage(image_file)
        self.image_2 = GameImage(image_file)
        self.image_2.x = self.image_1.x + self.image_1.width

    def raise_speed(self):
        self.speed.raise_multiplier()
    
    def lower_speed(self):
        self.speed.lower_multiplier()
    
    def move_left(self):
        self.image_1.x -= self.speed.get_value() * self.window.delta_time()
        self.image_2.x -= self.speed.get_value() * self.window.delta_time()
        
        if self.image_1.x < self.image_2.x:
            if self.image_2.x < 0:
                self.image_1.x = self.image_2.x + self.image_2.width
        else:
            if self.image_1.x < 0:
                self.image_2.x = self.image_1.x + self.image_1.width
        # Coloca a primeira imagem (está fora da tela) na frente da segunda

    def move_right(self):
        self.image_1.x += self.speed.get_value() * self.window.delta_time()
        self.image_2.x += self.speed.get_value() * self.window.delta_time()
        
        if self.image_1.x < self.image_2.x:
            if self.image_1.x > 0:
                self.image_2.x = self.image_1.x - self.image_1.width
        else:
            if self.image_2.x > 0:
                self.image_1.x = self.image_2.x - self.image_2.width
        # Coloca a segunda imagem (está fora da tela) atras da segunda

    def update(self):
        if not GD.game_over:
            self.move_left()

    def draw(self):
        if GD.on_screen(self.image_1):
            self.image_1.draw()
        if GD.on_screen(self.image_2):
            self.image_2.draw()
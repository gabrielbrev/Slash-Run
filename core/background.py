from PPlay.gameimage import GameImage

from common import GlobalData as GD

class Background():
    def __init__(self, speed, image_file) -> None:
        self.speed = speed
        self.window = GD.get_window()
        self.image_1 = GameImage(image_file)
        self.image_2 = GameImage(image_file)
        self.image_2.x = self.image_1.x + self.image_1.width
    
    def update(self):
        if not GD.game_over:
            self.image_1.x -= self.speed * self.window.delta_time()
            self.image_2.x -= self.speed * self.window.delta_time()
            
            if self.image_1.x < self.image_2.x:
                if self.image_2.x < 0:
                    self.image_1.x = self.image_2.x + self.image_2.width
            else:
                if self.image_1.x < 0:
                    self.image_2.x = self.image_1.x + self.image_1.width
            # Coloca a primeira imagem (está fora da tela) na frente da segunda

    def draw(self):
        if GD.on_screen(self.image_1):
            self.image_1.draw()
        if GD.on_screen(self.image_2):
            self.image_2.draw()
from PPlay.gameimage import GameImage

from .scene_objects.transition import Transition

from core.global_data import GlobalData as GD
from core.data_manager import DataManager

class Info:
    def __init__(self, image) -> None:
        self.window = GD.get_window()

        self.dm = DataManager()

        self.keyboard = GD.get_keyboard()

        self.t = Transition(100)
        
        self.bg = GameImage("assets/sprites/backgrounds/menu_bg.png")

        self.image = GameImage(image)
        self.image.set_position(self.window.width/2 - self.image.width/2, self.window.height/2 - self.image.height/2)

    def loop(self):
        self.t.play_in()
        while True:
            if self.keyboard.key_clicked("ESCAPE"):
                self.t.play_out(self.window)
                break
            
            self.window.update()

            self.bg.draw()
            self.image.draw()
            self.window.draw_text("ESC to go back", 5, 5, 12, (220, 220, 220))

            self.t.update()
            self.t.draw()
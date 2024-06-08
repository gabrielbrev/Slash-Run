from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.gameimage import GameImage

from .scene_objects.button import Button
from .scene_objects.transition import Transition

from scenes.level import Level

from common import GlobalData as GD
from common import KeyboardExtra

class LevelSelect:
    def __init__(self) -> None:
        self.window = GD.get_window()

        self.keyboard = KeyboardExtra()
        self.mouse = Mouse()

        self.t = Transition(100)

        self.bg = GameImage("/Users/gabrielbrevilieri/Desktop/Screenshot 2024-06-08 at 18.12.56.png")

    def loop(self):
        self.t.play_in()
        while True:
            if self.keyboard.key_clicked("ESCAPE"):
                self.t.play_out(self.window)
                break

            self.window.update()

            self.bg.draw()

            self.t.update()
            self.t.draw()

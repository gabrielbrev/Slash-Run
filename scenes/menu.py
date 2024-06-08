from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.mouse import Mouse
from PPlay.gameimage import GameImage

from .scene_objects.button import Button

from scenes.level_select import LevelSelect
from scenes.scene_objects.transition import Transition

from common import GlobalData as GD
from common import KeyboardExtra

class Menu:
    def __init__(self) -> None:
        self.window = GD.get_window()

        self.keyboard = KeyboardExtra()
        self.mouse = Mouse()

        self.t = Transition(100)

        self.bg = GameImage("assets/backgrounds/menu_bg.png")

        self.title = GameImage("assets/scene_objects/title.png")
        self.title.set_position(
            x=self.window.width / 2 - self.title.width / 2,
            y=20
        )

        self.play_button = Button(
            window=self.window,
            mouse=self.mouse,
            image_file="assets/scene_objects/buttons/play.png",
            frames=2,
            command=LevelSelect().loop,
            transition=self.t
        )
        self.play_button.set_position(
            x=self.window.width/2 - self.play_button.width/2,
            y=self.window.height/2 - self.play_button.height/2 + 75
        )

    def loop(self):
        while True:
            if self.keyboard.key_clicked("ESCAPE"):
                break
            elif self.keyboard.key_clicked("o"):
                self.t.play_in()

            self.window.update()
            self.play_button.update()
            if self.play_button.was_pressed():
                self.t.play_in()

            self.bg.draw()
            self.title.draw()
            self.play_button.draw()
            
            self.t.update()
            self.t.draw()
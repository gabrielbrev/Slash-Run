from PPlay.sound import Sound
from PPlay.gameimage import GameImage

from .scene_objects.transition import Transition

from scenes.menu import Menu

from core.global_data import GlobalData as GD
from core.sound_extra import SoundExtra
from core.data_manager import DataManager

from time import time

class Intro:
    def __init__(self) -> None:
        self.window = GD.get_window()

        self.dm = DataManager()

        self.keyboard = GD.get_keyboard()

        self.music = Sound("assets/sounds/music/intro_ambiance.ogg")
        self.music.set_volume(75)
        self.music.set_repeat(True)

        self.t = Transition(600)
        
        self.images = [GameImage(f"assets/sprites/screens/intro_{i}.png") for i in range(6)]

        title_screen = GameImage("assets/sprites/screens/title.png")
        title_screen.set_position(self.window.width/2 - title_screen.width/2, 0)
        self.images.append(title_screen)

        self.image_index = 0

    def change_image(self):
        self.image_index += 1
        self.t.play_out(self.window)
        start_time = time()
        while time() - start_time < 0.3:
            self.window.update()
        self.t.play_in()

    def start_game(self):
        self.music.fadeout(1000)
        start_time = time()
        while time() - start_time <= 4:
            self.images[self.image_index].draw()
            self.t.update()
            self.t.draw()
            self.window.update()
        self.t.play_out(self.window)
        self.dm.set_fisrt_boot(False)
        Menu().loop()

    def loop(self):
        self.t.play_in()
        self.music.play()
        while True:
            if self.keyboard.key_clicked("RETURN"):
                self.change_image()
            
            self.window.update()

            self.images[self.image_index].draw()
            if self.image_index < len(self.images) - 1:
                text = "Press ENTER to proceed"
                self.window.draw_text(text, self.window.width/2 - 80, self.window.height - 20, color=(100, 100, 100))
            else:
                self.start_game()
                break

            self.t.update()
            self.t.draw()

            
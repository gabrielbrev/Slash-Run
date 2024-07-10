from PPlay.mouse import Mouse
from PPlay.gameimage import GameImage

from .scene_objects.locked_button import LockedButton
from .scene_objects.button import Button
from .scene_objects.transition import Transition

from scenes.level import Level

from core.global_data import GlobalData as GD
from core.keyboard_extra import KeyboardExtra
from core.sound_extra import SoundExtra
from core.data_manager import DataManager

from .scene_objects.slider import Slider

class Config:
    def __init__(self, music: SoundExtra) -> None:
        self.window = GD.get_window()

        self.dm = DataManager()

        self.music = music

        self.keyboard = GD.get_keyboard()
        self.mouse = GD.get_mouse()

        self.t = Transition(100)

        self.bg = GameImage("assets/sprites/backgrounds/menu_bg.png")
        
        self.music_slider = Slider(
            mouse=GD.get_mouse(),
            bar_image="assets/sprites/scene_objects/buttons/slider_bar.png",
            indicator_image="assets/sprites/scene_objects/buttons/slider_indicator.png",
            initial_value=self.dm.get_music_volume(),
            value_range=(0, 100),
            title=GameImage("assets/sprites/scene_objects/titles/music.png")
        )
        self.music_slider.set_position(
            x=self.window.width/2 - self.music_slider.width/2,
            y=self.window.height/2 - self.music_slider.height - 20
        )

        self.sfx_slider = Slider(
            mouse=GD.get_mouse(),
            bar_image="assets/sprites/scene_objects/buttons/slider_bar.png",
            indicator_image="assets/sprites/scene_objects/buttons/slider_indicator.png",
            initial_value=self.dm.get_sfx_volume(),
            value_range=(0, 100),
            title=GameImage("assets/sprites/scene_objects/titles/sfx.png")
        )
        self.sfx_slider.set_position(
            x=self.window.width/2 - self.sfx_slider.width/2,
            y=self.window.height/2 + 20
        )

    def loop(self):
        self.t.play_in()
        while True:
            music_volume = self.music_slider.get_value()
            sfx_volume = self.sfx_slider.get_value()

            if self.keyboard.key_clicked("ESCAPE"):
                self.dm.set_music_volume(music_volume)
                self.dm.set_sfx_volume(sfx_volume)
                self.t.play_out(self.window)
                break

            self.window.update()
            self.music_slider.update()
            self.sfx_slider.update()

            self.music.update_volume()
            GD.set_music_volume(music_volume)
            GD.set_sfx_volume(sfx_volume)

            self.bg.draw()
            self.window.draw_text("ESC to go back", 5, 5, 12, (220, 220, 220))
            self.music_slider.draw()
            self.sfx_slider.draw()

            self.t.update()
            self.t.draw()
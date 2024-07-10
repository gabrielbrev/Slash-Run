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

class LevelSelect:
    def __init__(self, music: SoundExtra) -> None:
        self.window = GD.get_window()

        self.dm = DataManager()

        self.music = music

        button_hover_sound = SoundExtra("assets/sounds/sfx/button_hover.ogg", "sfx", 15, False)
        button_click_sound = SoundExtra("assets/sounds/sfx/level_button_click.ogg", "sfx", 30, False)

        self.keyboard = GD.get_keyboard()
        self.mouse = GD.get_mouse()

        self.t = Transition(100)
        self.t.set_play_out_duration(1300)

        self.bg = GameImage("assets/sprites/backgrounds/menu_bg.png")

        self.buttons = []

        self.level_1_button = LockedButton(
            mouse=self.mouse,
            button_image="assets/sprites/scene_objects/buttons/level1.png",
            lock_image="assets/sprites/scene_objects/buttons/lock.png",
            locked=False,
            command=self.start_level,
            args=(1,),
            transition=self.t,
            hover_sound=button_hover_sound,
            click_sound=button_click_sound,
            fade_sounds=True
        )
        self.level_2_button = LockedButton(
            mouse=self.mouse,
            button_image="assets/sprites/scene_objects/buttons/level2.png",
            lock_image="assets/sprites/scene_objects/buttons/lock.png",
            command=self.start_level,
            args=(2,),
            transition=self.t,
            hover_sound=button_hover_sound,
            click_sound=button_click_sound,
            fade_sounds=True
        )
        self.level_3_button = LockedButton(
            mouse=self.mouse,
            button_image="assets/sprites/scene_objects/buttons/level3.png",
            lock_image="assets/sprites/scene_objects/buttons/lock.png",
            command=self.start_level,
            args=(3,),
            transition=self.t,
            hover_sound=button_hover_sound,
            click_sound=button_click_sound,
            fade_sounds=True
        )
        self.custom_level_button = Button(
            mouse=self.mouse,
            image_file="assets/sprites/scene_objects/buttons/level0.png",
            command=self.start_level,
            args=(0,),
            transition=self.t,
            hover_sound=button_hover_sound,
            click_sound=button_click_sound,
            fade_sounds=True
        )

        self.level_2_button.set_position(
            x=self.window.width/2 - self.level_2_button.width/2,
            y=self.window.height/2 - self.level_2_button.height/2
        )
        self.level_3_button.set_position(
            x=self.level_2_button.x + self.level_2_button.width + 100,
            y=self.window.height/2 - self.level_3_button.height/2
        )
        self.level_1_button.set_position(
            x=self.level_2_button.x - self.level_1_button.width - 100,
            y=self.window.height/2 - self.level_1_button.height/2
        )
        self.custom_level_button.set_position(
            x=self.window.width/2 - self.custom_level_button.width/2,
            y=(self.level_2_button.y + self.level_2_button.height + self.window.height)/2 - self.custom_level_button.height/2
        )

        self.buttons.append(self.level_1_button)
        self.buttons.append(self.level_2_button)
        self.buttons.append(self.level_3_button)

        self.unlock_buttons()

    def unlock_buttons(self):
        current_level = self.dm.get_current_level()
        for i in range(current_level):
            if i < 3:
                self.buttons[i].unlock()
        if self.dm.has_accessed_editor():
            self.buttons.append(self.custom_level_button)

    def start_level(self, level_id):
        self.music.fadeout(500)
        self.mouse.hide()
        Level(level_id).loop()
        self.music.play()
        self.mouse.unhide()

    def loop(self):
        self.t.play_in()
        while True:
            if self.keyboard.key_clicked("ESCAPE"):
                self.t.set_play_out_duration(100)
                self.t.play_out(self.window)
                break

            self.window.update()
            for button in self.buttons:
                button.update()
                if button.is_clicked():
                    self.unlock_buttons()
                    self.t.play_in()

            self.bg.draw()
            self.window.draw_text("ESC to go back", 5, 5, 12, (220, 220, 220))
            for button in self.buttons:
                button.draw()

            self.t.update()
            self.t.draw()
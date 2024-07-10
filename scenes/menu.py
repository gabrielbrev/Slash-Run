from PPlay.gameimage import GameImage

from .scene_objects.button import Button
from .scene_objects.locked_button import LockedButton
from .scene_objects.transition import Transition

from scenes.level_select import LevelSelect
from scenes.level_editor import LevelEditor
from scenes.config import Config

from core.global_data import GlobalData as GD
from core.sound_extra import SoundExtra
from core.data_manager import DataManager

class Menu:
    def __init__(self) -> None:
        self.window = GD.get_window()

        self.dm = DataManager()

        self.keyboard = GD.get_keyboard()
        self.mouse = GD.get_mouse()

        self.music = SoundExtra("assets/sounds/music/menu_ambiance.ogg", "music")
        self.music.set_repeat(True)

        self.t = Transition(100)

        self.bg = GameImage("assets/sprites/backgrounds/menu_bg.png")

        self.title = GameImage("assets/sprites/scene_objects/titles/slash_run.png")
        self.title.set_position(self.window.width / 2 - self.title.width / 2, 40)

        self.buttons = []
        self.play_button = Button(
            mouse=self.mouse,
            image_file="assets/sprites/scene_objects/buttons/play.png",
            command=self.change_scene,
            args=("level_select",),
            transition=self.t,
            hover_sound=SoundExtra("assets/sounds/sfx/button_hover.ogg", "sfx", 15, False),
            click_sound=SoundExtra("assets/sounds/sfx/menu_button_click.ogg", "sfx", 40, False)
        )
        self.play_button.set_position(
            x=self.window.width/2 - self.play_button.width/2, 
            y=self.window.height/2 - self.play_button.height/2 + 75
        )
        self.buttons.append(self.play_button)

        self.config_button = Button(
            mouse=self.mouse,
            image_file="assets/sprites/scene_objects/buttons/config.png",
            command=self.change_scene,
            args=("config",),
            transition=self.t,
            hover_sound=SoundExtra("assets/sounds/sfx/button_hover.ogg", "sfx", 15, False),
            click_sound=SoundExtra("assets/sounds/sfx/menu_button_click.ogg", "sfx", 30, False)
        )
        self.config_button.set_position(
            x=self.play_button.x + self.play_button.width, 
            y=self.play_button.y + self.play_button.height / 2 - self.config_button.height / 2
        )
        self.buttons.append(self.config_button)

        self.editor_button = LockedButton(
            mouse=self.mouse,
            button_image="assets/sprites/scene_objects/buttons/editor.png",
            lock_image="assets/sprites/scene_objects/buttons/lock.png",
            locked=True,
            command=self.change_scene,
            args=("level_editor",),
            transition=self.t,
            hover_sound=SoundExtra("assets/sounds/sfx/button_hover.ogg", "sfx", 15, False),
            click_sound=SoundExtra("assets/sounds/sfx/menu_button_click.ogg", "sfx", 30, False)
        )
        self.editor_button.set_position(
            x=self.play_button.x - self.editor_button.width, 
            y=self.play_button.y + self.play_button.height / 2 - self.editor_button.height / 2
        )
        self.buttons.append(self.editor_button)

        self.try_unlock_editor()

    def change_scene(self, scene: str):
        match scene:
            case "level_select":
                LevelSelect(self.music).loop()
            case "level_editor":
                self.music.pause()
                self.dm.set_accessed_editor(True)
                LevelEditor().loop()
            case "config":
                Config(self.music).loop()
            case _:
                raise ValueError("Invalid scene name")
        self.music.unpause()

    def try_unlock_editor(self):
        if self.dm.get_current_level() == 4:
            self.editor_button.unlock()
        else:
            self.editor_button.lock()

    def loop(self):
        self.t.play_in()
        self.music.play()
        while True:
            # Comando secreto para resetar os dados do jogo
            if self.keyboard.key_pressed("Q"): # Quero
                if self.keyboard.key_pressed("R"): # Resetar
                    if self.keyboard.key_pressed("M"): # Meus
                        if self.keyboard.key_clicked("D"): # Dados ;)
                            self.dm.reset_data()
                            self.try_unlock_editor()

            self.window.update()
            for button in self.buttons:
                button.update()
                if button.is_clicked():
                    self.try_unlock_editor()
                    self.t.play_in()

            self.bg.draw()
            self.title.draw()
            for button in self.buttons:
                button.draw()
            
            self.t.update()
            self.t.draw()
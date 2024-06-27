from PPlay.mouse import Mouse
from PPlay.gameimage import GameImage

from .scene_objects.button import Button
from .scene_objects.locked_button import LockedButton

from scenes.level_select import LevelSelect
from scenes.level_editor import LevelEditor
from scenes.scene_objects.transition import Transition

from core.global_data import GlobalData as GD
from core.keyboard_extra import KeyboardExtra
from core.data_manager import DataManager

class Menu:
    def __init__(self) -> None:
        self.window = GD.get_window()

        self.dm = DataManager()

        self.keyboard = KeyboardExtra()
        self.mouse = Mouse()

        self.t = Transition(100)

        self.bg = GameImage("assets/backgrounds/menu_bg.png")

        self.title = GameImage("assets/scene_objects/title.png")
        self.title.set_position(self.window.width / 2 - self.title.width / 2, 40)

        self.buttons = []
        self.play_button = Button(
            mouse=self.mouse,
            image_file="assets/scene_objects/buttons/play.png",
            command=self.change_scene,
            args=("level_select",),
            transition=self.t
        )
        self.play_button.set_position(
            x=self.window.width/2 - self.play_button.width/2, 
            y=self.window.height/2 - self.play_button.height/2 + 75
        )
        self.buttons.append(self.play_button)

        self.info_button = Button(
            mouse=self.mouse,
            image_file="assets/scene_objects/buttons/info.png",
            # command=LevelSelect().loop,
            transition=self.t
        )
        self.info_button.set_position(
            x=self.play_button.x + self.play_button.width, 
            y=self.play_button.y + self.play_button.height / 2 - self.info_button.height / 2
        )
        self.buttons.append(self.info_button)

        self.editor_button = LockedButton(
            mouse=self.mouse,
            button_image="assets/scene_objects/buttons/editor.png",
            lock_image="assets/scene_objects/buttons/lock.png",
            locked=True,
            command=self.change_scene,
            args=("level_editor",),
            transition=self.t
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
                LevelSelect().loop()
            case "level_editor":
                self.dm.set_accessed_editor(True)
                LevelEditor().loop()
            case "_":
                raise ValueError("Invalid scene name")

    def try_unlock_editor(self):
        if self.dm.get_current_level() == 4:
            self.editor_button.unlock()
        else:
            self.editor_button.lock()

    def loop(self):
        self.t.play_in()
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
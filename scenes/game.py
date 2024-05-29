from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.gameimage import GameImage
from PPlay.mouse import Mouse

from core.grid import Grid
from core.background import Background

from entities.player import Player

from scenes.scene_objects.health_bar import HealthBar
from scenes.scene_objects.energy_bar import EnergyBar

from common import GlobalData as GD
from common import FPSCounter

class GameScene():
    def __init__(self, level = 0) -> None:
        self.window = GD.get_window()

        self.keyboard = Keyboard()
        self.mouse = Mouse()

        self.bg = Background(50, "assets/backgrounds/background.jpeg")

        self.front_grid = Grid(2000, 13, 600, 64)
        self.front_grid.load_level(f"levels/{level}/front.json")

        self.back_grid = Grid(2000, 26, 500, 48)
        self.back_grid.load_level(f"levels/{level}/back.json")

        self.player = Player(self.front_grid, self.back_grid)

        self.health_bar = HealthBar(self.player)
        self.health_bar.set_position(5, 5)

        self.energy_bar = EnergyBar(self.player)
        self.energy_bar.set_position(self.health_bar.x, self.health_bar.y + self.health_bar.height)

        self.fps = FPSCounter(0, 0, 30)

    def loop(self):
        while True:
            if self.keyboard.key_pressed("W"):
                self.player.jump()
            if self.keyboard.key_pressed("A"):
                self.player.move_left()  
            if self.keyboard.key_pressed("D"):
                self.player.move_right()
            if self.keyboard.key_pressed("SPACE"):
                self.player.switch_plane()
            if self.mouse.is_button_pressed(1):
                self.player.attack()

            if self.keyboard.key_pressed("h"):
                self.player.increment_energy()
            if self.keyboard.key_pressed("j"):
                self.player.decrement_energy()

            self.window.update()

            self.bg.update()
            self.player.update()
            self.back_grid.update()
            self.front_grid.update()
            self.health_bar.update()
            self.energy_bar.update()

            self.bg.draw()
            self.back_grid.draw()
            self.player.draw()
            self.front_grid.draw()
            self.health_bar.draw()
            self.energy_bar.draw()

            self.fps.update()
            self.fps.draw()
    
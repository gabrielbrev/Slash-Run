from PPlay.window import Window
from PPlay.keyboard import Keyboard
from PPlay.gameimage import GameImage

from entities.player import Player
from core.grid import Grid

window = Window(1300, 800)
window.set_title("Slash Run")

keyboard = Keyboard()

player = Player(window, keyboard, "assets/sprites/kim_run_colored.png", 6)

bg = GameImage("assets/backgrounds/background.png")

grid = Grid(window, 1000, 13, 500, 64, True, False)
grid.load_level("levels/level_0.json")

while True:
    window.update()
    player.update()
    grid.update(player)

    bg.draw()
    grid.draw()
    player.draw()
    
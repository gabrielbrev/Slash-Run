from PPlay.window import Window
from PPlay.gameimage import GameImage

from core.global_data import GlobalData as GD

from scenes.menu import Menu

from time import sleep
from random import randint

window = Window(1300, 800)
window.set_title("Slash Run")

title_screen = GameImage("assets/title_screen.png")
title_screen.set_position(window.width/2 - title_screen.width/2, 0)
title_screen.draw()

window.update()

GD.set_window(window)

print("Let's pretend something is loading... Its for the aesthetics :)")
sleep(randint(3, 5) / 10)

menu = Menu()
menu.loop()
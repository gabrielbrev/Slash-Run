from PPlay.window import Window
from PPlay.gameimage import GameImage

from core.global_data import GlobalData as GD
from core.mouse_extra import MouseExtra
from core.keyboard_extra import KeyboardExtra
from core.data_manager import DataManager

from scenes.menu import Menu
from scenes.intro import Intro

from time import sleep
from random import randint

window = Window(1300, 800)
window.set_title("Slash Run")

dm = DataManager()

GD.set_window(window)
GD.set_mouse(MouseExtra())
GD.set_keyboard(KeyboardExtra())
GD.set_music_volume(dm.get_music_volume())
GD.set_sfx_volume(dm.get_sfx_volume())

if dm.is_first_boot():
    Intro().loop()
else:
    title_screen = GameImage("assets/sprites/screens/title.jpeg")
    title_screen.set_position(window.width/2 - title_screen.width/2, 0)
    title_screen.draw()

    window.update()

    print("Pretend something is loading... Its for the aesthetics :)")
    sleep(randint(3, 5) / 10)

    Menu().loop()



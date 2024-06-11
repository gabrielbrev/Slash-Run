from PPlay.window import Window

from core.global_data import GlobalData as GD

from scenes.menu import Menu

window = Window(1300, 800)
window.set_title("Slash Run")

GD.set_window(window)
GD.set_screen(window)

menu = Menu()
menu.loop()
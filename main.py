from PPlay.window import Window

from common import GlobalData as GD

from scenes.game import GameScene

window = Window(1300, 800)
window.set_title("Slash Run")

GD.set_window(window)
GD.set_screen(window)

gs = GameScene()
gs.loop()



from PPlay.window import Window
from PPlay.gameobject import GameObject

from utils import ScreenUtils
from entities.player import Player

class ExtenseObject(GameObject):
    def __init__(self, window: Window, x, y, width, height, cell_size, type, args=()):
        super().__init__()
        self.window = window
        self.x = x
        self.y = y
        self.width = width * cell_size
        self.height = height * cell_size
        self.cell_size = cell_size
        self.matrix = []
        for i in range(width):
            obj_list = []
            for j in range(height):
                obj = type(*args)
                obj.x = x + i * cell_size
                obj.y = y + j * cell_size
                obj_list.append(obj)
            self.matrix.append(obj_list)
        self.screen = ScreenUtils(window)

    def update(self, player: Player):
        if self.collided(player):
            player.on_air = False
            player.y = self.y - player.height

        for i, obj_list in enumerate(self.matrix):
            for j, obj in enumerate(obj_list):
                obj.x = self.x + i * self.cell_size
                obj.y = self.y + j * self.cell_size
                obj.update()

    def draw(self):
        for obj_list in self.matrix:
            for obj in obj_list:
                if self.screen.on_screen(obj):
                    obj.draw()

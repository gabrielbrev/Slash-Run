from PPlay.gameobject import GameObject

from .skullord_hand import SkullordHand
from .skullord_head import SkullordHead

from core.grid import Grid
from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA

from .boulder import Boulder

from grid_objects.energy_orb import EnergyOrb

from time import time
from random import randint

class Skullord(GameObject):
    def __init__(self, x, y, fg: Grid, bg: Grid):
        super().__init__()
        self.window = GD.get_window()
        self.grid_id = -1
        self.x = x
        self.y = y
        self.fg = fg
        self.bg = bg
        self.head = SkullordHead(self.window.width + 500, -500, fg, bg)
        self.left_hand = SkullordHand(self.head.x - 100, self.head.y + 150, fg)
        self.right_hand = SkullordHand(self.head.x - 50, self.head.y + 100, bg)

        self.init_cooldown = 2.5
        self.init_time = 0
        self.active = False

        self.head.move_to(x, y, 2, MA.EASE_OUT_BACK)
        self.left_hand.move_to(x - 100, y + 150, 2.5, MA.EASE_OUT_BACK)
        self.right_hand.move_to(x - 50, y + 100, 2.5, MA.EASE_OUT_BACK)

        self.head.set_anchor(x, y)
        self.left_hand.set_anchor(x - 100, y + 150)
        self.right_hand.set_anchor(x - 50, y + 100)

        self.alive = True

    def is_alive(self):
        return self.alive

    def update(self):
        if not self.init_time:
            self.init_time = time()
        else:
            if self.active:
                self.left_hand.handle_actions()
                self.right_hand.handle_actions()
            elif time() - self.init_time >= self.init_cooldown:
                self.active = True
            self.head.update()
            self.left_hand.update()
            self.right_hand.update()

            if not self.head.active and self.left_hand.damaged and self.right_hand.damaged:
                self.head.activate()
                self.head.active = True
            elif self.head.active and self.head.get_action() == "idle" and self.left_hand.damaged and self.right_hand.damaged:
                self.left_hand.damaged = False
                self.right_hand.damaged = False
                self.head.active = False
            
            if not self.head.is_alive():
                self.left_hand.kill()
                self.right_hand.kill()
                self.alive = False

    def draw_head(self):
        self.head.draw()

    def draw_left_hand(self):
        self.left_hand.draw()

    def draw_right_hand(self):
        self.right_hand.draw()

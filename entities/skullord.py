from PPlay.gameobject import GameObject

from .skullord_hand import SkullordHand
from .skullord_head import SkullordHead

from core.grid import Grid
from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA

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
        self.left_hand = SkullordHand(self.head.x - 100, self.head.y + 150, self.head, fg)
        self.right_hand = SkullordHand(self.head.x - 50, self.head.y + 100, self.head, bg)

        self.init_cooldown = 2.5
        self.init_time = 0
        self.active = False

        self.alive = True

    def is_alive(self):
        return self.alive
    
    def is_active(self):
        return bool(self.init_time)
    
    def activate(self):
        self.init_time = time()
        self.head.move_to(self.x, self.y, 2, MA.EASE_OUT_BACK)
        self.left_hand.move_to(self.x - 15, self.y + 200, 2.5, MA.EASE_OUT_BACK)
        self.right_hand.move_to(self.x - 75, self.y + 170, 2.5, MA.EASE_OUT_BACK)

        self.head.set_anchor(self.x, self.y)
        self.left_hand.set_anchor(self.x - 15, self.y + 200)
        self.right_hand.set_anchor(self.x - 75, self.y + 170)

        self.left_hand.summon_time = time()
        self.right_hand.summon_time = time()
        if abs(self.right_hand.summon_cooldown - self.left_hand.summon_cooldown) < 1:
            if randint(0, 1):
                self.right_hand.summon_cooldown += 1
            else:
                self.left_hand.summon_cooldown += 1

    def fade_sounds(self, time_ms):
        self.left_hand.fade_sounds(time_ms)
        self.right_hand.fade_sounds(time_ms)
        self.head.fade_sounds(time_ms)

    def update(self):            
        if self.init_time:
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
                self.left_hand.can_summon = False
                self.right_hand.can_summon = False
            elif self.head.active and self.head.get_action() == "idle" and self.left_hand.damaged and self.right_hand.damaged:
                self.left_hand.damaged = False
                self.right_hand.damaged = False
                self.left_hand.can_summon = True
                self.right_hand.can_summon = True
                self.head.active = False

            if not self.head.active and not self.head.is_moving() and self.left_hand.damaged != self.right_hand.damaged:
                if self.left_hand.damaged:
                    if time() - self.left_hand.damage_time >= self.left_hand.damage_duration:
                        self.left_hand.damaged = False
                elif self.right_hand.damaged:
                    if time() - self.right_hand.damage_time >= self.right_hand.damage_duration:
                        self.right_hand.damaged = False
            
            if not self.head.is_alive():
                self.left_hand.kill()
                self.right_hand.kill()
                self.alive = False
                self.left_hand.mute()
                self.right_hand.mute()
            
            self.left_hand.hand_health = self.head.health
            self.right_hand.hand_health = self.head.health

    def mute(self):
        self.head.mute()
        self.left_hand.mute()
        self.right_hand.mute()

    def unmute(self):
        self.head.unmute()
        self.left_hand.unmute()
        self.right_hand.unmute()

    def draw_head(self):
        self.head.draw()

    def draw_left_hand(self):
        self.left_hand.draw()

    def draw_right_hand(self):
        self.right_hand.draw()

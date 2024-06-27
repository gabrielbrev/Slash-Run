from .fixed_entity import FixedEntity

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation
from core.grid import Grid

from .fireball import FireBall

from utils import Vector

from time import time
from random import randint

class SkullordHead(FixedEntity):
    GRAVITY = 50

    def __init__(self, x, y, fg: Grid, bg: Grid):
        super().__init__(x, y, 375, 450)

        self.window = GD.get_window()

        self.y_speed = -20

        self.fg = fg
        self.bg = bg
        self.grid_id = -1

        self.player = GD.get_player()

        self.add_sprite("idle", "assets/entities/skullord/head/idle.png", 1, 500)
        self.add_sprite("magic", "assets/entities/skullord/head/magic.png", 1, 500)

        self.set_action("idle")

        self.fireball_cooldown = 0.2
        self.last_fireball_time = time()
        self.fireball_index = 0
        self.last_fireball_x = 0

        self.fireballs = []
        for i in range(30):
            if i % 2 == 0:
                f = FireBall(0, 0, 0, bg.cell_size, bg.id)
            else:
                f = FireBall(0, 0, 0, fg.cell_size, fg.id)
            self.reset_fireball(f)
            f.destroyed = True
            f.set_speed(600)
            self.fireballs.append(f)

        self.magic_duration = 7.5
        self.magic_start_time = time()

        self.health = 1
        self.lost_health = False
        self.alive = True

        self.active = False

        GD.add_screen_obj(self)

    def is_alive(self):
        return self.alive
    
    def kill(self):
        self.move_to(self.x + 10, self.window.height, 2.5, MoveAnimation.EASE_IN_BACK)
        self.alive = False

    def activate(self):
        self.move_to(self.x - 150, self.y + 150, 0.5, MoveAnimation.EASE_OUT_EXPO)
        self.lost_health = False
        self.magic_start_time = time()
        self.set_action("magic")

    def deactivate(self):
        self.move_to(self.og_pos.x, self.og_pos.y, 0.5, MoveAnimation.EASE_OUT_EXPO)
        self.y_speed = -20
        self.set_action("idle")

    def decrement_health(self):
        if not self.lost_health:
            if self.health:
                self.blink(1)
                self.health -= 1
                self.lost_health = True
                if not self.health:
                    self.blink(10)
                    self.kill()
                else:
                    self.deactivate()

    def reset_fireball(self, f: FireBall):
        x = self.last_fireball_x
        while abs(x - self.last_fireball_x) < f.width * 2:
            x = randint(0, int(self.window.width // f.width)) * f.width
        self.last_fireball_x = x
        y = -f.height
        f.set_position(x, y)
        f.set_action("shoot", reset=True)
        f.destroyed = False
        f.hit_the_ground = False

    def summon_fireballs(self):
        if time() - self.magic_start_time >= 0.5:
            fireball = self.fireballs[self.fireball_index]
            if fireball.is_destroyed():
                self.reset_fireball(fireball)
            if time() - self.last_fireball_time >= self.fireball_cooldown:
                self.fireball_index += 1
                if self.fireball_index >= len(self.fireballs):
                    self.fireball_index = 0
                self.last_fireball_time = time()

    def handle_fireballs(self):
        for fireball in self.fireballs:
            if not fireball.is_destroyed():
                fireball.update()

    def handle_actions(self):
        if self.get_action() == "idle":
            if not self.is_moving():
                if self.y >= self.og_pos.y:
                    self.y_speed -= SkullordHead.GRAVITY * self.window.delta_time()
                else:
                    self.y_speed += SkullordHead.GRAVITY * self.window.delta_time()
                self.y += self.y_speed * self.window.delta_time()

        if self.get_action() == "magic":
            if time() - self.magic_start_time >= self.magic_duration:
                if self.alive:
                    self.deactivate()
            self.summon_fireballs()

        self.handle_fireballs()

    def update(self):
        self.handle_actions()
        super().update()

    def draw(self):
        for f in self.fireballs:
            f.draw()
        super().draw()


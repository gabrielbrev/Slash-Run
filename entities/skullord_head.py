from .fixed_entity import FixedEntity

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation
from core.grid import Grid

from .fireball import FireBall

from utils import difficulty_multiplier

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

        self.add_sprite("idle", "assets/sprites/entities/skullord/head/idle.png", 1, 500)
        self.add_sprite("magic", "assets/sprites/entities/skullord/head/magic.png", 10, 600)

        self.set_action("idle")

        self.add_sound("magic", "assets/sounds/sfx/skullord_magic.ogg", 55, True)
        self.add_sound("damage", "assets/sounds/sfx/enemy_damage_hard.ogg", 20)
        self.add_sound("death", "assets/sounds/sfx/skullord_death.ogg")

        self.fireball_cooldown = 0.15
        self.last_fireball_time = time()
        self.fireball_index = 0
        self.last_fireball_x = 0
        self.summon_counter = 0
        self.can_summon = True

        self.magic_duration = 10
        self.magic_start_time = time()

        self.health = 5
        self.lost_health = False
        self.alive = True

        self.active = False

        self.fireballs = []
        self.back_fireballs = []
        self.front_fireballs = []
        # front e back sao utilizadas apenas na hora de desenhar na tela
        for i in range(60):
            if i % 2 == 0:
                f = FireBall(0, 0, 0, bg.cell_size, bg.id)
                self.back_fireballs.append(f)
            else:
                f = FireBall(0, 0, 0, fg.cell_size, fg.id)
                self.front_fireballs.append(f)
                f.mute()
            self.reset_fireball(f)
            f.destroyed = True                
            self.fireballs.append(f)

        GD.add_screen_obj(self)

    def is_alive(self):
        return self.alive
    
    def kill(self):
        self.set_action("idle")
        self.move_to(self.x + 10, self.window.height, 2.5, MoveAnimation.EASE_IN_BACK)
        self.alive = False

    def activate(self):
        self.move_to(self.x - 150, self.y + 150, 0.5, MoveAnimation.EASE_OUT_EXPO)
        self.can_summon = True
        self.lost_health = False
        self.magic_start_time = time()
        self.set_action("magic")
        self.play_sound("magic")

    def deactivate(self):
        self.move_to(self.og_pos.x, self.og_pos.y, 0.5, MoveAnimation.EASE_OUT_EXPO)
        self.y_speed = -20
        self.set_action("idle")
        self.pause_sound("magic")
        for f in self.fireballs:
            f.destroy(stop_moving=False)

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
                    self.play_sound("damage")

    def reset_fireball(self, f: FireBall):
        x = self.last_fireball_x
        while abs(x - self.last_fireball_x) < f.width * 3:
            x = randint(0, int(self.window.width // f.width)) * f.width
        self.last_fireball_x = x
        y = -f.height
        f.set_position(x, y)
        f.set_speed(600 * difficulty_multiplier(self.health, 5))
        f.set_action("shoot", reset=True)
        f.damaged_player = False
        f.destroyed = False
        f.hit_the_ground = False
        f.played_sound = False
        if self.summon_counter % 2 != 0:
            f.mute()
        else:
            f.unmute()
        self.summon_counter += 1

    def summon_fireballs(self):
        if time() - self.magic_start_time >= 0.75:
            fireball = self.fireballs[self.fireball_index]
            if fireball.is_destroyed() and self.can_summon:
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
        if self.alive:
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
                else:
                    if self.alive:
                        self.summon_fireballs()

                    # Empurra o player e os pedregulhos pra tras com força que diminui com o tempo
                    wind_speed = ((100 / (time() - self.magic_start_time + 0.0001)) + 150) * self.window.delta_time()
                    self.player.x -= wind_speed
                    self.player.x = max(self.player.x, 0)
                    for obj in GD.get_screen_objs("Boulder", self.grid_id):
                        if obj.x > self.x + self.width/2:
                            obj.x += wind_speed
                        else:
                            obj.x -= wind_speed

        self.handle_fireballs()

    def mute(self):
        super().mute()
        for f in self.fireballs:
            f.mute()

    def unmute(self):
        super().unmute()
        for f in self.fireballs:
            f.unmute()

    def update(self):
        self.handle_actions()
        super().update()

    def draw(self):
        for f in self.back_fireballs:
            f.draw()
        super().draw()
        for f in self.front_fireballs:
            f.draw()


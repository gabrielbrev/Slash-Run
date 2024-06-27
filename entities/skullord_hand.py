from PPlay.sprite import Sprite

from .fixed_entity import FixedEntity
from .boulder import Boulder

from grid_objects.energy_orb import EnergyOrb

from core.global_data import GlobalData as GD
from core.move_animation import MoveAnimation as MA
from core.grid import Grid

from utils import Vector

from time import time
from random import randint

class SkullordHand(FixedEntity):
    GRAVITY = 50

    def __init__(self, x, y, grid: Grid):
        self.player = GD.get_player()
        self.grid = grid
        self.grid_id = grid.id
        if self.grid_id == self.player.fg.id:
            s = Sprite("assets/entities/skullord/hand/left/idle.png")
        else:
            s = Sprite("assets/entities/skullord/hand/right/idle.png")
        width = s.width
        height = s.height
        super().__init__(x, y, width, height)

        self.ground_y = grid.get_inf_ground_y()
        self.idle_y = self.ground_y - self.grid.cell_size * 4.5 - self.height

        self.y_speed = -20

        self.action_change_time = time()
        self.action_cooldown = 5
        
        if self.grid_id == self.player.fg.id:
            self.add_sprite("idle", "assets/entities/skullord/hand/left/idle.png", 1, 500)
            self.add_sprite("smash", "assets/entities/skullord/hand/left/idle.png", 1, 500)
            self.add_sprite("inactive", "assets/entities/skullord/hand/left/idle.png", 1, 500)
            self.add_sprite("activating", "assets/entities/skullord/hand/left/idle.png", 1, 500)
            self.set_action("inactive")
        else:
            self.add_sprite("idle", "assets/entities/skullord/hand/right/idle.png", 1, 500)
            self.add_sprite("smash", "assets/entities/skullord/hand/right/idle.png", 1, 500)
            self.add_sprite("inactive", "assets/entities/skullord/hand/right/idle.png", 1, 500)
            self.add_sprite("activating", "assets/entities/skullord/hand/right/idle.png", 1, 500)
            self.set_action("inactive")

        self.attacked = False

        self.follow_speed = 270
        self.same_grid_as_player = False

        self.arsenal = [
            [Boulder(self.window.width + 100, self.ground_y - self.grid.cell_size * 4, self.grid.cell_size, self.grid.id, False)], 
            [EnergyOrb(self.window.width + self.grid.cell_size * i, self.ground_y - self.grid.cell_size, self.grid.cell_size, self.grid.id) for i in range(2)]
        ]
        self.summoned_objs = []
        self.summon_cooldown = randint(7, 10)
        self.summon_time = time()

        self.alive = True

        self.damaged = False

        GD.add_screen_obj(self)

    def is_moving(self):
        return self.move_animation.is_playing()
    
    def is_alive(self):
        return self.alive
    
    def attack(self):
        self.attacked = True

    def kill(self):
        self.alive = False

    def damage(self):
        if not (self.damaged or self.is_moving()):
            self.blink(0.7)
            self.damaged = True
            self.move_to(self.window.width, self.y - 50, 1, MA.EASE_IN_OUT_CUBIC)

    def deactivate(self):
        self.set_action("inactive")
        self.move_to(self.og_pos.x, self.og_pos.y, 0.5, MA.EASE_IN_OUT_CUBIC)

    def activate(self):
        self.set_action("activating")
        self.alive = True
        self.move_to(self.player.x + self.player.width/2 - self.width/2, self.idle_y, 0.5, MA.EASE_IN_OUT_CUBIC)
        self.action_cooldown /= randint(1, 4)
        self.action_change_time = time()

    def idle(self):
        self.set_action("idle")
        self.move_to(self.x, self.idle_y, 1, MA.EASE_OUT_QUAD)

    def smash(self):
        self.attacked = False
        self.lost_health = False
        self.set_action("smash")
        self.move_to(self.x, self.ground_y - self.height, 0.65, MA.EASE_IN_BACK, 5)

    def move_right(self):
        self.x += self.follow_speed * self.window.delta_time()
    
    def move_left(self):
        self.x -= self.follow_speed * self.window.delta_time()

    def summon_obj(self):
        if randint(0, 4):
            self.summoned_objs = self.arsenal[0]
        else:
            self.summoned_objs = self.arsenal[1]
        for obj in self.summoned_objs:
            if obj.x + obj.width < 0:
                obj.reset()

    def update_summoned_objs(self):
        curr_time = time()
        if curr_time - self.summon_time >= self.summon_cooldown:
            self.summon_time = curr_time
            self.summon_cooldown = randint(30, 50) / 10
            if randint(0, 1):
                if self.alive:
                    self.summon_obj()
        if len(self.summoned_objs):
            for obj in self.summoned_objs:
                obj.x -= self.grid.speed.get_value() * self.window.delta_time()
                obj.update()

                if GD.off_screen(self.summoned_objs[-1]) < 0:
                    self.summoned_objs = []

    def handle_actions(self):
        if not self.damaged:
            curr_time = time()
            if self.get_action() == "idle":
                player_center_x = self.player.x + self.player.width/2
                hand_center_x = self.x + self.width/2
                if self.same_grid_as_player:
                    if curr_time - self.action_change_time >= self.action_cooldown:
                        self.action_change_time = curr_time
                        self.action_cooldown = randint(0, 15) / 10
                        self.smash()

                    if hand_center_x > player_center_x:
                        self.move_left()
                    else:
                        self.move_right()
                else:
                    self.deactivate()

            elif self.get_action() == "smash":
                if not self.move_animation.is_playing():
                    if curr_time - self.action_change_time >= self.action_cooldown:
                        self.action_change_time = curr_time
                        self.action_cooldown = randint(25, 30) / 10
                        self.idle()

            elif self.get_action() == "inactive":
                if self.same_grid_as_player:
                    self.activate()
                else:
                    if self.y >= self.og_pos.y:
                        self.y_speed -= SkullordHand.GRAVITY * self.window.delta_time()
                    else:
                        self.y_speed += SkullordHand.GRAVITY * self.window.delta_time()
                    self.y += self.y_speed * self.window.delta_time()

            elif self.get_action() == "activating":
                if not self.move_animation.is_playing():
                    self.set_action("idle")

    def update(self):
        if self.alive:
            self.same_grid_as_player = self.player.curr_grid.id == self.grid.id and not self.player.switching

            if not self.same_grid_as_player:
                self.tracking_player = False

        self.update_summoned_objs()
        super().update()

    def draw(self):
        for obj in self.summoned_objs:
            if GD.on_screen(obj, append_to_list=True):
                obj.draw()
        if self.alive:
            super().draw()